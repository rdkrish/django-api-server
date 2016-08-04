import json


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

  def input_validation(self, sms_from, sms_to, sms_text, output):
    if sms_from is None:
      output['error'] = 'from is missing'
    elif sms_to is None:
      output['error'] = 'to is missing'
    elif sms_text is None:
      output['error'] = 'text is missing'
    elif not self.is_value_validated(sms_from, self.validations['from']['min_length'],
        self.validations['from']['max_length']):
      output['error'] = 'from is invalid'
    elif not self.is_value_validated(sms_to, self.validations['to']['min_length'],
        self.validations['to']['max_length']):
      output['error'] = 'to is invalid'
    elif not self.is_value_validated(sms_text, self.validations['text']['min_length'],
        self.validations['text']['max_length']):
      output['error'] = 'text is invalid'

  def inbound_sms(self, sms_from, sms_to, sms_text, output):
    try:
      self.input_validation(sms_from, sms_to, sms_text, output)
      if len(output['error']) > 0:
        return
      output['message'] = 'Input fields are all validated'
    except:
      output['error'] = 'unknown failure'

  def outbound_sms(self, sms_from, sms_to, sms_text, output):
    try:
      self.input_validation(sms_from, sms_to, sms_text, output)
      if len(output['error']) > 0:
        return
      output['message'] = 'Input fields are all validated'
    except:
      output['error'] = 'unknown failure'
