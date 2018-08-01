import os, sys
import requests
import json
import xlsxwriter
import re
import xlrd
import string
from write_timetable import add_time_table
# from lxml import html


DIVISION_IDS = {"P": "15", "B": "14", "L": "12", "I" :"10" , "S": "7", "AdS": "4", "Y" : "3", "AY": "18", "All": "Any"}
COMPETITION_TYPE_IDS = {"P": "1", "S": "2", "V": "4", "SpP-A": "9", "SpP-T": "8", "W": "3", "A": "5", "Q" : "7", "D": "6", "All": "Any"}

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPET_XLS = os.path.join(FILE_DIR, "competition_details_2018.xlsx")
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
		comp_ids[data["Comp Code"]] = data["Comp Id"]
	return comp_details, comp_ids

def init_sess():
	payload = {
		"login": "yoges", 
		"password": "Yoges", 
	}
	login_url = "http://www.tamilcompetition.org.au/admin/login/run"
	sess = requests.session()

	res = sess.post(
		login_url, 
		data = payload,
	)

	res.raise_for_status()
	return sess

COMP_DETAILS, COMP_IDS = get_comp_details()

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def get_data_table(sess, type_key="student_details"):
	max_len = 500
	types = {"student_details" :{
					"url": "http://www.tamilcompetition.org.au/admin/student_details/get_data_table?draw=1&",
					"number_of_columns" : 15
					},
			"student_competitions" :{
					"url": "http://www.tamilcompetition.org.au/admin/student_competitions/get_data_table?draw=1&",
					"number_of_columns" : 18
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

def get_student_details(sess, division_id= "All"):
	students_url = "http://www.tamilcompetition.org.au/admin/student_details/searchcomp/"
	payload = {
		"state_id":6,
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


def get_competition_details(sess, division_id= "", competition_type_id="", competion_id=""):
	assert competion_id != "" or (division_id !="" and competition_type_id !=""), "have to give either competion id or competiion type id with division id"
	competitions_url = "http://www.tamilcompetition.org.au/admin/student_competitions/searchcomp/"
	payload = {
		"state_id": "6",
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

def split_data(comp_data):
	comp_g = []
	comp_b = []
	for comp in comp_data:
		if comp[6] == "Male":
			comp_b.append(comp)
		else:
			comp_g.append(comp)
	return comp_b, comp_g


def write_competition_spreadsheet(xls_wb="test.xlsx"):
	oral_time_table = "Time Table 22-07-2018"
	comp_th = 15
	sess = init_sess()
	wb = xlsxwriter.Workbook(xls_wb)
	title_format = wb.add_format({
    'bold': 1,
    'bottom': 2,
	'font_size': 22,
    'align': 'center',
    'valign': 'vcenter'})

	header_format = wb.add_format({
    'bold': 1,
    'bottom': 2,
    'align': 'center',
	'font_size': 14, 
    'valign': 'vcenter'})

	row_format = wb.add_format({
	'font_size': 12,
	'align': 'left'})

	tamil_format = wb.add_format({
	'font_size': 10,
	'align': 'left'})

	#setting up stats 
	ws_stats = wb.add_worksheet("stats")
	
	# ws for time table oral
	oral_start_time = "1:30 PM"
	written_start_time = "9:30 AM"
	ws_oral_time_table = wb.add_worksheet("Time Table 22-07-2018")
	ws_written_time_table = wb.add_worksheet("Time Table 05-08-2018")

	ws_stats.merge_range('A1:J1', "Participants Count", title_format)
	
	ws_stats.write_row(1, 0, ["Comp-code", "Desc", "Count", "Time(S)", "Admin(S)", "Total Time (S)", "Judge Buf(S)", "Total(S)", "Total(M)", "Comment"], header_format)
	ws_stats.set_column('A:A', 20)
	ws_stats.set_column('B:B', 30)
	ws_stats.set_column('C:C', 15)
	ws_stats.set_column('D:J', 15)
	comp_row = 2
	oral_comps = {}
	written_comps = {}
	for comp in COMP_DETAILS[:4]:
		code = comp["Comp Code"]
		comp_type = comp["Comp Type"]
		comp_data_raw = get_competition_details(sess, competion_id= comp["Comp Id"])
		if len(comp_data_raw) > comp_th:
			comp_b, comp_g = split_data(comp_data_raw)
			comp_data_sets = [{'split': '-boys', 'data': comp_b},
							 {'split': '-girls', 'data': comp_g}
							]
		else:
			comp_data_sets = [{'split': '', 'data': comp_data_raw}
							]

		for comp_data_set in comp_data_sets:
			comp_data = comp_data_set["data"]
			split = comp_data_set['split']
			sheet_code = code + split
			ws = wb.add_worksheet(sheet_code)
			comp_desc = comp['Comp Eng'] + split
			comp_time = comp["Time"]
			comp_admin = comp["Admin"]
			judge_buf = comp["Comp Time"]
			comp_count = len(comp_data)
			comp_total = (comp_time + comp_admin) * comp_count
			comp_total_sec = comp_total + judge_buf
			comp_total_min = float('{:0.2f}'.format(comp_total_sec/60.0))
			row_data = [sheet_code, comp_desc, comp_count, comp_time, comp_admin, comp_total,  judge_buf, comp_total_sec, comp_total_min, "" ]
			# writing stats info
			ws_stats.write_row(comp_row, 0, row_data, row_format)
			ws_stats.set_row(comp_row, 25)
			comp_row +=1
			if comp_type.lower() == "oral":
				oral_comps[sheet_code] = (comp_count, comp_total_min)
			else:
				written_comps[sheet_code] = (comp_count, comp_total_min)

			title = comp['Comp Tamil'] + " ({:s}){:s}".format(code, split)
			ws.merge_range('A1:E1', title, title_format)
			ws.write_row(1, 0, ["Index Num", "Std ID", "Full Name (Eng)", "Full Name (Tamil)", "Date of Birth"], header_format)
			for row, r_data in enumerate(comp_data):
				std_id = cleanhtml(r_data[0])
				e_name = r_data[6].replace("<br>", " ")
				t_name = r_data[7].replace("<br>", " ")
				dob = r_data[8]
				ws.write_row(row+2, 0, ["", std_id, e_name, t_name, dob], row_format)
				ws.set_row(row+2, 25)
			ws.set_row(0, 35)
			ws.set_row(1, 28)
			ws.set_column('A:B', 11)
			ws.set_column('C:C', 25)
			ws.set_column('D:D', 35, tamil_format)
			ws.set_column('E:E', 15)

	stats_ref_range = "stats!$A${:d}:$J${:d}".format(3, comp_row + 1)
	total_time_col = 9

	add_time_table(wb, ws_oral_time_table, oral_start_time, oral_comps,  stats_ref_range, total_time_col, comp_type="oral")
	add_time_table(wb, ws_written_time_table, written_start_time, written_comps, stats_ref_range, total_time_col, comp_type="written")
	
	wb.close()


# get_student_details("L")
# get_competition_details(division_id= "L", competition_type_id="P")
# get_comp_details()
if __name__ == "__main__":
	write_competition_spreadsheet()
