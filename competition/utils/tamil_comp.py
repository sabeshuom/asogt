import os, sys
import requests
import json
import xlsxwriter
import re
import xlrd
import string
from write_timetable import add_time_table
sys.path.append("../../")
from   asogt.settings import MEDIA_ROOT, BASE_DIR
# from lxml import html
from unicode_to_bamini import unicode2bamini

DIVISION_IDS = {"P": "15", "B": "14", "L": "12", "I" :"10" , "S": "7", "AdS": "4", "Y" : "3", "AY": "18", "All": "Any"}
COMPETITION_TYPE_IDS = {"P": "1", "S": "2", "V": "4", "SpP-A": "9", "SpP-T": "8", "W": "3", "A": "5", "Q" : "7", "D": "6", "All": "Any"}

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPET_XLS = os.path.join(MEDIA_ROOT, "comp_data_2018.xlsx")
OUTPUT_XLS = os.path.join(MEDIA_ROOT, "comp_details_QLD_2018.xlsx")
STATE_ID  = 6 # QLD
STATE_DETAILS  = {"QLD": 6, "NSW" : 2 }
def get_comp_details():
	wb = xlrd.open_workbook(COMPET_XLS)
	ws = wb.sheet_by_index(0)
	header_keys = ws.row_values(0, end_colx=8)
	comp_details = []
	comp_ids = {}
	for row_index in xrange(1, ws.nrows):
		vals = ws.row_values(row_index, end_colx=8)
		data = {}
		for col, header_key in enumerate(header_keys):
			val = int(vals[col]) if type(vals[col]) == float else vals[col]
			data[header_key] = val
		comp_details.append(data)
		comp_ids[data["Comp Code"]] = data
	return comp_details, comp_ids

def init_sess(username="yoges", password="Yoges", state="QLD"):
	global STATE_ID
	STATE_ID = STATE_DETAILS[state]
	payload = {
		"login": username, 
		"password": password, 
	}
	login_url = "http://www.tamilcompetition.org.au/admin/login/run"
	sess = requests.session()

	res = sess.post(
		login_url, 
		data = payload,
	)

	res.raise_for_status()
	return sess

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def get_data_table(sess, type_key="student_details"):
	max_len = 5000
	types = {"student_details" :{
					"url": "http://www.tamilcompetition.org.au/admin/student_details/get_data_table?draw=1&",
					"number_of_columns" : 15
					},
			"student_competitions" :{
					"url": "http://www.tamilcompetition.org.au/admin/student_competitions/get_data_table?draw=1&",
					"number_of_columns" : 21
					},
			"exam" :{
					"url": "http://www.tamilcompetition.org.au/admin/exam/get_data_table?draw=1&",
					"number_of_columns" : 12
					}
	}
	data_type = types[type_key]
	search_str = ""
	number_of_columns = data_type["number_of_columns"]
	data_table_url = data_type["url"]

	for i in range(number_of_columns):
		search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(i, "data", str(i))
		search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(i, "name", "")
		search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(i, "searchable", "true")
		search_str += "columns%5B{:d}%5D%5B{:s}%5D={:s}&".format(i, "orderable", "true")
		search_str += "columns%5B{:d}%5D%5B{:s}%5D%5B{:s}%5D={:s}&".format(i, "search", "value", "")
		search_str += "columns%5B{:d}%5D%5B{:s}%5D%5B{:s}%5D={:s}&".format(i, "search", "regex", "false")

	search_str +="order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&start=0&length={:d}&search%5Bvalue%5D=&search%5Bregex%5D=false".format(max_len)

	data_table_url = data_table_url + search_str
	res = sess.get(data_table_url)
	data = json.loads(res.content)["data"]

	return data

def get_student_details(sess, state_id, division_id= "All"):
	students_url = "http://www.tamilcompetition.org.au/admin/student_details/searchcomp/"
	payload = {
		"state_id":state_id,
		"year": 2018,
		"gender":2,
		"student_no":"",
		"division_id": DIVISION_IDS[division_id],
		"country_id":"Any",
		"tamil_school_id":"Any",
		"add":"Search",
	}
	res = sess.post(
		students_url,
		data = payload,
	)
	data = get_data_table("student_details")


def get_competition_details(sess, state_id, division_id= "",  competition_type_id="", competion_id=""):
	assert competion_id != "" or (division_id !="" and competition_type_id !=""), "have to give either competion id or competiion type id with division id"
	competitions_url = "http://www.tamilcompetition.org.au/admin/student_competitions/searchcomp/"
	payload = {
		"state_id": state_id,
		"year": "2018",
		"division_id": "Any",
		"gender": "2",
		"student_no":"",
		"competition_type_id": "Any",
		"competition_id": "Any",
		"tamil_school_id":"Any",
		"start_dob":"",
		"end_dob":"",
		"add":"Search",
	}
	if competion_id != "":
		payload["competition_id"] = competion_id
	else:
		payload["competition_type_id"] = competition_type_id
		payload["division_id"] = division_id

	res = sess.post(
		competitions_url,
		data = payload,
	)
	data = get_data_table(sess, "student_competitions")
	return data

def get_exam_details(sess, state_id= "6", competion_id=""):
	competitions_url = "http://www.tamilcompetition.org.au/admin/exam/searchcomp/"
	payload = {
		"state_id": state_id,
		"year": "2018",
		"division_id": "Any",
		"exam_category_id": "1",
		"location_id": "Any",
		"competition_id": "Any",
		"exam_id":"Any",
		"search_exam":"Search",
	}
	res = sess.post(
		competitions_url,
		data = payload,
	)
	data = get_data_table(sess, "exam")
	exam_details = {}
	for exam in data:
		exam_code = exam[0]
		exam_e = exam[1]
		exam_t = exam[2]
		comp = exam[3]
		exam_details[exam_e] = {'code': exam_code, "exam_t": exam_t, "exam_e": exam_e, "comp": comp}
	return exam_details


def split_data(comp_data):
	comp_sets = {}
	for comp in comp_data:
		exam_e = comp[1]
		comp_sets[exam_e] = comp_sets.get(exam_e, [])
		comp_sets[exam_e].append(comp)
	return comp_sets

# sess = init_sess()
COMP_DETAILS, COMP_DETAILS_DICT = get_comp_details()
def write_competition_spreadsheet(sess, xls_wb= OUTPUT_XLS):
	exam_details = get_exam_details(sess, state_id=STATE_ID)
	wb = xlsxwriter.Workbook(xls_wb)
	left_image_path = os.path.join(MEDIA_ROOT,   "left_src.jpg")
	right_image_path = os.path.join(MEDIA_ROOT,   "right_src.jpg")
	## comps
	comp_title1_format = wb.add_format({
	'font_name': "Bamini",
	'bold': 2,
    'align': 'center',
	'font_size': 26, 
    'valign': 'vcenter'})
	comp_title1_height = 45

	comp_title2_format = wb.add_format({
	# 'font_name': "Bamini",
	'font_name': "Calibri (Body)",
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
	'top':2,
	'left': 1,
	'right': 1,
    'align': 'left',
	'font_size': 14, 
    'valign': 'vcenter'})
	comp_header_height = 30

	comp_row_format = wb.add_format({
	'font_name': "Calibri (Body)",
	'border':1,
	'font_size': 14,
	'align': 'left'})
	comp_row_height = 25

	comp_header_right_border = wb.add_format({
	'font_name': "Calibri (Body)",
	'bg_color': '#ebf0df',
	'bold': 1,
	'bottom': 2,
	'top':2,
	'left': 1,
	'right': 2,
    'align': 'left',
	'font_size': 14, 
    'valign': 'vcenter'})

	## stats
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

	## common formats
	tamil_format = wb.add_format({
	'font_name': "Calibri (Body)",
	'font_size': 16,
	'border':1,
	'align': 'left'})

	tamil_header = wb.add_format({
	'font_name': "Bamini",
	'bold': 1,
	'font_size': 16,
	'valign': 'vcenter',
	'bottom': 2,
	'top':2,
	'left': 1,
	'right': 1,
	'bg_color': '#ebf0df',
	'align': 'left'})

	#setting up stats 
	ws_stats = wb.add_worksheet("stats")
	ws_stats.merge_range('A1:J1', "Participants Count", stats_title_format)
	ws_stats.write_row(1, 0, ["Comp-code", "Desc", "Count", "Time(S)", "Admin(S)", "Total Time (S)", "Judge Buf(S)", "Total(S)", "Total(M)", "Comment"], stats_header_format)
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
	comp_data_raw = get_competition_details(sess, state_id=STATE_ID, competion_id= "Any")
	comp_data_sets = split_data(comp_data_raw)
	for exam_e in sorted(comp_data_sets):
		if exam_e not in exam_details:
			print("Exam not found")
			print exam_e
			continue
		comp_data = comp_data_sets[exam_e]
		exam_code = exam_details[exam_e]['code']
		comp_code= exam_details[exam_e]['comp']
		comp = COMP_DETAILS_DICT[comp_code]
		code = comp["Comp Code"]
		comp_type = comp["Comp Type"]
		comp_time = comp["Time"]
		comp_admin = comp["Admin"]
		judge_buf = comp["Comp Time"]

		ws = wb.add_worksheet(exam_code)

		comp_count = len(comp_data)
		comp_total = (comp_time + comp_admin) * comp_count
		comp_total_sec = comp_total + judge_buf
		comp_total_min = float('{:0.2f}'.format(comp_total_sec/60.0))
		row_data = [exam_code, exam_e, comp_count, comp_time, comp_admin, comp_total,  judge_buf, comp_total_sec, comp_total_min, "" ]
		
		# writing stats info
		ws_stats.write_row(stats_row, 0, row_data, stats_row_format)
		ws_stats.set_row(stats_row, 25)
		stats_row +=1
		
		# setting up oral and written details
		if comp_type.lower() == "oral":
			oral_comps[exam_code] = (comp_count, comp_total_min)
		else:
			written_comps[exam_code] = (comp_count, comp_total_min)
		
		#adding title images

		ws.insert_image('A1', left_image_path, {'x_offset': 20, 'y_offset': 10})
		ws.insert_image('F1', right_image_path, {'x_offset': -20, 'y_offset': 10})

		#  titile 1 for comp sheet
		title1 = "jkpo; Cf;Ftpg;Gg; Nghl;b - 2018"
		ws.merge_range('A1:F1', title1, comp_title1_format)
		ws.set_row(0, comp_title1_height)
		#  titile 2 for comp sheet
		# title2 = unicode2bamini(exam_details[exam_e]["exam_t"])
		title2 = exam_details[exam_e]["exam_t"]
		ws.merge_range('A2:F2', title2, comp_title2_format)
		ws.set_row(1, comp_title2_height)
		#  titile 3 for comp sheet
		title3 = exam_code
		ws.merge_range('A3:F3', title3, comp_title3_format)
		ws.set_row(2, comp_title3_height)

		# header for comp sheet
		ws.write_row(3, 0, ["Number", "Student ID", "Student Name", "", "Payment", "Comments"], comp_header_format)
		ws.write("D4", "khzthpd; ngaH", tamil_header)
		ws.write("F4", "Comments", comp_header_right_border)
		ws.set_row(3, comp_header_height)
		header_rows = 4
		comp_data = 	sorted(comp_data, key = lambda  x: x[6].replace("<br>", " "))
		for row, r_data in enumerate(comp_data):
			cur_row = row + header_rows
			std_id = cleanhtml(r_data[0])
			e_name = r_data[6].replace("<br>", " ")
			t_name = unicode2bamini(r_data[7].replace("<br>", " "))
			t_name = r_data[7].replace("<br>", " ")
			paid = r_data[18]
			ws.write_row(cur_row , 0, ["", std_id, e_name, t_name, paid, ""], comp_row_format)
			ws.write("D{:0d}".format(cur_row+1), t_name, tamil_format)
			ws.set_row(cur_row, comp_row_height)

		ws.set_column('A:B', 11)
		ws.set_column('C:C', 35)
		ws.set_column('D:D', 55)
		ws.set_column('E:E', 15)
		ws.set_column('F:F', 15)

	stats_ref_range = "stats!$A${:d}:$J${:d}".format(3, stats_row + 1)
	total_time_col = 9

	add_time_table(wb, ws_oral_time_table, oral_start_time, oral_comps,  stats_ref_range, total_time_col, comp_type="oral")
	add_time_table(wb, ws_written_time_table, written_start_time, written_comps, stats_ref_range, total_time_col, comp_type="written")
	
	wb.close()
	return OUTPUT_XLS


# get_student_details("L")
# get_competition_details(division_id= "L", competition_type_id="P")
# get_comp_details()
if __name__ == "__main__":
	username = "sabesan"
	password = "Sabesan4NSW"

        sess = init_sess(username, password, state)
	write_competition_spreadsheet()
