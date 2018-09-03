from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.template import Template
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from io import BytesIO

from view_utils import per_exam_details, results_for_certificate, results_for_trophy, results_for_book
from asogt.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.
from django.http import HttpResponse


def index(request):
    return render(request, 'asogt.html')


def students(request):
    return render(request, 'students.html')


def competitions(request):
    return render(request, 'competitions.html')


def results(request):
    return render(request, 'results.html')


@csrf_exempt
def get_student_details(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=204)
    else:
        json_data = json.loads(request.body)
        state = json_data["state"]
        year = json_data["year"]
        req_format = json_data["format"]

        # if state == "QLD":
        #     username = "yoges"
        #     password = "Yoges"
        # if state == "NSW":
        username = "sabesan"
        password = "Sabesan4NSW"
        output = BytesIO()
        per_exam_details.export_to_excel(output, state, year, username, password)
        output.seek(0)
        response = HttpResponse(output.read(
        ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response


@csrf_exempt
def get_results(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=204)
    else:
        json_data = json.loads(request.body)
        state = json_data["state"]
        year = json_data["year"]
        req_format = json_data["format"]

        # if state == "QLD":
        #     username = "yoges"
        #     password = "Yoges"
        # if state == "NSW":
        username = "sabesan"
        password = "Sabesan4NSW"
        output = BytesIO()
        if req_format.lower() == "certificate":
            results_for_certificate.export_to_excel(output, state, year, username, password)
        if req_format.lower() == "trophy":
            results_for_trophy.export_to_excel(output, state, year, username, password)
        if req_format.lower() == "book":
            results_for_book.export_to_excel(output, state, year, username, password)

        output.seek(0)
        response = HttpResponse(output.read(
        ), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response