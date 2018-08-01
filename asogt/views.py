from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.template import Template
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from io import BytesIO

# Create your views here.
from django.http import HttpResponse

def index(request):
   return render(request, 'index.html')