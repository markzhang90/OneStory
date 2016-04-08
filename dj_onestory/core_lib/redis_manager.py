import redis
import time
from .conf import _CONF


class RedisManager:
    HOST = None
    redis_client = None
    _conf = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(RedisManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        try:
            self._conf = _CONF()
            self.HOST = self._conf._redis_host()
            self.redis_client = redis.Redis(host=self.HOST['host'], port=self.HOST['port'], db=0)
        except Exception as e:
            print(e)

    def read_from_cache(self, key):
        value = self.redis_client.get(key)
        if value is None:
            data = None
        else:
            data = value
        return data

    def write_to_cache(self, key, value):
        return self.redis_client.set(key, value)

    def login_update(self, key, value):
        expires = int(time.time())+self._conf._expire_buffer()
        try:
            self.redis_client.pipeline()
            self.redis_client.set(key, value)
            self.redis_client.expireat(key, expires)
            self.redis_client.execute_command()
        except BaseException as e:
            return False
        return True

