class CacheManager:
  def __init__(self):
    import redis
    self.cache_connection = redis.StrictRedis(host = 'localhost', port = '6379', db = 0)

  def setex(self, name, time, value):
    return self.cache_connection.setex(name, time, value)

  def get(self, name):
    return self.cache_connection.get(name)

  def incr(self, name, amount=1):
    return self.cache_connection.incr(name, amount)
