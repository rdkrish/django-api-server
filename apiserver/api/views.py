from django.shortcuts import render
from django.http import JsonResponse

# from rest_framework import status
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
# from rest_framework.response import Response

import json

from datamanager import DataManager

datamanager = DataManager()

# Create your views here.
@api_view(['GET', 'POST'])
def inbound_sms(request):
  input_data = json.loads(request.body)
  output = datamanager.inbound_sms(input_data)
  return JsonResponse(output)

@api_view(['GET', 'POST'])
def outbound_sms(request):
  input_data = json.loads(request.body)
  output = datamanager.outbound_sms(input_data)
  return JsonResponse(output)
