from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

import json

from authentication import ApiAuthentication
from datamanager import DataManager

datamanager = DataManager()

@api_view(['POST'])
@authentication_classes([ApiAuthentication])
def inbound_sms(request):
  input_data = json.loads(request.body)
  output = datamanager.inbound_sms(input_data, request.user)
  return Response(output)

@api_view(['POST'])
@authentication_classes([ApiAuthentication])
def outbound_sms(request):
  input_data = json.loads(request.body)
  output = datamanager.outbound_sms(input_data, request.user)
  return Response(output)
