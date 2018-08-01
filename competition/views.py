from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.template import Template
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from io import BytesIO

from utils.tamil_comp import write_competition_spreadsheet, init_sess
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
def get_per_exam_details(request):
    if not request.user.is_authenticated():
        return HttpResponse(status=204)
    else:
        state = json.loads(request.body)["state"]
        if state == "QLD":
            username = "yoges"
            password= "Yoges"
        if state == "NSW":
            username = "sabesan"
            password = "Sabesan4NSW"
        output = BytesIO()
        sess = init_sess(username, password, state)
        write_competition_spreadsheet(sess, output)
        output.seek(0)
        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        return response
