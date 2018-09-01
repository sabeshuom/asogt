import os
import sys
import requests
import json
import xlsxwriter
import re
import xlrd
import pandas as pd
import string
from write_timetable import add_time_table
sys.path.append("../")
from asogt.settings import MEDIA_ROOT, BASE_DIR
# from lxml import html
from unicode_to_bamini import unicode2bamini
import numpy as np

DIVISION_IDS = {"P": "15", "B": "14", "L": "12", "I": "10",
                "S": "7", "AdS": "4", "Y": "3", "AY": "18", "All": "Any"}
COMPETITION_TYPE_IDS = {"P": "1", "S": "2", "V": "4", "SpP-A": "9", "SpP-T": "8", "W": "3", "A": "5", "Q": "7",
                        "D": "6", "All": "Any"}
COMPET_XLS = os.path.join(MEDIA_ROOT, "comp_data_2018.xlsx")
STATE_DETAILS = {"QLD": 6, "NSW": 2}
COMPETITION_IDS = {"All": "Any"}

def get_certificate_info():
    df = pd.ExcelFile(COMPET_XLS)
    cert_data = {}
    cert_data['competitions'] = df.parse("certificate-competitions").fillna('').transpose().to_dict()
    cert_data['common_fields'] = df.parse("certificate-common_fields")['details'].fillna('').to_dict()
    cert_data['grades'] = df.parse("certificate-grades").transpose().fillna('').to_dict()
    cert_data['gender'] = df.parse("certificate-gender").transpose().fillna('').to_dict()
    cert_data['states'] = df.parse("certificate-states").transpose().fillna('').to_dict()
    col_data = df.parse("certificate-cols").fillna('')
    cert_data['cols'] = col_data['COLS'].tolist()
    cert_data['col_formats'] = col_data.set_index('COLS').transpose().to_dict() 
    return cert_data

def get_competition_info():
    wb = xlrd.open_workbook(COMPET_XLS)
    ws = wb.sheet_by_index(0)
    header_keys = ws.row_values(0, end_colx=8)
    comp_details = []
    comp_details_map = {}
    for row_index in xrange(1, ws.nrows):
        vals = ws.row_values(row_index, end_colx=8)
        data = {}
        for col, header_key in enumerate(header_keys):
            val = int(vals[col]) if type(vals[col]) == float else vals[col]
            data[header_key] = val
        comp_details.append(data)
        comp_details_map[data["Comp Code"]] = data
    return comp_details, comp_details_map


def get_exam_info(sess, state, competion="All"):
    competitions_url = "https://www.tamilcompetition.org.au/admin/exam/searchcomp/"
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": "2018",
        "division_id": "Any",
        "exam_category_id": "1",
        "location_id": "Any",
        "competition_id": COMPETITION_IDS[competion],
        "exam_id": "Any",
        "search_exam": "Search",
    }
    res = sess.post(
        competitions_url,
        data=payload,
    )
    data = get_data_table(sess, "exam")
    exam_details = {}
    for exam in data:
        exam_code = exam[0]
        exam_e = exam[1]
        exam_t = exam[2]
        comp = exam[3]
        exam_details[exam_e] = {'code': exam_code,
                                "exam_t": exam_t, "exam_e": exam_e, "comp": comp}
    return exam_details


def init_sess(username="yoges", password="Yoges"):
    payload = {
        "login": username,
        "password": password,
    }
    login_url = "https://www.tamilcompetition.org.au/admin/login/run"
    sess = requests.session()

    res = sess.post(
        login_url,
        data=payload,
    )
    res.raise_for_status()
    return sess


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_data_table(sess, type_key="student_details"):
    max_len = 5000
    types = {
        "student_details": {
            "url": "https://www.tamilcompetition.org.au/admin/student_details/get_data_table?draw=1&",
            "number_of_columns": 15
        },
        "student_competitions": {
            "url": "https://www.tamilcompetition.org.au/admin/student_competitions/get_data_table?draw=1&",
            "number_of_columns": 21
        },
        "exam": {
            "url": "https://www.tamilcompetition.org.au/admin/exam/get_data_table?draw=1&",
            "number_of_columns": 12
        },
        "results": {
            "url": "https://www.tamilcompetition.org.au/admin/results/get_data_table?draw=1&",
            "number_of_columns": 12
        }
    }
    data_type = types[type_key]
    search_str = ""
    number_of_columns = data_type["number_of_columns"]
    data_table_url = data_type["url"]

    for i in range(number_of_columns):
        search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(
            i, "data", str(i))
        search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(i, "name", "")
        search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(
            i, "searchable", "true")
        search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(
            i, "orderable", "true")
        search_str += "columns%5B{:d}%5D%5B{:s}%5D%5B{:s}%5D={:s}&".format(
            i, "search", "value", "")
        search_str += "columns%5B{:d}%5D%5B{:s}%5D%5B{:s}%5D={:s}&".format(
            i, "search", "regex", "false")

    search_str += "order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&start=0&length={:d}&search%5Bvalue%5D=&search%5Bregex%5D=false".format(
        max_len)
 
    data_table_url = data_table_url + search_str
    res = sess.get(data_table_url)
    data = json.loads(res.content)["data"]
    return data


def get_student_details(sess, state, division="All"):
    students_url = "https://www.tamilcompetition.org.au/admin/student_details/searchcomp/"
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": 2018,
        "gender": 2,
        "student_no": "",
        "division_id": DIVISION_IDS[division],
        "country_id": "Any",
        "tamil_school_id": "Any",
        "add": "Search",
    }
    res = sess.post(
        students_url,
        data=payload,
    )
    data = get_data_table("student_details")


def get_competition_details(sess, state, division="",  competition_type="", competion=""):
    assert competion != "" or (division != "" and competition_type !=
                               ""), "have to give either competion id or competiion type id with division id"
    competitions_url = "https://www.tamilcompetition.org.au/admin/student_competitions/searchcomp/"
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": "2018",
        "division_id": "Any",
        "gender": "2",
        "student_no": "",
        "competition_type_id": "Any",
        "competition_id": "Any",
        "tamil_school_id": "Any",
        "start_dob": "",
        "end_dob": "",
        "add": "Search",
    }
    if competion != "":
        payload["competition_id"] = COMPETITION_IDS[competion]
    else:
        payload["competition_type_id"] = COMPETITION_TYPE_IDS[competition_type]
        payload["division_id"] = DIVISION_IDS[division]

    res = sess.post(
        competitions_url,
        data=payload,
    )
    data = get_data_table(sess, "student_competitions")
    return data


def get_results(sess, state="6", competion="All"):
    competitions_url = "https://www.tamilcompetition.org.au/admin/results/searchcomp/"
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": "2018",
        "division_id": "Any",
        "gender": "2",
        "student_no": "",
        "competition_id": COMPETITION_IDS[competion],
        "competition_type_id": "Any",
        "exam_id": "Any",
        "tamil_school_id": "Any",
        "add": "Search",
    }
    res = sess.post(
        competitions_url,
        data=payload,
    )
    results_data = get_data_table(sess, "results")
    return results_data


def split_data(comp_data):
    comp_sets = {}
    for comp in comp_data:
        exam_e = comp[1]
        comp_sets[exam_e] = comp_sets.get(exam_e, [])
        comp_sets[exam_e].append(comp)
    return comp_sets


if __name__ == "__main__":
    # username = "sabesan"
    # password = "Sabesan4NSW"
    # state = "NSW"
    # sess = init_sess(username, password)
    # get_student_details(sess, sate, division="All")
    # get_competition_details(sess, state, division="All", competion="All")

    cert_data = get_certificate_info()
