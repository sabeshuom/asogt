"""
Login views
"""

import json

from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from django.contrib.auth.models import User

# from rest_framework.response import Response
# from tokenapi.views import token_new, token_generator
from datetime import datetime, timedelta
from django.utils import timezone
 
import logging
logger = logging.getLogger('')


# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

@csrf_exempt
def is_authenticated(request):
    authenticated = False
    if (request.user.is_authenticated()):
        if((timezone.now()-request.user.last_login) > timedelta(days=2)):
            print("Logging out the user")
            auth_logout(request)
        else:
            print("Logged in less than one minute")
            authenticated = True
    else:
        print("Not authenticated")
    return HttpResponse(json.dumps({'is_authenticated': authenticated}), content_type="application/json")

@csrf_exempt
def login_ajax(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # success_response = HttpResponse(json.dumps({'success': True,
                #                                             'user': user.pk,
                #                                             'token': token_generator.make_token(request.user)}),
                #                                 content_type="application/json")
                success_response = HttpResponse(json.dumps({'success': True,
                                                            'user': user.pk}),
                                                content_type="application/json")
                return success_response
            else:
                # Return a 'disabled account' error message
                # error = 'Account is not active. Please contact '+settings.DEFAULT_FROM_EMAIL
                return HttpResponse(
                    json.dumps({'success': False, 'reason': 1}), content_type="application/json"
                )
        else:
            # Return an 'invalid login' error message.
            return HttpResponse(
                json.dumps({'success': False, 'reason': 0}),
                content_type="application/json"
            )
            # error = "Invalid login. Please try again."

    # Probably never happens as it will return 401 for not having csrf
    return HttpResponse(
        json.dumps({'success': False, 'reason': -1}),
        content_type="application/json"
    )

def logout_ajax(request):
    auth_logout(request)
    return HttpResponse(
        json.dumps({'success': True, 'reason': 0}),
        content_type="application/json"
    )

# @api_view(['GET', 'POST', ])
# def login(request):
#     print(request)
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             LOGGER.info('login user %s', user)
#             auth_login(request, user)
#             filter_filename = request.POST.get('filter')
#             if filter_filename:
#                 url = request.POST.get('next').rstrip(
#                     '/') + '/?filter=' + filter_filename
#                 return HttpResponseRedirect(url)
#             else:
#                 return HttpResponseRedirect(request.POST.get('next'))
#         else:
#             # Return an 'invalid login' error message.
#             return Response(
#                 json.dumps({'success': False, 'reason': 0}),
#                 content_type="application/json"
#             )
#             # error = "Invalid login. Please try again."

#     # Probably never happens as it will return 401 for not having csfr
#     return Response(
#         json.dumps({'success': False, 'reason': -1}),
#         content_type="application/json"
#     )
