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
    get_competition_details,\
    get_competition_info,\
    get_exam_info,\
    get_results,\
    cleanhtml,\
    split_data,\
    get_certificate_info,\
    DIVISION_IDS
from core import unicode_to_bamini

from core.write_timetable import add_time_table


BOOK_GRADES = ["First Prize",
                 "Second Prize",
                 "Third Prize",
                 "Grade A",
                 "Grade B",
                 "Grade C",
                 "Participated"]

GRADE_WEGHTS = {"First Prize": 2000, "Second Prize": 500, "Thrid Prize": 100, "Grade A": 20, "Grade B": 10, "Grade C": 5}

def get_results_for_book(state, year, username, password):
    sess = init_sess(username, password)
    results = get_results(sess, state, year,  "All")
    exam_info = get_exam_info(sess, state)

    book_data = {}
    division_comp_map  = {}
    for result in results:
        try:
            # get comp grade details
            std_no = result[0]
            division = result[4]
            grade = result[6]
            comp = result[10]

            if grade in BOOK_GRADES:
                if division not in book_data:
                    book_data[division] = {}
                if division not in division_comp_map:
                    division_comp_map[division] = []
                if comp not in division_comp_map:
                    division_comp_map[division].append(comp)

                fullname_uc = result[2].replace("<br>", " ")
                name_key = "--".join([std_no, fullname_uc])
                
                if name_key not in book_data[division]:
                    book_data[division][name_key] = {}

                book_data[division][name_key][comp] = grade
        except Exception as e:
            print(e)
            import pdb
            pdb.set_trace()

    return book_data,division_comp_map

def sort_division_keys(division_data):
    std_weights  = {}
    for student in division_data:
        std_weights[student] = 0
        for comp in division_data[student]:
            weight = GRADE_WEGHTS[division_data[student][comp]]
            std_weights[student] += weight
    return sorted(std_weights, key=lambda x : std_weights[x], reverse=True)


def export_to_excel(xls_wb, state,  year, username, password):
    book_data, division_map = get_results_for_book(state, year, username, password)

    wb = xlsxwriter.Workbook(xls_wb)


    for division in division_map:
        ws = wb.add_worksheet("division")
        comps = division_map[division]
        row_data = ["std_no", "Namae"]
        ws.write_row(num_of_header_rows + i, 0, results[std_no])

            for i, std_no in enumerate(sorted(results)):
        ws.write_row(num_of_header_rows + i, 0, results[std_no])

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
    headers = ["Number", "Full Nmae", "Line1",
               "Line2", "Line3", "Line4", "Line5", "Trophy", "Size"]
    ws.write_row(5, 0, headers, row_title_format)

    num_of_header_rows = 6
    for i, std_no in enumerate(sorted(results)):
        ws.write_row(num_of_header_rows + i, 0, results[std_no])
    ws.set_column('A:A', 15)
    ws.set_column('B:B', 30)
    ws.set_column('C:G', 45)

    wb.close()


if __name__ == "__main__":
    username = "sabesan"
    password = "Sabesan4NSW"
    # username = "yoges"
    # password = "Yoges"
    state = "NSW"
    xls_wb = "test.xlsx"
    # export_to_excel(xls_wb, state, year, username, password)

    state = "NSW"
    year = "2018"

    book_data, div_map = get_results_for_book(state, year, username, password)

    import pdb; pdb.set_trace()
