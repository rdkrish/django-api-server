from rest_framework import authentication
from rest_framework import exceptions

from models import Account

class ApiAuthentication(authentication.BasicAuthentication):
  def authenticate(self, request):
    username = request.META.get('HTTP_X_USERNAME')
    auth_id = request.META.get('HTTP_X_AUTHID')
    if username is None or auth_id is None:
      raise exceptions.PermissionDenied('No such user')
    try:
      account = Account.objects.get(username=username, auth_id=auth_id)
      if account.id:
        return (account, None)
    except:
      raise exceptions.PermissionDenied('No such user')
