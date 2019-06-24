from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.template import Template
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from io import BytesIO

from competition.view_utils import competition_details, results, student_details
from asogt.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.
from django.http import HttpResponse

ASOGT_USERNAME = "sabesan"
ASOGT_PASSWORD = "Sabesan4NSW"


def index(request):
    return render(request, 'asogt.html')


def students_page(request):
    return render(request, 'students.html')


def competitions_page(request):
    return render(request, 'competitions.html')


def results_page(request):
    return render(request, 'results.html')


@csrf_exempt
def get_competition_details(request):
    json_data = json.loads(request.body)
    state = json_data["state"]
    year = json_data["year"]

    if state == "National":
        exam_category = "National"
        state = "All"
    else:
        exam_category = ["State", "Final"]
    std_data, headers = competition_details.get_formatted_details(
        state, year, exam_category, ASOGT_USERNAME, ASOGT_PASSWORD)
    return HttpResponse(json.dumps({'headers': headers, 'std_data': std_data}))


@csrf_exempt
def export_competition_details(request):
    json_data = json.loads(request.body)
    state = json_data["state"]
    year = json_data["year"]
    req_format = json_data["format"]

    if state == "National":
        exam_category = "National"
        state = "All"
    else:
        exam_category = ["State", "Final"]

    output = BytesIO()
    competition_details.export_to_excel(
        output, state, year, exam_category, ASOGT_USERNAME, ASOGT_PASSWORD)
    output.seek(0)
    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response

# Content types reference:
# https://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc


@csrf_exempt
def get_results(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=204)
    else:
        json_data = json.loads(request.body)
        state = json_data["state"]
        year = json_data["year"]
        if state == "National":
            exam_category = "National"
            state = "All"
        else:
            exam_category = ["State", "Final"]
        
        data, headers = results.get_formatted_results(state, year, exam_category,  ASOGT_USERNAME, ASOGT_PASSWORD)
        return HttpResponse(json.dumps({'headers': headers, 'result_data': data}))


@csrf_exempt
def get_student_details(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=204)
    else:
        json_data = json.loads(request.body)
        state = json_data["state"]
        year = json_data["year"]        
        data, headers = student_details.get_formatted_student_details(state, year, ASOGT_USERNAME, ASOGT_PASSWORD)
        return HttpResponse(json.dumps({'headers': headers, 'students_data': data}))


@csrf_exempt
def export_student_details(request):
    json_data = json.loads(request.body)
    state = json_data["state"]
    year = json_data["year"]
    req_format = json_data["format"]

    if state == "National":
        exam_category = "National"
        state = "All"
    else:
        exam_category = ["State", "Final"]

    output = BytesIO()
    student_details.export_to_excel(
        output, state, year, exam_category, ASOGT_USERNAME, ASOGT_PASSWORD)
    output.seek(0)
    response = HttpResponse(output.read(
    ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response

@csrf_exempt
def export_results(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=204)
    else:
        json_data = json.loads(request.body)
        state = json_data["state"]
        year = json_data["year"]
        req_format = json_data["format"]
        if state == "National":
            exam_category = "National"
            state = "All"
        else:
            exam_category = ["State", "Final"]

        output = BytesIO()
        content_type, output = results.export_results(req_format, output, state, year,
                               exam_category,  ASOGT_USERNAME, ASOGT_PASSWORD)

        output.seek(0)
        response = HttpResponse(output.read(), content_type=content_type)
        return response

    
