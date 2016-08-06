import json

from models import Account, PhoneNumber

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
      else:
        output['message'] = 'outbound sms ok'
    except:
      output['error'] = 'unknown failure'
    return output
