
import os
import sys
import requests
import json
import xlsxwriter
import re
import xlrd
import string
import numpy as np
from operator import itemgetter
from itertools import groupby
sys.path.append("../../")
from core.data_utils import init_sess,\
    get_student_details,\
    get_competition_details


def get_formatted_student_details(state, year, username, password):
    sess = init_sess(username, password)
    students = get_student_details(sess, state=state, year=year)
    headers = ["StdNo", "IndNo", "Name (T)", "Name (E)", 'DOB', "Division", 'Gender', 'Phone', 'Email']
    data = []
    for r in students:
        data.append([r.std_no, r.ind_no, r.name_t, r.name_e, r.dob, r.division_t, r.gender, r.phone, r.email])
    return data, headers


def export_payment_summary(xls_wb, state, year, exam_category, username, password):
    sess = init_sess(username, password)

    comp_data_raw = get_competition_details(
        sess, state=state, exam_category=exam_category, year=year, competition="All")
    get_comp_info(comp_data_raw)

    date_comp_sets_by_id, date_comp_sets_by_family = split__data(comp_data_raw)

    wb = xlsxwriter.Workbook(xls_wb)
    # left_image_path = os.path.join(MEDIA_ROOT, "left_src.jpg")
    # right_image_path = os.path.join(MEDIA_ROOT, "right_src.jpg")

    # comps
    index_height = 170
    index_ind_format = wb.add_format({
        'font_name': "Impact",
        'bold': 3,
        'border': 5,
        'align': 'center',
        'font_size': 80,
        'valign': 'vcenter'})
    index_name_format = wb.add_format({
        'font_name': "Arial",
        'bold': 2,
        'border': 5,
        'align': 'center',
        'font_size': 12,
        'valign': 'vcenter'})

    index_exam_format = wb.add_format({
        'font_name': "Arial",
        'text_wrap': True,
        'border': 5,
        'align': 'center',
        'font_size': 10,
        'valign': 'vcenter'})

    # setting up family list
    family_header_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'bg_color': '#ebf0df',
        'bold': 1,
        'bottom': 2,
        'top': 2,
        'left': 1,
        'right': 1,
        'align': 'center',
        'font_size': 18,
        'valign': 'vcenter'})
 
    family_row_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'font_size': 14,
        'valign': 'vcenter',
        'align': 'left'})
    family_count_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'bold':2,
        'font_size': 20,
        'valign': 'vcenter',
        'align': 'center'})
    family_ind_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'bold': 2,
        'border': 1,
        'font_size': 20,
        'valign': 'vcenter',
        'align': 'center'})

    # setting up index tags
    for date in date_comp_sets_by_id:
        comp_sets_by_id = date_comp_sets_by_id[date]
        comp_sets_by_family = date_comp_sets_by_family[date]
        ws_ids = wb.add_worksheet("ids-" + date)
        row = 0
        ws_ids.set_column(0, 0, 41.75)
        ws_ids.set_column(1, 1, 41.75)
        aa = [{'div': a.split("-")[0], 'id': a.split("-")[1]} for a in comp_sets_by_id.keys()]
        aa.sort(key=itemgetter('div'))
        for div, items in groupby(aa, key=itemgetter('div')):
            for item in sorted(items, key=lambda x: int(x['id'])):
                ind_no = item["div"] + "-" + item['id'] 
                exams = comp_sets_by_id[ind_no]['exams']
                rows_per_id = len(exams) + 1
                row_height = index_height / float(rows_per_id)
                row += 1
                ws_ids.merge_range('A{}:A{}'.format(row, row+len(exams)), ind_no, index_ind_format)
                ws_ids.write("B{}".format(row), comp_sets_by_id[ind_no]['name'], index_name_format)
                ws_ids.set_row(row-1, row_height)
                for exam in exams:
                    row += 1
                    ws_ids.write("B{}".format(row), exam, index_exam_format)
                    ws_ids.set_row(row-1, row_height)

        # family lists
        ws_family = wb.add_worksheet("familyList -" + date)
        family_row_height = 25

        ws_family.set_column(0, 0, 10)
        ws_family.set_column(1, 1, 20)
        ws_family.set_column(2, 3, 20)
        ws_family.set_column(4, 4, 70)
        ws_family.set_column(5, 5, 25)
        ws_family.write_row(0, 0, ["Family", "Index No", "First Name", "Last Name", "Exams", "Comments"], family_header_format)
        ws_family.set_row(0, family_row_height + 10)
        row = 2
        for count, email_val in enumerate(sorted(comp_sets_by_family.items(), key=lambda x: x[1][x[1].keys()[0]]["lname"])):
            email, val = email_val
            row_family = row
            for ind_no in sorted(val):
                exams = val[ind_no]['exams']
                lname = val[ind_no]['lname']
                fname = val[ind_no]['fname']
                row_ind = row
                for exam in exams:
                    ws_family.write("E{}".format(row), exam, family_row_format)
                    ws_family.set_row(row-1, family_row_height)
                    row += 1
                if (row_ind < row-1):
                    ws_family.merge_range('B{}:B{}'.format(row_ind, row-1), ind_no, family_ind_format)
                    ws_family.merge_range('C{}:C{}'.format(row_ind, row-1), fname, family_row_format)
                    ws_family.merge_range('D{}:D{}'.format(row_ind, row-1), lname, family_row_format)
                    ws_family.merge_range('F{}:F{}'.format(row_ind, row-1), "", family_row_format)
                else:
                    ws_family.write('B{}'.format(row_ind), ind_no, family_ind_format)
                    ws_family.write('C{}'.format(row_ind), fname, family_row_format)
                    ws_family.write('D{}'.format(row_ind), lname, family_row_format)
                    ws_family.write('F{}'.format(row_ind), "", family_row_format)
            if row_family < (row-1):
                ws_family.merge_range('A{}:A{}'.format(row_family, row-1), count, family_count_format)
            else:
                ws_family.write('A{}'.format(row_family), count, family_count_format)
    wb.close()

def split__data(comp_data):
    date_comp_sets_by_id = {}
    date_comp_sets_by_family = {}

    for comp in comp_data:
        exam_e = comp.exam_e
        date = comp.date
        if exam_e is None or date is None:
            continue

        if date not in date_comp_sets_by_family:
            date_comp_sets_by_id[date] = {}
            date_comp_sets_by_family[date] = {}

        comp_sets_by_id = date_comp_sets_by_id[date]
        comp_sets_by_family = date_comp_sets_by_family[date]

        ind = comp.ind_no if comp.ind_no else comp.std_no
        if ind in comp_sets_by_id:
            comp_sets_by_id[ind]['exams'].append(exam_e)
        else:
            comp_sets_by_id[ind] = {'exams': [exam_e], 'name': comp.name_e}
        
        if comp.email in comp_sets_by_family:
            if ind in comp_sets_by_family[comp.email]:
                comp_sets_by_family[comp.email][ind]['exams'].append(
                    exam_e)
            else:
                comp_sets_by_family[comp.email][ind] = {
                    'exams': [comp.exam_e], 'fname': comp.fname_e, 'lname': comp.lname_e}

        else:
            comp_sets_by_family[comp.email] = {ind: {'exams': [comp.exam_e], 'fname': comp.fname_e, 'lname': comp.lname_e}
                                                   }
        
    return date_comp_sets_by_id, date_comp_sets_by_family


def export_to_excel(xls_wb, state, year, exam_category, username, password):
    sess = init_sess(username, password)

    comp_data_raw = get_competition_details(
        sess, state=state, exam_category=exam_category, year=year, competition="All")

    date_comp_sets_by_id, date_comp_sets_by_family = split__data(comp_data_raw)

    wb = xlsxwriter.Workbook(xls_wb)
    # left_image_path = os.path.join(MEDIA_ROOT, "left_src.jpg")
    # right_image_path = os.path.join(MEDIA_ROOT, "right_src.jpg")

    # comps
    index_height = 170
    index_ind_format = wb.add_format({
        'font_name': "Impact",
        'bold': 3,
        'border': 5,
        'align': 'center',
        'font_size': 80,
        'valign': 'vcenter'})
    index_name_format = wb.add_format({
        'font_name': "Arial",
        'bold': 2,
        'border': 5,
        'align': 'center',
        'font_size': 12,
        'valign': 'vcenter'})

    index_exam_format = wb.add_format({
        'font_name': "Arial",
        'text_wrap': True,
        'border': 5,
        'align': 'center',
        'font_size': 10,
        'valign': 'vcenter'})

    # setting up family list
    family_header_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'bg_color': '#ebf0df',
        'bold': 1,
        'bottom': 2,
        'top': 2,
        'left': 1,
        'right': 1,
        'align': 'center',
        'font_size': 18,
        'valign': 'vcenter'})
 
    family_row_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'font_size': 14,
        'valign': 'vcenter',
        'align': 'left'})
    family_count_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'border': 1,
        'bold':2,
        'font_size': 20,
        'valign': 'vcenter',
        'align': 'center'})
    family_ind_format = wb.add_format({
        'font_name': "Calibri (Body)",
        'bold': 2,
        'border': 1,
        'font_size': 20,
        'valign': 'vcenter',
        'align': 'center'})

    # setting up index tags
    for date in date_comp_sets_by_id:
        comp_sets_by_id = date_comp_sets_by_id[date]
        comp_sets_by_family = date_comp_sets_by_family[date]
        ws_ids = wb.add_worksheet("ids-" + date)
        row = 0
        ws_ids.set_column(0, 0, 41.75)
        ws_ids.set_column(1, 1, 41.75)
        aa = [{'div': a.split("-")[0], 'id': a.split("-")[1]} for a in comp_sets_by_id.keys()]
        aa.sort(key=itemgetter('div'))
        for div, items in groupby(aa, key=itemgetter('div')):
            for item in sorted(items, key=lambda x: int(x['id'])):
                ind_no = item["div"] + "-" + item['id'] 
                exams = comp_sets_by_id[ind_no]['exams']
                rows_per_id = len(exams) + 1
                row_height = index_height / float(rows_per_id)
                row += 1
                ws_ids.merge_range('A{}:A{}'.format(row, row+len(exams)), ind_no, index_ind_format)
                ws_ids.write("B{}".format(row), comp_sets_by_id[ind_no]['name'], index_name_format)
                ws_ids.set_row(row-1, row_height)
                for exam in exams:
                    row += 1
                    ws_ids.write("B{}".format(row), exam, index_exam_format)
                    ws_ids.set_row(row-1, row_height)

        # family lists
        ws_family = wb.add_worksheet("familyList -" + date)
        family_row_height = 25

        ws_family.set_column(0, 0, 10)
        ws_family.set_column(1, 1, 20)
        ws_family.set_column(2, 3, 20)
        ws_family.set_column(4, 4, 70)
        ws_family.set_column(5, 5, 25)
        ws_family.write_row(0, 0, ["Family", "Index No", "First Name", "Last Name", "Exams", "Comments"], family_header_format)
        ws_family.set_row(0, family_row_height + 10)
        row = 2
        for count, email_val in enumerate(sorted(comp_sets_by_family.items(), key=lambda x: x[1][x[1].keys()[0]]["lname"])):
            email, val = email_val
            row_family = row
            for ind_no in sorted(val):
                exams = val[ind_no]['exams']
                lname = val[ind_no]['lname']
                fname = val[ind_no]['fname']
                row_ind = row
                for exam in exams:
                    ws_family.write("E{}".format(row), exam, family_row_format)
                    ws_family.set_row(row-1, family_row_height)
                    row += 1
                if (row_ind < row-1):
                    ws_family.merge_range('B{}:B{}'.format(row_ind, row-1), ind_no, family_ind_format)
                    ws_family.merge_range('C{}:C{}'.format(row_ind, row-1), fname, family_row_format)
                    ws_family.merge_range('D{}:D{}'.format(row_ind, row-1), lname, family_row_format)
                    ws_family.merge_range('F{}:F{}'.format(row_ind, row-1), "", family_row_format)
                else:
                    ws_family.write('B{}'.format(row_ind), ind_no, family_ind_format)
                    ws_family.write('C{}'.format(row_ind), fname, family_row_format)
                    ws_family.write('D{}'.format(row_ind), lname, family_row_format)
                    ws_family.write('F{}'.format(row_ind), "", family_row_format)
            if row_family < (row-1):
                ws_family.merge_range('A{}:A{}'.format(row_family, row-1), count, family_count_format)
            else:
                ws_family.write('A{}'.format(row_family), count, family_count_format)
    wb.close()


if __name__ == "__main__":
    username = "sabesan"
    password = "Sabesan4NSW"
    year = "2019"
    state = "VIC"
    xls_wb = "test.xlsx"
    exam_category = ["State", "Final"]
    export_to_excel(xls_wb, state, year, exam_category, username, password)
