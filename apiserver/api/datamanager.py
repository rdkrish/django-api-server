import json

from models import Account, PhoneNumber
from cachemanager import CacheManager

cachemanager = CacheManager()

class DataManager:

  def __init__(self):
    # Set of validations that needs to be verified for all the input data
    self.validations = {
      'from': {'min_length': 6, 'max_length': 16},
      'to': {'min_length': 6, 'max_length': 16},
      'text': {'min_length': 1, 'max_length': 120}
    }

  def validate_parameter(self, input_data):
    # Loop through the keys and check if they are valid or not
    for key in ['from', 'to', 'text']:
      value = input_data[key] if key in input_data else None
      min_length = self.validations[key]['min_length']
      max_length = self.validations[key]['max_length']
      if not ((type(value) == str or type(value) == unicode) \
          and len(value) >= min_length and len(value) <= max_length):
        # input data is invalid, return the key that is invalid
        return key

  def check_parameter_missing(self, input_data):
    # Loop through the keys and check if they are present in the input data
    for key in ['from', 'to', 'text']:
      if key not in input_data:
        # If key is not found, then return the missing key
        return key

  def input_validation(self, input_data):
    # Check if there are any missing parameters in the request data
    missing_parameter = self.check_parameter_missing(input_data)
    if missing_parameter is not None:
      # Missing parameter found, return appropriate error message
      return missing_parameter + ' is missing'
    # Check if the data is valid or not
    invalid_parameter = self.validate_parameter(input_data)
    if invalid_parameter is not None:
      # Invalid parameter found, return appropriate error message
      return invalid_parameter + ' is invalid'
    # If all the parameters are found and are valid, then do not return error message
    return ''

  def check_authorized(self, number, account_id):
    # Check if the user trying to access the phone number has access to it or not
    phone = PhoneNumber.objects.filter(number=number, account_id=account_id).count()
    if phone == 0:
      return False
    return True

  def add_key_to_redis(self, input_data):
    # Create a unique key combination for the 'from' and 'to' parameters
    key_from_to = input_data['from'] + '_' + input_data['to']
    # Check if the text parameter is 'STOP' or variations of it
    # and the unique combination is present in redis or not
    if input_data['text'].strip() == 'STOP' and \
      cachemanager.get(key_from_to) is None:
      # If true, then add the key to redis and set the time to expire for 4 hours
      expire_time = 60 * 60 * 4 # 4 hours in seconds
      cachemanager.setex(key_from_to, expire_time, key_from_to)

  def inbound_sms(self, input_data, user):
    output = {
      'message': '', 'error': ''
    }
    try:
      # Validate the input data
      output['error'] = self.input_validation(input_data)
      if len(output['error']) > 0:
        # if there are missing or invalid parameter, then return the error message
        return output
      # Check if the phone number accessible to the authenticated user
      if self.check_authorized(input_data['to'], user.id) is False:
        # If phone_number not accessible to the authenticated user,
        # then return an error message
        output['error'] = 'to parameter not found'
        return output
      self.add_key_to_redis(input_data)
      # If all the conditions are satisfied, then send message back to the client
      output['message'] = 'inbound sms ok'
    except:
      output['error'] = 'unknown failure'
    return output

  def increment_and_get_counter(self, input_data):
    # If the request counter is not set, then set the request counter
    # with expire time as 24 hours
    if cachemanager.get(input_data['from']) is None:
      cachemanager.setex(input_data['from'], 60 * 60 * 24, 0)
    # Increment the counter of the requests from 'from' number
    return cachemanager.incr(input_data['from'])

  def outbound_sms(self, input_data, user):
    output = {
      'message': '', 'error': ''
    }
    try:
      # Validate the input data
      output['error'] = self.input_validation(input_data)
      if len(output['error']) > 0:
        # if there are missing or invalid parameter, then return the error message
        return output
      # Check if the phone number accessible to the authenticated user
      if self.check_authorized(input_data['from'], user.id) is False:
        # If phone_number not accessible to the authenticated user,
        # then return an error message
        output['error'] = 'from parameter not found'
        return output
      # Check if the sms request is blocked due to the STOP text sent in inbound sms request
      if cachemanager.get(input_data['from'] + '_' + input_data['to']):
        # If the communication is STOPPED, then send error message
        output['error'] = 'sms from {} to {} blocked by STOP request'.format(
          input_data['from'], input_data['to'])
        return output
      request_count = self.increment_and_get_counter(input_data)
      # Check if the API request limit for the 'from' phone number is reached
      if request_count >= 50:
        output['error'] = 'limit reached for from {}'.format(input_data['from'])
      else:
        # If all the conditions are satisfied, then send message back to the client
        output['message'] = 'outbound sms ok'
    except:
      output['error'] = 'unknown failure'
    return output
