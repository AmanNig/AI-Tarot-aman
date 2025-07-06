# # cache.py
# import redis, json
# from initialize.config import REDIS_URL

# # Connect, auto-decode strings
# cache = redis.Redis.from_url(REDIS_URL, decode_responses=True)

# def get_cached(question: str):
#     key = question.lower().strip()
#     raw = cache.get(key)
#     return json.loads(raw) if raw else None

# def set_cached(question: str, data: dict, ttl: int = 86400):
#     key = question.lower().strip()
#     cache.set(key, json.dumps(data), ex=ttl)
  

import json
import time

_cache_store = {}

def get_cached(key):
    entry = _cache_store.get(key)
    if not entry:
        return None
    value, expires_at = entry
    if expires_at is None or expires_at > time.time():
        return value
    else:
        del _cache_store[key]
        return None

def set_cached(key, value, ttl=3600):
    expires_at = time.time() + ttl if ttl else None
    _cache_store[key] = (value, expires_at)
