import redis
import app.onestory.conf.config as config
import app.onestory.library.customErr as customErr


class MyRedis(object):
    __first_init = True
    __pool_conf = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MyRedis, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        pass

    def get_connect_from_pool(self, pool_name='redis_onestory'):
        try:
            (host, port) = self.load_conf_from_pool_name(pool_name)
            pool = redis.ConnectionPool(host=host, port=int(port), socket_connect_timeout=10, retry_on_timeout=3, db=0)
            r = redis.Redis(connection_pool=pool)
        except customErr.CustomErr as e:
            return None
        except Exception as e:
            return None
        return r

    def load_conf_from_pool_name(self, pool_name):
        if pool_name in self.__pool_conf:
            return self.__pool_conf[pool_name]

        redis_host = config.load_config("redis_onestory", "host")
        redis_port = config.load_config("redis_onestory", "port")
        if redis_host is False or redis_port is False:
            raise customErr.CustomErr(customErr.CustomErr.common_err_code, 'get config fail')
        self.__pool_conf[pool_name] = (redis_host, redis_port)
        return self.__pool_conf[pool_name]
