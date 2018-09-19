import os
import sys
import requests
import json
import xlsxwriter
import re
import xlrd
import string
import numpy as np

sys.path.append("../../")
from asogt.settings import MEDIA_ROOT, BASE_DIR
from core.data_utils import init_sess,\
    get_results,\
    sort_std_keys_for_division,\
    get_ref_data_from_excel,\
    process_results_for_seating_number,\
    GRADE_WEIGHTS,\
    DIVISION_ORDER,\
    GRADES

from core import unicode_to_bamini

from core.write_timetable import add_time_table


REF_DATA = get_ref_data_from_excel()


def get_trophy_data_by_rows(ordered_results, student_data_map):
    trophy_rows = []
    num_of_lines = 0
    name_cols = 3
    comp_details = REF_DATA.competition_details
    cert_comp_data = REF_DATA.cert_competitions

    # get trophy details for the group information
    def add_trophy_rows_for_group(division_data):
        comps = {}
        for std_no in division_data:
            std_comps = division_data[std_no]
            for comp_t in std_comps:
                if comp_t not in comps:
                    comps[comp_t] = {grade: [] for grade in GRADES}
                grade = std_comps[comp_t]
                comps[comp_t][grade].append(std_no)

        for grade in GRADES:
            for comp_t in comps:
                comp_code = comp_details[comp_details["Comp Tamil"]
                                        == comp_t]["Comp Code"].item()
                comp_division = cert_comp_data[comp_code]["E7"]
                comp_type = cert_comp_data[comp_code]["E9"]
                if grade not in comps[comp_t]:
                    continue
                else:
                    comp_grade_info = "{:s} {:s} - {:s}".format(comp_division,
                                                                comp_type,
                                                                grade)
                    for std_no in comps[comp_t][grade]:
                        std = student_data_map[std_no]
                        seat_pos = std.seat_pos
                        name_e = std.name_e
                        trophy_rows.append(
                            [seat_pos, std_no, name_e, comp_grade_info])

    # loop through the division
    for division, division_prefix in DIVISION_ORDER:
        if division not in ordered_results:
            print("division {} not found.".format(division))
            continue

        division_data = ordered_results[division]

        if division_prefix == "G":
            add_trophy_rows_for_group(division_data)
            continue

        ordered_std_nos = sorted(division_data.keys(), key=lambda x: int(
            student_data_map[x].seat_pos[-3:]))
        for std_no in ordered_std_nos:
            std = student_data_map[std_no]
            seat_pos = std.seat_pos
            name_e = std.name_e
            std_comps = division_data[std_no]
            if division_prefix not in ["SP"]:
                num_of_lines = max(num_of_lines, len(std_comps))
                trophy_rows.append([seat_pos, std_no, name_e])
            for comp_t in sorted(std_comps, key=lambda x: GRADE_WEIGHTS.get(std_comps[x], 0), reverse=True):
                try:
                    comp_code = comp_details[comp_details["Comp Tamil"]
                                             == comp_t]["Comp Code"].item()
                    comp_division = cert_comp_data[comp_code]["E7"]
                    comp_type = cert_comp_data[comp_code]["E9"]
                except Exception, e:
                    print("getting error on processing row {}".format(str(e)))
                    import pdb
                    pdb.set_trace()

                grade = std_comps[comp_t]
                if grade not in GRADES:
                    continue
                comp_grade_info = "{:s} {:s} - {:s}".format(comp_division,
                                                            comp_type,
                                                            grade)
                if division_prefix in ["SP"]:
                    trophy_rows.append(
                        [seat_pos, std_no, name_e, comp_grade_info])
                else:
                    trophy_rows[-1].append(comp_grade_info)
            # check there whehter there is enough competitions there:
            if len(trophy_rows[-1]) == 3:
                print(
                    "No valid competitions grades fround for std_no : {} ".format(std_no))
                del trophy_rows[-1]

    return trophy_rows, num_of_lines

    # for result in sorted(results, key=lambda x: result_weight(x), reverse=True):
    #     try:
    #         # get comp grade details
    #         exam_e = result.exam_e
    #         grade = result.grade if result.award == "" else result.award
    #         if grade in GRADE_WEIGHTS:
    #             std_no = result.std_no
    #             seating_no = seating_num_map[std_no]
    #             name_e = result.name_e
    #             std_data = student_data.get(seating_no, [seating_no, std_no, name_e])
    #             comp_code = exam_info[exam_e].comp_code
    #             comp_grade_info = "{:s} {:s} - {:s}".format(CERT_INFO["competitions"][comp_code]["E7"],
    #                                                         CERT_INFO["competitions"][comp_code]["E9"],
    #                                                         grade)
    #             std_data.append(comp_grade_info)
    #             student_data[seating_no] = std_data
    #             num_of_lines = max(num_of_lines, len(std_data) - name_cols)
    #         else:
    #             print("Grade not found {:s}".format(grade))
    #     except Exception as e:
    #         print(e)
    #         import pdb
    #         pdb.set_trace()
    # return student_data, num_of_lines

# def get_results_per_student(results, exam_info, seating_num_map):
#     student_data = {}
#     num_of_lines = 0
#     name_cols = 3
#     for result in sorted(results, key=lambda x: result_weight(x), reverse=True):
#         try:
#             # get comp grade details
#             exam_e = result.exam_e
#             grade = result.grade if result.award == "" else result.award
#             if grade in GRADE_WEIGHTS:
#                 std_no = result.std_no
#                 seating_no = seating_num_map[std_no]
#                 name_e = result.name_e
#                 std_data = student_data.get(seating_no, [seating_no, std_no, name_e])
#                 comp_code = exam_info[exam_e].comp_code
#                 comp_grade_info = "{:s} {:s} - {:s}".format(CERT_INFO["competitions"][comp_code]["E7"],
#                                                             CERT_INFO["competitions"][comp_code]["E9"],
#                                                             grade)
#                 std_data.append(comp_grade_info)
#                 student_data[seating_no] = std_data
#                 num_of_lines = max(num_of_lines, len(std_data) - name_cols)
#             else:
#                 print("Grade not found {:s}".format(grade))
#         except Exception as e:
#             print(e)
#             import pdb
#             pdb.set_trace()
#     return student_data, num_of_lines


def sort_students(std_result):
    std_weights = {}
    for student in division_data:
        std_weights[student] = 0
        for comp in division_data[student]:
            weight = GRADE_INFO[division_data[student][comp]]["weight"]
            std_weights[student] += weight
    return sorted(std_weights, key=lambda x: std_weights[x], reverse=True)


def compute_trophy_size(result_row):
    """
     compute the trophy size according to below:
    if there is first price: trophy size =1
    else if there is second price: trophy size =2
    else if there is thrid price: trophy size = 3
    otherwise : 4
    """
    grades = [r.split(" - ")[-1] for r in result_row]
    if "First Prize" in grades:
        return 1
    if "Second Prize" in grades:
        return 2
    if "Third Prize" in grades:
        return 3
    return 4


def export_to_excel(xls_wb, state,  year, result_type, username, password):
    sess = init_sess(username, password)
    results = get_results(sess, state=state, year=year,
                          competion="All", result_type=result_type)
    ordered_results, division_comp_map, student_data_map = process_results_for_seating_number(
        results)
    trophy_rows, num_of_lines = get_trophy_data_by_rows(
        ordered_results, student_data_map)
    wb = xlsxwriter.Workbook(xls_wb)
    ws = wb.add_worksheet("Trophy_template")

    row_height = 20
    ws.set_default_row(row_height)
    # comps
    trophy1_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': 'yellow',
        'bold': 1,
        'right': 2,
        'font_size': 14,
        'valign': 'vcenter'})

    trophy2_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': 'yellow',
        'bold': 1,
        'right': 2,
        'font_size': 14,
        'valign': 'vcenter'})

    trophy3_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': 'yellow',
        'bold': 1,
        'right': 2,
        'font_size': 14,
        'valign': 'vcenter'})

    trophy4_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': 'yellow',
        'right': 2,
        'font_size': 14,
        'valign': 'vcenter'})

    trophy5_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': 'yellow',
        'right': 2,
        'bottom': 2,
        'font_size': 14,
        'valign': 'vcenter'})
    note_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': 'yellow',
        'font_size': 14,
        'valign': 'vcenter'})

    row_title_format = wb.add_format({
        'font_name': "Arial",
        'align': 'center',
        'bg_color': '#ebf0df',
        'bold': 1,
        'bottom': 2,
        'top': 2,
        'left': 2,
        'right': 2,
        'font_size': 14,
        'valign': 'vcenter'})

    row_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'align': 'left',
        'font_size': 11,
        'valign': 'vcenter'})

    # trophy headers
    trophy1 = "Australian Society of Graduate Tamils (ASoGT)"
    ws.merge_range('A1:D1', trophy1, trophy1_format)
    trophy2 = "Tamil Competitions 2018 - QLD"
    ws.merge_range('A2:D2', trophy2, trophy2_format)
    trophy3 = "Full Name (Eg: Asvetha Senthilkumaran) - Number (Eg: P001)"
    ws.merge_range('A3:D3', trophy3, trophy3_format)
    trophy4 = "Grade (Eg: First Prize)  - Competition Name (Eg:Palar - Poetry) "
    ws.merge_range('A4:D4', trophy4, trophy4_format)
    trophy5 = "Grade (Eg: First Prize)  - Competition Name (Eg:Palar - Poetry) "
    ws.merge_range('A5:D5', trophy5, trophy5_format)

    # write note
    note = "Note: Black Print on Gold Plate"
    ws.write("E4", note, note_format)

    # write row headers
    headers = ["Seat No", "Std No", "Full Nmae"] +\
        ["Line{:d}".format(line_no + 1) for line_no in range(num_of_lines)] +\
        ["Trophy Size"]
    ws.write_row(5, 0, headers, row_title_format)

    num_of_header_rows = 6
    trophy_column = num_of_lines + 3

    for i, trophy_row in enumerate(trophy_rows):
        ws.write_row(num_of_header_rows + i, 0, trophy_row)
        trophy_size = compute_trophy_size(trophy_row)
        ws.write(num_of_header_rows + i, trophy_column, trophy_size)

    ws.set_column(0, 1, 15)
    ws.set_column(2, 2, 30)
    ws.set_column(3, trophy_column - 1, 45)
    ws.set_column(trophy_column, trophy_column, 15)

    # for i, seating_no in enumerate(sorted(results, key=lambda x: int(x[-3:]))):
    #     result_row = results[seating_no]
    #     ws.write_row(num_of_header_rows + i, 0, result_row)
    #     trophy_size = compute_trophy_size(result_row)
    #     ws.write(num_of_header_rows + i, trophy_column, trophy_size)
    # ws.set_column(0, 1, 15)
    # ws.set_column(2, 2, 30)
    # ws.set_column(3, trophy_column - 1, 45)
    # ws.set_column(trophy_column, trophy_column, 15)

    wb.close()


if __name__ == "__main__":
    username = "sabesan"
    password = "Sabesan4NSW"
    # username = "yoges"
    # password = "Yoges"
    state = "NSW"
    xls_wb = "test.xlsx"
    year = "2018"
    result_type = "State"
    export_to_excel(xls_wb, state, year, result_type, username, password)
