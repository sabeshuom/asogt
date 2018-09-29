#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
STATE_DETAILS = {"NSW": 2, "VIC": 3, "SA": 5,
                 "QLD": 6, "WA": 7, "ACT": 4, "NZW": 8, "NZH": 9, "All": "Any"}
# 7,8,9,
COMPETITION_IDS = {"All": "Any"}

GRADE_WEIGHTS = {"First Prize": 2000,
                 "Second Prize": 500,
                 "Third Prize": 100,
                 "Grade A": 20,
                 "Grade B": 10,
                 "Grade C": 5,
                 "Participated": 1,
                 }

__group_comp__ = "குழுநிலைப் போட்டிகள்"
__special_comp__ = "விசேட தமிழார்வ தேர்வு"
__national_comp__ = "தேசிய நிலைப்  போட்டிகள்"
DIVISION_ORDER = [("பாலர் பிரிவு", "P"),
                  ("ஆரம்பப் பிரிவு", "B"), ("கீழ்ப் பிரிவு", "L"),
                  ("மத்திய பிரிவு", "I"), ("மேற் பிரிவு", "S"),
                  ("அதிமேற் பிரிவு", "AS"), ("இளைஞர் பிரிவு", "Y"),
                  (__group_comp__,
                   "G"), (__special_comp__, "SP"), (__national_comp__, "N"),
                  ]
GROUP_COMPS = ["வினாடி வினாப் போட்டி - அதிமேற் பிரிவு",
               "வினாடி வினாப் போட்டி - இளைஞர் பிரிவு", "விவாத போட்டி - இளைஞர் பிரிவு"
               ]
SPECIAL_COMPS = ["விசேட அடிப்படை தமிழார்வ எழுத்தறிவுத் தேர்வு - இடைநிலை",
                 "விசேட அடிப்படை தமிழார்வ எழுத்தறிவுத் தேர்வு - மேல்நிலை"]

GRADES = ["First Prize", 
          "Second Prize",
          "Third Prize",
          "Forth Prize",
          "Fifth Prize",
          "Sixth Prize",
          "Seventh Prize",
          "Eigth Prize",
          "Ninth Prize",
          "Tenth Prize",
          "Grade A",
          "Grade B",
          "Grade C",
          "Participated",
          ]


NATIONAL_GRADES = [
    "First Prize (Gold Medal)",
    "Second Prize (Silver Medal)",
    "Third Prize (Bronze Medal)",
    "Fourth Prize",
    "Fifth Prize",
    "Sixth Prize",
    "Seventh Prize",
    "Eighth Prize",
    "Ninth Prize",
    "Tenth Prize",
    "Grade A",
    "Grade B",
    "Grade C",
    "Participated",
]


class Result(object):
    def __init__(self, result):
        self.std_no = result[0]
        self.name_e = result[1].replace("<br>", " ")
        self.name_t = result[2].replace("<br>", " ")
        self.name_bamini = unicode2bamini(self.name_t)
        self.gender = result[3]
        self.division_t = result[4]
        self.exam_e = result[6].split("<br>")[0]
        self.grade = result[7]
        self.award = result[8]
        self.comp_t = result[12].strip()
        self.exam_category = result[5]


class Competition(object):
    def __init__(self, competition):
        self.std_no = cleanhtml(competition[0])
        self.exam_e = competition[1]
        self.name_e = competition[6].replace("<br>", " ")
        self.name_t = competition[7].replace("<br>", " ")
        self.name_bamini = unicode2bamini(self.name_t)
        self.paid_status = competition[18]


class Exam(object):
    def __init__(self, exam):
        self.exam_code = exam[0]
        self.exam_e = exam[1]
        self.exam_t = exam[2]
        self.comp_code = exam[3]
        self.exam_bamini = unicode2bamini(self.exam_t)


def get_student_weight(std_data):
    std_weight = 0
    for res in std_data[2:]:
        grade = res.split(" - ")[-1]
        try:
            std_weight += GRADE_WEIGHTS[grade]
        except Exception, e:
            print(
                "Error in getting student weight for grade {:s}".format(grade))
    return std_weight


def result_weight(result):
    grade = result.grade if result.award == "" else result.award
    return GRADE_WEIGHTS.get(grade, 0)


def get_ref_data_from_excel():
    class RefData(object):
        pass
    df = pd.ExcelFile(COMPET_XLS)
    ref_data = RefData()
    ref_data.competition_details = df.parse(
        "competitions").fillna('')
    ref_data.cert_competitions = df.parse(
        "certificate-competitions").fillna('').transpose()
    ref_data.cert_common_fields = df.parse(
        "certificate-common_fields")['details'].fillna('')
    ref_data.cert_grades = df.parse(
        "certificate-grades").transpose().fillna('')
    ref_data.cert_gender = df.parse(
        "certificate-gender").transpose().fillna('')
    ref_data.cert_states = df.parse(
        "certificate-states").transpose().fillna('')
    col_data = df.parse("certificate-cols").fillna('')
    ref_data.cert_cols_list = col_data['COLS'].tolist()
    ref_data.cert_cols_format = col_data.set_index('COLS').transpose()

    return ref_data


def get_certificate_info():
    df = pd.ExcelFile(COMPET_XLS)
    cert_data = {}
    cert_data['competitions'] = df.parse(
        "certificate-competitions").fillna('').transpose().to_dict()
    cert_data['common_fields'] = df.parse(
        "certificate-common_fields")['details'].fillna('').to_dict()
    cert_data['grades'] = df.parse(
        "certificate-grades").transpose().fillna('').to_dict()
    cert_data['gender'] = df.parse(
        "certificate-gender").transpose().fillna('').to_dict()
    cert_data['states'] = df.parse(
        "certificate-states").transpose().fillna('').to_dict()
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


def get_exam_info(sess, state, exam_category=["State"], competition="All"):
    # get exam infor for each state
    # Returns:
    #   Exam objext for each exam
    competitions_url = "https://www.tamilcompetition.org.au/admin/exam/searchcomp/"
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": "2018",
        "division_id": "Any",
        "exam_category_id": "Any",
        "location_id": "Any",
        "competition_id": COMPETITION_IDS[competition],
        "exam_id": "Any",
        "search_exam": "Search",
    }
    res = sess.post(
        competitions_url,
        data=payload,
    )
    exams = get_data_table(sess, "exam")
    exam_details = {}
    for exam in exams:
        exam_cat = exam[4]
        if exam_cat in exam_category:
            exam_obj = Exam(exam)
            exam_details[exam_obj.exam_e] = exam_obj
    return exam_details


def init_sess(username="yoges", password="Yoges"):
    # init session to retrieve data
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
    max_len = -1
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


def get_competition_details(sess, state, year="2018", division="",  exam_category=["State"],  competition_type="", competition=""):
    assert competition != "" or (division != "" and competition_type !=
                               ""), "have to give either competition id or competiion type id with division id"
    competitions_url = "https://www.tamilcompetition.org.au/admin/student_competitions/searchcomp/"
    
    # make sure we consider all the states if we doing this in national state
    if exam_category == "National":
        state = "All"
    
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": year,
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
    if competition != "":
        payload["competition_id"] = COMPETITION_IDS[competition]
    else:
        payload["competition_type_id"] = COMPETITION_TYPE_IDS[competition_type]
        payload["division_id"] = DIVISION_IDS[division]

    res = sess.post(
        competitions_url,
        data=payload,
    )
    comp_data = get_data_table(sess, "student_competitions")
    comp_data_objs = []
    for comp in comp_data:
        if comp[3] is not None:
            if comp[3] in exam_category:
                comp_data_objs.append(Competition(comp))
        else:
            print(comp)
    return comp_data_objs


def get_results(sess, state="All", year="2018", competition="All", exam_category=["State", "Final"]):
    if exam_category == "National":
        state = "All"

    competitions_url = "https://www.tamilcompetition.org.au/admin/results/searchcomp/"
    payload = {
        "state_id": STATE_DETAILS[state],
        "year": year,
        "division_id": "Any",
        "gender": "2",
        "student_no": "",
        "competition_id": COMPETITION_IDS[competition],
        "competition_type_id": "Any",
        "exam_id": "Any",
        "tamil_school_id": "Any",
        "add": "Search",
    }
    res = sess.post(
        competitions_url,
        data=payload,
    )
    results = get_data_table(sess, "results")
    return [Result(result) for result in results if result[5] in exam_category]


def sort_std_keys_for_division(division_data):
    std_weights = {}
    for student in division_data:
        std_weights[student] = 0
        for comp in division_data[student]:
            weight = GRADE_WEIGHTS[division_data[student][comp]]
            std_weights[student] += weight
    return sorted(std_weights, key=lambda x: std_weights[x], reverse=True)


class Student(object):
    def __init__(self, std_no, name_t="", name_e="", seat_pos="999"):
        self.std_no = std_no
        self.name_t = name_t
        self.name_e = name_e
        self.seat_pos = seat_pos
        self.name_bamini = unicode2bamini(name_t)


def process_results_for_seating_number(results, exam_category=["State", "Final"]):
    ordered_results = {division: {} for division, _ in DIVISION_ORDER}
    division_comp_map = {division: {} for division, _ in DIVISION_ORDER}
    student_data_map = {}
    for result in results:
        try:
            # get comp grade details
            std_no = result.std_no
            division = result.division_t
            grade = result.grade if result.award == "" else result.award
            comp = result.comp_t
            if std_no not in student_data_map:
                student_data_map[std_no] = Student(
                    std_no, name_t=result.name_t, name_e=result.name_e)

            if comp in GROUP_COMPS:
                division = __group_comp__
            if comp in SPECIAL_COMPS:
                division = __special_comp__
            if grade in GRADE_WEIGHTS:
                if comp not in division_comp_map[division]:
                    division_comp_map[division][comp] = 0
                division_comp_map[division][comp] += 1

                if std_no not in ordered_results[division]:
                    ordered_results[division][std_no] = {}
                ordered_results[division][std_no][comp] = grade
        except Exception as e:
            print("Getting exception on getting results for book, Error - {}".format(e))

    seat_count = 0
    for division, division_prefix in DIVISION_ORDER:
        if division not in ordered_results:
            print("division {} not found in ordered results".format(division))
            continue
        division_data = ordered_results[division]

        if division_prefix == "G":
            ordered_stds = sort_std_no_group(division_data)
        else:
            ordered_stds = sort_std_keys_for_division(division_data)

        for std_no in ordered_stds:
            if student_data_map[std_no].seat_pos in ["", "999"]:
                seat_count += 1
                seat_pos = '{:s}{:03d}'.format(
                    division_prefix, seat_count)
                student_data_map[std_no].seat_pos = seat_pos

    return ordered_results, division_comp_map, student_data_map


def sort_national_results(results):
    division_weights = {division: weight for weight,
                        (division, prefix) in enumerate(DIVISION_ORDER)}
    national_grade_weights = {
        grade: weight for weight, grade in enumerate(NATIONAL_GRADES)}

    def grade_weight(result):
        grade = result.grade if result.award == "" else result.award
        return national_grade_weights[grade]

    # filter resutls:
    results = [result for result in results if result.grade in national_grade_weights]
    sorted_results = sorted(results, key=lambda x: (
        division_weights[x.division_t], x.comp_t, grade_weight(x)))
    student_data_map = {}
    seat_count = 0
    for result in sorted_results:
        std_no = result.std_no
        if std_no not in student_data_map:
            seat_count += 1
            seat_pos = "N{:03d}".format(seat_count)
            student_data_map[std_no] = Student(
                std_no, name_t=result.name_t, name_e=result.name_e, seat_pos=seat_pos)
    return sorted_results, student_data_map


def sort_std_no_group(division_data):
    comps = {}
    ordered_stds = []
    for std_no in division_data:
        std_comps = division_data[std_no]
        for comp_t in std_comps:
            if comp_t not in comps:
                comps[comp_t] = {grade: [] for grade in GRADES}
            grade = std_comps[comp_t]
            comps[comp_t][grade].append(std_no)

    for grade in GRADES:
        for comp_t in comps:
            if grade not in comps[comp_t]:
                continue
            else:
                for std_no in comps[comp_t][grade]:
                    if std_no not in ordered_stds:
                        ordered_stds.append(std_no)
    return ordered_stds


def split_data(comp_data):
    comp_sets = {}
    for comp in comp_data:
        exam_e = comp.exam_e
        comp_sets[exam_e] = comp_sets.get(exam_e, [])
        comp_sets[exam_e].append(comp)
    return comp_sets


if __name__ == "__main__":
    # username = "sabesan"
    # password = "Sabesan4NSW"
    # state = "NSW"
    # sess = init_sess(username, password)
    # # get_student_details(sess, sate, division="All")
    # # get_competition_details(sess, state, division="All", competition="All")

    # # cert_data = get_certificate_info()

    # results = get_results(sess, state)
    # ordered_results, divisin_comp = process_results_for_seating_number(results)
    # import pdb
    # pdb.set_trace()

    get_data_from_excel()
