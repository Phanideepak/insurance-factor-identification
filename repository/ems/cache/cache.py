from redis import Redis
import json



class CacheService:
    def has(key : str, cache : Redis):
        return cache.exists(key)

    def get(key : str, cache : Redis):
        if not cache.exists(key):
            return None
        return json.loads(cache.get(key))

    def put(key : str, value, cache : Redis, jsonSerializer = None):
        cache.set(name = key, value = json.dumps(value, default = jsonSerializer), ex = 3600)

    def delete(key : str, cache : Redis):
        if cache.exists(key):
            cache.delete(key)