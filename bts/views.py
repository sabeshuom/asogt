from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.template import Template
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
from io import BytesIO

from django.core.mail import EmailMessage

from competition.view_utils import competition_details, results, student_details
from asogt.settings import MEDIA_ROOT, MEDIA_URL

# Create your views here.
from django.http import HttpResponse
from asogt.settings import MEDIA_ROOT
import threading

def index(request):
    return render(request, 'bts/registration.html')


class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list, attachments):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.attachments = attachments
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMessage(self.subject, self.html_content, "BTS Enrolment", self.recipient_list)
        msg.content_subtype = "html"
        for attachemnt in self.attachments:
            msg.attach_file(attachemnt)
        msg.send()

@csrf_exempt
def submit_registration(request):
    request_data = json.loads(request.body)
    doc_data = generate_doc_data(request_data)
    attachments = generate_docs(doc_data)
    subject = "BTS Enroment - " + str(request_data["year"])
    html_content = 'PLease find the attached enrolment form.'
    recipient_list = ["sabeshuom@gmail.com"]
    EmailThread(subject, html_content, recipient_list, attachments).start()
    return HttpResponse(json.dumps({'Sucess': True}))

def generate_docs(doc_data):
    from docxtpl import DocxTemplate
    template_path = os.path.join(MEDIA_ROOT, "bts/BTS_online_enrolment_template.docx")
    doc = DocxTemplate(template_path)
    attachments = []
    for student_doc_data in doc_data:
        context = student_doc_data
        fname = "BTS_enrolment_form_2020_" + context["student_surname_eng"] + "_" + context["student_givenname_eng"] + ".docx"
        fpath = os.path.join(MEDIA_ROOT, "bts_uploaded_forms", fname)
        doc.render(context)
        doc.save(fpath)
        attachments.append(fpath)
    return attachments

def generate_doc_data(data):
    student_data = [{} for ind in range(data['no_of_students'])]
    common_data = {}
    form_data = data["form_data"]
    common_data["enrolment_year"] = str(data["year"])
    for key in form_data:
        if "student" not in key:
            common_data[key] =  form_data[key]
        else:
            student_split = key.split("_")
            student_ind  = int(student_split[1])-1
            student_key = "student_" + str("_".join(student_split[2:]))
            student_data[student_ind][student_key] = str(form_data[key])
    
    for ind in range(data['no_of_students']):
        student_data[ind].update(common_data)
    return student_data
    




