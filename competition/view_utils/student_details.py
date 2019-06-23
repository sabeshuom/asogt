
from core.data_utils import init_sess,\
    get_student_details


def get_formatted_student_details(state, year, username, password):
    sess = init_sess(username, password)
    students = get_student_details(sess, state=state, year=year)
    headers = ["StdNo", "IndNo", "Name (T)", "Name (E)", 'DOB', "Division", 'Gender', 'Phone', 'Email']
    data = []
    for r in students:
        data.append([r.std_no, r.ind_no, r.name_t, r.name_e, r.dob, r.division_t, r.gender, r.phone, r.email])
    return data, headers
