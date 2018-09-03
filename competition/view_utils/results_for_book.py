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
from core.unicode_to_bamini import unicode2bamini

from core.write_timetable import add_time_table


BOOK_GRADES = ["First Prize",
               "Second Prize",
               "Third Prize",
               "Grade A",
               "Grade B",
               "Grade C",
               "Participated"]

GRADE_INFO = {"First Prize": {"weight": 2000, "grade": (" ", "Kjw; ghpR")},
              "Second Prize": {"weight": 500, "grade": (" ", ",uz;lhk; ghpR")},
              "Third Prize": {"weight": 100, "grade": (" ", "%d;whk; ghpR")},
              "Grade A": {"weight": 20, "grade": ("A ", "epiy")},
              "Grade B": {"weight": 10, "grade": ("B ", "epiy")},
              "Grade C": {"weight": 5, "grade": ("C ", "epiy")},
              "Participated": {"weight": 0, "grade": (" ", "gq;Fgw;wpdhu;")},
              }


def get_results_for_book(state, year, username, password):
    sess = init_sess(username, password)
    results = get_results(sess, state, year,  "All")
    exam_info = get_exam_info(sess, state)

    book_data = {}
    division_comp_map = {}
    for result in results:
        try:
            # get comp grade details
            std_no = result[0]
            division = result[4]
            grade = result[6]
            comp = result[10]

            if grade in GRADE_INFO:
                if division not in book_data:
                    book_data[division] = {}
                if division not in division_comp_map:
                    division_comp_map[division] = {}
                if comp not in division_comp_map[division]:
                    division_comp_map[division][comp] = 0
                division_comp_map[division][comp] += 1

                fullname_uc = result[2].replace("<br>", " ")
                name_key = "--".join([std_no, fullname_uc])

                if name_key not in book_data[division]:
                    book_data[division][name_key] = {}

                book_data[division][name_key][comp] = grade
        except Exception as e:
            print(e)
            import pdb
            pdb.set_trace()

    return book_data, division_comp_map


def sort_division_keys(division_data):
    std_weights = {}
    for student in division_data:
        std_weights[student] = 0
        for comp in division_data[student]:
            weight = GRADE_INFO[division_data[student][comp]]["weight"]
            std_weights[student] += weight
    return sorted(std_weights, key=lambda x: std_weights[x], reverse=True)


def export_to_excel(xls_wb, state,  year, username, password):
    book_data, division_map = get_results_for_book(
        state, year, username, password)

    wb = xlsxwriter.Workbook(xls_wb)
    row_height = 25
    row_title_height = 35

    div_header_format = wb.add_format({
        'font_name': "Bamini",
        'align': 'left',
        'bg_color': '#ebf0df',
        'bold': 1,
        'border': 2,
        'font_size': 14,
        'valign': 'vcenter'})

    bamini_cell_format = wb.add_format({
        'font_name': "Bamini",
        'align': 'left',
        'font_size': 14,
        'border': 1,
        'valign': 'vcenter'})

    uc_cell_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'align': 'left',
        'font_size': 14,
        'border': 1,
        'valign': 'vcenter'})

    for division in division_map:
        ws = wb.add_worksheet(division)
        ws.set_default_row(row_height)
        comps = [comp for comp in sorted(division_map[division], key=lambda x: division_map[division][x], reverse=True)]
        comps_bamini = [unicode2bamini(comp) for comp in comps]
        div_header = ["khztu; ,y.", "KOg; ngau;", "KOg; ngau;"] + comps_bamini
        ws.write_row(0, 0, div_header, div_header_format)
        ws.set_row(0, row_title_height)

        division_data = book_data[division]
        std_ids = sort_division_keys(division_data)
        header_r = 1
        for r, std in enumerate(std_ids):
            std_data = division_data[std]
            std_no, name_uc = std.split("--")

            name_bamini = unicode2bamini(name_uc)
            c = 0
            ws.write_string(header_r + r, c, std_no, uc_cell_format)
            c += 1
            ws.write_string(header_r + r, c, name_uc, uc_cell_format)
            c += 1
            ws.write_string(header_r + r, c, name_bamini, bamini_cell_format)

            for comp in comps:
                c += 1
                ws.write_rich_string(header_r +r, c, " ", uc_cell_format)
                if comp in std_data:
                    grade = std_data[comp]
                    grade_e, grade_bamini = GRADE_INFO[grade]["grade"]
                    ws.write_rich_string(header_r + r, c,
                                         uc_cell_format, grade_e, bamini_cell_format, grade_bamini, uc_cell_format)

        ws.set_column('A:A', 15)
        ws.set_column('B:B', 45)
        ws.set_column('C:C', 35)
        ws.set_column('D:G', 45)

    wb.close()


if __name__ == "__main__":
    username = "sabesan"
    password = "Sabesan4NSW"
    state = "NSW"
    year = "2018"
    xls_wb = "test.xlsx"
    export_to_excel(xls_wb, state, year, username, password)

    # book_data, div_map = get_results_for_book(state, year, username, password)
