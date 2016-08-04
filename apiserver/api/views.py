from django.shortcuts import render
from django.http import JsonResponse

# from rest_framework import status
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
# from rest_framework.response import Response

from datamanager import DataManager

datamanager = DataManager()

# Create your views here.
@api_view(['GET', 'POST'])
def inbound_sms(request):
  sms_from = request.POST['from'] if 'from' in request.POST else None
  sms_to = request.POST['to'] if 'to' in request.POST else None
  sms_text = request.POST['text'] if 'text' in request.POST else None
  output = {
    'message': '',
    'error': ''
  }
  datamanager.inbound_sms(sms_from, sms_to, sms_text, output)
  return JsonResponse(output)

@api_view(['GET', 'POST'])
def outbound_sms(request):
  sms_from = request.POST['from'] if 'from' in request.POST else None
  sms_to = request.POST['to'] if 'to' in request.POST else None
  sms_text = request.POST['text'] if 'text' in request.POST else None
  output = {
    'message': '',
    'error': ''
  }
  datamanager.outbound_sms(sms_from, sms_to, sms_text, output)
  return JsonResponse(output)
