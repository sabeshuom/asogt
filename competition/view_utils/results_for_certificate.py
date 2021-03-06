#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import json
import xlsxwriter
import re
import xlrd
import string
import numpy as np
reload(sys)  
sys.setdefaultencoding('utf-8')

sys.path.append("../../")
from asogt.settings import MEDIA_ROOT, BASE_DIR
from core.data_utils import init_sess,\
    get_results,\
    cleanhtml,\
    split_data,\
    get_ref_data_from_excel,\
    process_results_for_seating_number,\
    sort_national_results
from core import unicode_to_bamini

from core.write_timetable import add_time_table


national_formatted_grades = ["Fourth Prize",
                                "Fifth Prize",
                                "Sixth Prize",
                                "Seventh Prize",
                                "Eighth Prize",
                                "Ninth Prize",
                                "Tenth Prize"]

# CERT_INFO = get_certificate_info()
REF_DATA = get_ref_data_from_excel()


def merge_dicts(dict_list):
    new_dict = {}
    for c_dict in dict_list:
        new_dict.update(c_dict)
    return new_dict


def get_row_data(result, cert_state, student_data_map):
    comp_details = REF_DATA.competition_details
    cert_competitions = REF_DATA.cert_competitions.to_dict()
    cert_common_fields = REF_DATA.cert_common_fields.to_dict()
    cert_states = REF_DATA.cert_states.to_dict()
    cert_gender = REF_DATA.cert_gender.to_dict()
    cert_grades = REF_DATA.cert_grades.to_dict()

    try:
        std_no = result.std_no
        name_e = result.name_e
        name_t = result.name_t
        name_bamini = result.name_bamini
        gender = result.gender
        grade = result.grade
        award = result.award
        comp_t = result.comp_t
        if cert_state == "National":
            grade_award = award if award != "" else grade
        else:
            grade_award = grade if award == "" else award + "-" + grade
        comp_code = comp_details[comp_details["Comp Tamil"] == comp_t]["Comp Code"].item()

    except Exception, e:
        print("Getting Exception when getting row data {:s}".format(str(e)))
        import pdb
        pdb.set_trace()

    # get the corresponding keys
    name_info = {
        "STD ID": std_no,
        "NAME": name_t,
        "T2": name_bamini,
        "E3": name_e,
    }

    if (comp_code not in cert_competitions) or (cert_state not in cert_states) or\
            (gender not in cert_gender) or (grade_award not in cert_grades):
        print("STD: {:s} -- Not found comp: {:s}, stae: {:s}, gender: {:s} , grade : {:s}".format(std_no,
                                                                                                  comp_code, cert_state,
                                                                                                  gender, grade_award))
        return None

    name_info["SEAT POS"] = student_data_map[std_no].seat_pos
    comp_info = cert_competitions[comp_code]
    common_info = cert_common_fields
    state_info = cert_states[cert_state]
    gender_info = cert_gender[gender]
    grade_info = cert_grades[grade_award]

    if cert_state == "National":
        if grade_award in national_formatted_grades:
            grade_info["T9"] = grade.replace("Grade ", "")
            grade_info["E5"] = grade_info["E5"] + " ({:s}) ".format(grade)

    row_data = merge_dicts([name_info, common_info, comp_info,
                            state_info, gender_info, grade_info])
    return row_data


def export_to_excel(xls_wb, state,  year, exam_category, username, password, seat_no_map=None):
    sess = init_sess(username, password)
    results = get_results(sess, state=state, year=year, competition="All", exam_category=exam_category)

    if exam_category == "National":
        sorted_results, student_data_map = sort_national_results(results)
    else:
        ordered_results, division_comp_map, student_data_map = process_results_for_seating_number(results,exam_category, seperate_group_comps=False, seat_no_map=seat_no_map)
        filtered_results = [r for r in results if r.std_no in student_data_map]
        sorted_results = sorted(filtered_results, key=lambda x: int(
            student_data_map[x.std_no].seat_pos[-3:]))

    wb = xlsxwriter.Workbook(xls_wb)
    ws = wb.add_worksheet("Certificate_template")

    # comps
    row_title_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'align': 'center',
        'bg_color': '#ebf0df',
        'bold': 1,
        'bottom': 2,
        'top': 2,
        'left': 2,
        'right': 2,
        'font_size': 14,
        'valign': 'vcenter'})
    row_title_height = 20

    tamil_cell_format = wb.add_format({
        'font_name': "Bamini",
        'border': 1,
        'align': 'left',
        'font_size': 14,
        'valign': 'vcenter'})
    eng_cell_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'align': 'left',
        'font_size': 14,
        'valign': 'vcenter'})

    col_headers = REF_DATA.cert_cols_list
    col_formats = REF_DATA.cert_cols_format.to_dict()
    ws.write_row(0, 0, col_headers, row_title_format)
    ws.set_row(0, row_title_height)
    header_rows = 0
    data_row = 1
    col_max_widths = [8]*len(col_headers)

    for result in sorted_results:
        if result.exam_category not in exam_category:
            continue

        if exam_category == "National":
            cert_state = exam_category
        else:
            cert_state = state
        row_data = get_row_data(result, cert_state, student_data_map)
        if row_data is not None:
            for col, header in enumerate(col_headers):
                col_format = col_formats[header]['FORMAT']
                val = row_data[header]
                if col_format == "ENG":
                    cell_format = eng_cell_format
                    font_width = 1.3
                elif col_format == "TAMIL":
                    cell_format = tamil_cell_format
                    font_width = 1.3
                ws.write_string(data_row, col, val, cell_format)
                col_width = int(font_width * len(val))
                if col_width > col_max_widths[col]:
                    col_max_widths[col] = col_width
            data_row += 1
    for col, val in enumerate(col_headers):
        ws.set_column(col, col, col_max_widths[col])

    wb.close()

if __name__ == "__main__":
    username = "sabesan"
    password = "Sabesan4NSW"
    year = "2018"
    # username = "yoges"
    # password = "Yoges"
    state = "NSW"
    xls_wb = "test.xlsx"
    exam_category = ["State", "Final"]
    #exam_category = "National"
    export_to_excel(xls_wb, state, year, exam_category, username, password)
