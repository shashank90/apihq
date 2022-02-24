from typing import Dict

from redis import Redis

redis = Redis(host='localhost', port=6379, db=1)


# Precursor to store a python object is that it needs to be serializable.
# Approach followed here is to write `to_dict` and `from_dict` inside respective classes
def put_obj(key: str, value):
    """
    Store object as dict
    :param key:Cache key
    :param value: Object
    """
    put_str(key, value.to_dict())


def get_obj(key: str, cls):
    """
    Return object after converting from dict
    :param key: Cache key
    :param cls: Class name
    :return: Object
    """
    value = get_str(key)
    return cls.to_obj(value)


def put_dict(key: str, value: Dict):
    return redis.hmset(key, value)


def get_dict(key):
    return redis.hgetall(key)


def put_str(key: str, value: str):
    return redis.set(key, value)


def get_str(key: str):
    return redis.get(key)


def clear_cache(key: str):
    redis.delete(key)
