import json

from models import Account, PhoneNumber
from cachemanager import CacheManager

cachemanager = CacheManager()

class DataManager:

  def __init__(self):
    self.validations = {
      'from': {'min_length': 6, 'max_length': 16},
      'to': {'min_length': 6, 'max_length': 16},
      'text': {'min_length': 1, 'max_length': 120}
    }

  def is_value_validated(self, value, min_length, max_length):
    if (type(value) == str or type(value) == unicode) \
        and len(value) >= min_length and len(value) <= max_length:
      return True
    return False

  def input_validation(self, input_data, output):
    if 'from' not in input_data:
      output['error'] = 'from is missing'
    elif 'to' not in input_data:
      output['error'] = 'to is missing'
    elif 'text' not in input_data:
      output['error'] = 'text is missing'
    elif not self.is_value_validated(input_data['from'],
        self.validations['from']['min_length'],
        self.validations['from']['max_length']):
      output['error'] = 'from is invalid'
    elif not self.is_value_validated(input_data['to'],
        self.validations['to']['min_length'],
        self.validations['to']['max_length']):
      output['error'] = 'to is invalid'
    elif not self.is_value_validated(input_data['text'],
        self.validations['text']['min_length'],
        self.validations['text']['max_length']):
      output['error'] = 'text is invalid'

  def check_authorized(self, number, account_id):
    phone = PhoneNumber.objects.filter(number=number, account_id=account_id).count()
    if phone == 0:
      return False
    return True

  def inbound_sms(self, input_data, user):
    output = {
      'message': '', 'error': ''
    }
    try:
      self.input_validation(input_data, output)
      if len(output['error']) > 0:
        return output
      if self.check_authorized(input_data['to'], user.id) is False:
        output['error'] = 'to parameter not found'
      else:
        key_from_to = input_data['from'] + '_' + input_data['to']
        if input_data['text'].strip() == 'STOP' and \
          cachemanager.get(key_from_to) is None:
          # Add from and to the redis
          expire_time = 60 * 60 * 4 # 4 hours in seconds
          cachemanager.setex(key_from_to, expire_time, key_from_to)
        output['message'] = 'inbound sms ok'
    except:
      output['error'] = 'unknown failure'
    return output

  def outbound_sms(self, input_data, user):
    output = {
      'message': '', 'error': ''
    }
    try:
      self.input_validation(input_data, output)
      if len(output['error']) > 0:
        return output
      if self.check_authorized(input_data['from'], user.id) is False:
        output['error'] = 'from parameter not found'
      elif cachemanager.get(input_data['from'] + '_' + input_data['to']):
        output['error'] = 'sms from {} to {} blocked by STOP request'.format(
          input_data['from'], input_data['to'])
      else:
        # If the request counter is not set, then set the request counter
        # with expire time as 24 hours
        if cachemanager.get(input_data['from']) is None:
          cachemanager.setex(input_data['from'], 60 * 60 * 24, 0)
        # Increment the counter of the requests from 'from' number
        request_count = cachemanager.incr(input_data['from'])
        if request_count >= 50:
          output['error'] = 'limit reached for from {}'.format(input_data['from'])
        else:
          output['message'] = 'outbound sms ok'
    except:
      output['error'] = 'unknown failure'
    return output
