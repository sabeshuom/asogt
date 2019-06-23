
from competition.view_utils import results_for_certificate, results_for_trophy, results_for_book
from core.data_utils import init_sess,\
    get_results


def get_formatted_results(state, year, exam_category, username, password):
    sess = init_sess(username, password)
    results = get_results(sess, state=state, year=year, competition="All", exam_category=exam_category)
    headers = ["StdNo", "Name (T)", "Name (E)", 'Exam', "Competition", 'Grade', 'Award']
    data = []
    for r in results:
        data.append([r.std_no, r.name_t, r.name_e, r.exam_e, r.comp_t, r.grade, r.award])
    return data, headers


def export_results(req_format, output, state, year, exam_category,  ASOGT_USERNAME, ASOGT_PASSWORD):
    content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    if req_format.lower() == "certificate":
        results_for_certificate.export_to_excel(
            output, state, year, exam_category,  ASOGT_USERNAME, ASOGT_PASSWORD)
    if req_format.lower() == "trophy":
        results_for_trophy.export_to_excel(
            output, state, year, exam_category, ASOGT_USERNAME, ASOGT_PASSWORD)
    if req_format.lower() == "book excel":
        results_for_book.export_to_excel(
            output, state, year, exam_category, ASOGT_USERNAME, ASOGT_PASSWORD)
    if req_format.lower() == "book word":
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        results_for_book.export_to_docx(
            output, state, year, exam_category, ASOGT_USERNAME, ASOGT_PASSWORD)
    return content_type, output
