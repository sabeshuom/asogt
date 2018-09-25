import os
import sys
import requests
import json
import xlsxwriter
import re
import xlrd
import string

sys.path.append("../../")
from asogt.settings import MEDIA_ROOT, BASE_DIR
from core.data_utils import init_sess,\
    get_competition_details,\
    get_ref_data_from_excel,\
    get_exam_info,\
    cleanhtml,\
    split_data
from core.write_timetable import add_time_table

# COMP_DETAILS, COMP_DETAILS_DICT = get_competition_info()

COMP_DATA = get_ref_data_from_excel(
).competition_details.set_index("Comp Code").transpose()


def export_to_excel(xls_wb, state, year, exam_category, username, password):
    sess = init_sess(username, password)

    comp_data_raw = get_competition_details(
        sess, state=state, exam_category=exam_category, year=year, competition="All")

    comp_data_sets = split_data(comp_data_raw)

    exam_details = get_exam_info(
        sess, state=state, exam_category=exam_category)

    wb = xlsxwriter.Workbook(xls_wb)
    left_image_path = os.path.join(MEDIA_ROOT, "left_src.jpg")
    right_image_path = os.path.join(MEDIA_ROOT, "right_src.jpg")

    # comps
    comp_title1_format = wb.add_format({
        'font_name': "Bamini",
        'bold': 2,
        'align': 'center',
        'font_size': 26,
        'valign': 'vcenter'})
    comp_title1_height = 45

    comp_title2_format = wb.add_format({
        'font_name': "Bamini",
        # 'font_name': "Calibri (Body)",
        'align': 'center',
        'font_size': 16,
        'valign': 'vcenter'})
    comp_title2_height = 30

    comp_title3_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'align': 'center',
        'font_size': 18,
        'valign': 'vcenter'})
    comp_title3_height = 30

    comp_header_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'bg_color': '#ebf0df',
        'bold': 1,
        'bottom': 2,
        'top': 2,
        'left': 1,
        'right': 1,
        'align': 'left',
        'font_size': 14,
        'valign': 'vcenter'})
    comp_header_height = 30

    comp_row_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'font_size': 14,
        'align': 'left'})
    comp_row_height = 25

    comp_header_right_border = wb.add_format({
        'font_name': "Calibri (Body)",
        'bg_color': '#ebf0df',
        'bold': 1,
        'bottom': 2,
        'top': 2,
        'left': 1,
        'right': 2,
        'align': 'left',
        'font_size': 14,
        'valign': 'vcenter'})

    # stats
    stats_row_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'font_size': 12,
        'align': 'left'})

    stats_title_format = wb.add_format({
        'bold': 1,
        'bottom': 2,
        'font_size': 16,
        'align': 'center',
        'valign': 'vcenter'})

    stats_header_format = wb.add_format({
        'bold': 1,
        'bottom': 2,
        'align': 'center',
        'font_size': 14,
        'valign': 'vcenter'})

    # common formats
    tamil_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'font_size': 16,
        'border': 1,
        'align': 'left'})

    tamil_header = wb.add_format({
        'font_name': "Bamini",
        'bold': 1,
        'font_size': 16,
        'valign': 'vcenter',
        'bottom': 2,
        'top': 2,
        'left': 1,
        'right': 1,
        'bg_color': '#ebf0df',
        'align': 'left'})

    # setting up stats
    ws_stats = wb.add_worksheet("stats")
    ws_stats.merge_range('A1:J1', "Participants Count", stats_title_format)
    ws_stats.write_row(1, 0, ["Comp-code", "Desc", "Count", "Time(S)", "Admin(S)", "Total Time (S)",
                              "Judge Buf(S)", "Total(S)", "Total(M)", "Comment"], stats_header_format)
    ws_stats.set_column('A:A', 20)
    ws_stats.set_column('B:B', 30)
    ws_stats.set_column('C:C', 15)
    ws_stats.set_column('D:J', 15)
    stats_row = 2

    # ws for time table oral
    oral_start_time = "1:30 PM"
    written_start_time = "9:30 AM"
    ws_oral_time_table = wb.add_worksheet("Time Table - oral")
    ws_written_time_table = wb.add_worksheet("Time Table - written")

    oral_comps = {}
    written_comps = {}
    # comp_data_raw = get_competition_details(sess, competion_id= comp["Comp Id"])

    for exam_e in sorted(comp_data_sets):
        if exam_e not in exam_details:
            print("Exam not found")
            print exam_e
            continue
        comp_data = comp_data_sets[exam_e]
        exam = exam_details[exam_e]
        exam_code = exam.exam_code
        comp_code = exam.comp_code
        comp = COMP_DATA[comp_code]
        comp_type = comp["Comp Type"]
        comp_time = comp["Time"]
        comp_admin = comp["Admin"]
        judge_buf = comp["Comp Time"]

        ws = wb.add_worksheet(exam_code)
        comp_count = len(comp_data)
        comp_total = (comp_time + comp_admin) * comp_count
        comp_total_sec = comp_total + judge_buf
        comp_total_min = float('{:0.2f}'.format(comp_total_sec/60.0))
        row_data = [exam_code, exam_e, comp_count, comp_time, comp_admin,
                    comp_total,  judge_buf, comp_total_sec, comp_total_min, ""]

        # writing stats info
        ws_stats.write_row(stats_row, 0, row_data, stats_row_format)
        ws_stats.set_row(stats_row, 25)
        stats_row += 1

        # setting up oral and written details
        if comp_type.lower() == "oral":
            oral_comps[exam_code] = (comp_count, comp_total_min)
        else:
            written_comps[exam_code] = (comp_count, comp_total_min)

        # adding title images

        ws.insert_image('A1', left_image_path, {
                        'x_offset': 20, 'y_offset': 10})
        ws.insert_image('F1', right_image_path, {
                        'x_offset': -20, 'y_offset': 10})

        #  titile 1 for comp sheet
        title1 = "jkpo; Cf;Ftpg;Gg; Nghl;b - 2018"
        ws.merge_range('A1:F1', title1, comp_title1_format)
        ws.set_row(0, comp_title1_height)
        #  titile 2 for comp sheet
        # title2 = unicode2bamini(exam_details[exam_e]["exam_t"])
        title2 = exam.exam_bamini
        ws.merge_range('A2:F2', title2, comp_title2_format)
        ws.set_row(1, comp_title2_height)
        #  titile 3 for comp sheet
        title3 = exam_code
        ws.merge_range('A3:F3', title3, comp_title3_format)
        ws.set_row(2, comp_title3_height)

        # header for comp sheet
        ws.write_row(3, 0, ["Number", "Student ID", "Student Name",
                            "", "Payment", "Comments"], comp_header_format)
        ws.write("D4", "khzthpd; ngaH", tamil_header)
        ws.write("F4", "Comments", comp_header_right_border)
        ws.set_row(3, comp_header_height)
        header_rows = 4
        comp_data = sorted(comp_data, key=lambda x: x.name_e)
        for row, comp_row in enumerate(comp_data):
            cur_row = row + header_rows
            ws.write_row(
                cur_row, 0, ["", comp_row.std_no, comp_row.name_e, comp_row.name_t, comp_row.paid_status, ""], 
                comp_row_format)
            ws.write("D{:0d}".format(cur_row+1), comp_row.name_t, tamil_format)
            ws.set_row(cur_row, comp_row_height)

        ws.set_column('A:B', 11)
        ws.set_column('C:C', 35)
        ws.set_column('D:D', 55)
        ws.set_column('E:E', 15)
        ws.set_column('F:F', 15)

    stats_ref_range = "stats!$A${:d}:$J${:d}".format(3, stats_row + 1)
    total_time_col = 9

    add_time_table(wb, ws_oral_time_table, oral_start_time, oral_comps,
                   stats_ref_range, total_time_col, comp_type="oral")
    add_time_table(wb, ws_written_time_table, written_start_time,
                   written_comps, stats_ref_range, total_time_col, comp_type="written")

    wb.close()


if __name__ == "__main__":
    username = "sabesan"
    password = "Sabesan4NSW"
    # username = "yoges"
    # password = "Yoges"
    state = "All"
    exam_category = "National"
    xls_wb = "test.xlsx"
    year = "2018"
    export_to_excel(xls_wb, state, year, exam_category, username, password)
