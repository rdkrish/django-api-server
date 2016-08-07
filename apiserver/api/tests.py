from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase

import json

from cachemanager import CacheManager
from configmanager import config

cachemanager = CacheManager()
client = APIClient()

# Create your tests here.
class APITests(APITestCase):
  def setUp(self):
    self.data = {'from': '4924195509198', 'to': '31297728125', 'text': 'sample test'}

  def test_http_request_type(self):
    # Test with get request, response status should be 405 method not allowed
    response = client.get('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    # Test with put request, response status should be 405 method not allowed
    response = client.put('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    # Test with delete request, response status should be 405 method not allowed
    response = client.delete('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    # Test with post request, response status should be 200 ok
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_inbound_parameter_missing(self):
    # Test if any of the parameters are missing
    # Check if server detects 'from' parameter missing
    response = client.post('/inbound/sms/',
      {'to': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from is missing')

    # Check if server detects 'to' parameter missing
    response = client.post('/inbound/sms/',
      {'from': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to is missing')

    # Check if server detects 'text' parameter missing
    response = client.post('/inbound/sms/',
      {'from': '4924195509198', 'to': '31297728125'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'text is missing')

  def test_inbound_from_parameter_invalid(self):
    # Test if any parameter is invalid
    # Check if server detects 'from' parameter as invalid
    # test for min length = 6
    response = client.post('/inbound/sms/',
      {'from': '49241', 'to': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from is invalid')

    # Check if server detects 'from' parameter as invalid
    # test for max_length = 16
    response = client.post('/inbound/sms/',
      {'from': '01234567890123456', 'to': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from is invalid')

  def test_inbound_to_parameter_invalid(self):
    # Check if server detects 'to' parameter as invalid
    # test for min length = 6
    response = client.post('/inbound/sms/',
      {'from': '012345678', 'to': '01234', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to is invalid')

    # Check if server detects 'to' parameter as invalid
    # test for max_length = 16
    response = client.post('/inbound/sms/',
      {'from': '0123456789012345', 'to': '01234567890123456', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to is invalid')

  def test_inbound_text_parameter_invalid(self):
    # Check if server detects 'text' parameter as invalid
    # test for min length = 1
    response = client.post('/inbound/sms/',
      {'from': '012345678', 'to': '01234568', 'text': ''},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'text is invalid')

    # Check if server detects 'text' parameter as invalid
    # test for max_length = 120
    text = 'sample test' * 11 # len(text) = 121
    response = client.post('/inbound/sms/',
      {'from': '0123456789012345', 'to': '0123456789012345', 'text': text},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'text is invalid')

  def test_outbound_parameter_missing(self):
    # Test if any of the parameters are missing
    # Check if server detects 'from' parameter missing
    response = client.post('/outbound/sms/',
      {'to': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from is missing')

    # Check if server detects 'to' parameter missing
    response = client.post('/outbound/sms/',
      {'from': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to is missing')

    # Check if server detects 'text' parameter missing
    response = client.post('/outbound/sms/',
      {'from': '4924195509198', 'to': '31297728125'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'text is missing')


  def test_outbound_from_parameter_invalid(self):
    # Test if any parameter is invalid
    # Check if server detects 'from' parameter as invalid
    # test for min length = 6
    response = client.post('/outbound/sms/',
      {'from': '49241', 'to': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from is invalid')

    # Check if server detects 'from' parameter as invalid
    # test for max_length = 16
    response = client.post('/outbound/sms/',
      {'from': '01234567890123456', 'to': '31297728125', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from is invalid')

  def test_outbound_to_parameter_invalid(self):
    # Check if server detects 'to' parameter as invalid
    # test for min length = 6
    response = client.post('/outbound/sms/',
      {'from': '012345678', 'to': '01234', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to is invalid')

    # Check if server detects 'to' parameter as invalid
    # test for max_length = 16
    response = client.post('/outbound/sms/',
      {'from': '0123456789012345', 'to': '01234567890123456', 'text': 'sample test'},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to is invalid')

  def test_outbound_text_parameter_invalid(self):
    # Check if server detects 'text' parameter as invalid
    # test for min length = 1
    response = client.post('/outbound/sms/',
      {'from': '012345678', 'to': '01234568', 'text': ''},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'text is invalid')

    # Check if server detects 'text' parameter as invalid
    # test for max_length = 120
    text = 'sample test' * 11 # len(text) = 121
    response = client.post('/outbound/sms/',
      {'from': '0123456789012345', 'to': '0123456789012345', 'text': text},
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'text is invalid')

  def test_inbound_valid_parameters(self):
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], 'inbound sms ok')
    self.assertEqual(response_data['error'], '')

  def test_inbound_stop_text(self):
    # Check if it accepts 'STOP' text and updates redis
    self.data['text'] = 'STOP'
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], 'inbound sms ok')
    self.assertEqual(response_data['error'], '')
    key_stored = self.data['from'] + '_' + self.data['to']
    redis_data = cachemanager.get(key_stored)
    self.assertEqual(redis_data, key_stored)
    ttl = cachemanager.ttl(key_stored)
    self.assertGreater(ttl, 0)
    self.assertLessEqual(ttl, 60 * 60 * 4) # ttl should not be greater than 4 hours

    # Check if it accepts 'STOP\r' text and updates redis
    self.data['text'] = 'STOP\r'
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], 'inbound sms ok')
    self.assertEqual(response_data['error'], '')
    key_stored = self.data['from'] + '_' + self.data['to']
    redis_data = cachemanager.get(key_stored)
    self.assertEqual(redis_data, key_stored)
    ttl = cachemanager.ttl(key_stored)
    self.assertGreater(ttl, 0)
    self.assertLessEqual(ttl, 60 * 60 * 4) # ttl should not be greater than 4 hours

    # Check if it accepts 'STOP\n' text and updates redis
    self.data['text'] = 'STOP\n'
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], 'inbound sms ok')
    self.assertEqual(response_data['error'], '')
    key_stored = self.data['from'] + '_' + self.data['to']
    redis_data = cachemanager.get(key_stored)
    self.assertEqual(redis_data, key_stored)
    ttl = cachemanager.ttl(key_stored)
    self.assertGreater(ttl, 0)
    self.assertLessEqual(ttl, 60 * 60 * 4) # ttl should not be greater than 4 hours

    # Check if it accepts 'STOP\r\n' text and updates redis
    self.data['text'] = 'STOP\r\n'
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], 'inbound sms ok')
    self.assertEqual(response_data['error'], '')
    key_stored = self.data['from'] + '_' + self.data['to']
    redis_data = cachemanager.get(key_stored)
    self.assertEqual(redis_data, key_stored)
    ttl = cachemanager.ttl(key_stored)
    self.assertGreater(ttl, 0)
    self.assertLessEqual(ttl, 60 * 60 * 4) # ttl should not be greater than 4 hours

  def test_inbound_to_not_in_phone_number(self):
    self.data['to'] = '441224980094'
    response = client.post('/inbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'to parameter not found')

  def test_outbound_from_not_in_phone_number(self):
    self.data['from'] = '441224980094'
    response = client.post('/outbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'], 'from parameter not found')

  def test_outbound_sms_stop_request(self):
    response = client.post('/outbound/sms/', self.data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'],
      'sms from {} to {} blocked by STOP request'.format(self.data['from'], self.data['to']))

  def test_outbound_valid_parameters(self):
    data = {
      'from': '4924195509197',
      'to': '4924195509193',
      'text': 'sample test'
    }
    # Reset the redis data if the key already presents
    cachemanager.setex(data['from'], 60 * 60 * 24, 0)
    response = client.post('/outbound/sms/', data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], 'outbound sms ok')
    self.assertEqual(response_data['error'], '')

  def test_max_api_request(self):
    data = {
      'from': '3253280312',
      'to': '3253280313',
      'text': 'sample test'
    }
    # Reset the redis data if the key already presents
    cachemanager.setex(data['from'], 60 * 60 * 24, 0)
    max_request = int(config['Api']['max_request'])
    for i in range(max_request - 1):
      response = client.post('/outbound/sms/', data,
        HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
      response_data = json.loads(response.content)
      self.assertEqual(response_data['message'], 'outbound sms ok')
      self.assertEqual(response_data['error'], '')
    # When the api request is made even after max_request number,
    # then expect an error message
    response = client.post('/outbound/sms/', data,
      HTTP_X_USERNAME='plivo1', HTTP_X_AUTHID='20S0KPNOIM')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    response_data = json.loads(response.content)
    self.assertEqual(response_data['message'], '')
    self.assertEqual(response_data['error'],
      'limit reached for from {}'.format(data['from']))
