import json
from functools import wraps
from functools import wraps

from utils.decarators.encoder import CustomEncoder

def cache_redis(key_prefix: str, cache_type: str, expire: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            cache_key = f"{key_prefix}:{kwargs.get('id', '')}" if cache_type == 'details' else key_prefix
            cached_data = await self.redis.get(cache_key)
            if cached_data:
                print(f'from Redis, cache key: {cache_key}')
                return json.loads(cached_data)
            result = await func(self, *args, **kwargs)
            if result:
                try:
                    serialized_data = json.dumps(result, cls=CustomEncoder)
                    await self.redis.set(cache_key, serialized_data, ex=expire)
                    print(f'from DB, cached in Redis -> key - {cache_key}')
                except TypeError as e:
                    print(f"Error serializing data: {e}")
            return result
        return wrapper
    return decorator
