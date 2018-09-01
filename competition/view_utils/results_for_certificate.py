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
    get_certificate_info
from core import unicode_to_bamini

from core.write_timetable import add_time_table


CERT_INFO = get_certificate_info()


def merge_dicts(dict_list):
    new_dict = {}
    for c_dict in dict_list:
        new_dict.update(c_dict)
    return new_dict


def get_row_data(result, state, exam_info):
    std_no = result[0]
    name_e = result[1].replace("<br>", " ")
    name_t = result[2].replace("<br>", " ")
    name_t_bamini = unicode_to_bamini.unicode2bamini(name_t)
    gender = result[3]
    exam = result[5]
    grade = result[6]
    comp = exam_info[exam]["comp"]

    # get the corresponding keys
    name_info = {
        "STD ID": std_no,
        "NAME": name_t,
        "T2": name_t_bamini,
        "E3": name_e,
    }

    if (comp not in CERT_INFO["competitions"]) or (state not in CERT_INFO["states"]) or\
            (gender not in CERT_INFO["gender"]) or (grade not in CERT_INFO["grades"]):
        print("Not found comp: {:s}, stae: {:s}, gender: {:s} , grade : {:s}".format(
            comp, state, gender, grade))
        return None

    comp_info = CERT_INFO["competitions"][comp]
    common_info = CERT_INFO["common_fields"]
    state_info = CERT_INFO["states"][state]
    gender_info = CERT_INFO["gender"][gender]
    grade_info = CERT_INFO["grades"][grade]

    row_data = merge_dicts([name_info, common_info, comp_info,
                           state_info, gender_info, grade_info])
    return row_data


def export_to_excel(xls_wb, state, username, password):
    sess = init_sess(username, password)
    import pdb; pdb.set_trace()
    results = get_results(sess, state, "All")

    exam_info = get_exam_info(sess, state)


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
        'border' : 1,
        'align': 'left',
        'font_size': 14,
        'valign': 'vcenter'})

    col_headers = CERT_INFO["cols"]
    col_formats = CERT_INFO["col_formats"]
    ws.write_row(0, 0, col_headers, row_title_format)
    ws.set_row(0, row_title_height)
    header_rows = 0
    data_row = 1
    col_max_widths = [5]*len(col_headers)
    for result in sorted(results, key=lambda x: x[0]):
        row_data = get_row_data(result, state, exam_info)
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
    # username = "yoges"
    # password = "Yoges"
    state = "NSW"
    xls_wb = "test.xlsx"
    export_to_excel(xls_wb, state, username, password)