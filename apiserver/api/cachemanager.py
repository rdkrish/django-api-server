import redis

from configmanager import config

class CacheManager:
  def __init__(self):
    self.cache_connection = redis.StrictRedis(host = config['Redis']['host'],
      port = config['Redis']['port'], db = 0)

  def setex(self, name, time, value):
    return self.cache_connection.setex(name, time, value)

  def get(self, name):
    return self.cache_connection.get(name)

  def incr(self, name, amount=1):
    return self.cache_connection.incr(name, amount)
