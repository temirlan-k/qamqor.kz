import json
from functools import wraps
from typing import List

from utils.decarators.encoder import CustomEncoder

def cache_redis(key_prefix: str, cache_type: str, expire: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            print(kwargs)
            print(kwargs.get('id', ''))
            cache_key = f"{key_prefix}:{kwargs.get('id', '')}" if cache_type == 'details' else key_prefix
            print(cache_key)
            cached_data = await self.redis.get(cache_key)
            print(cached_data)
            if cached_data is not None:
                print(f'from Redis, cache key: {cache_key}')
                return json.loads(cached_data)

            result = await func(self, *args, **kwargs)
        
            try:
                if isinstance(result, List):
                    serialized_data = json.dumps(result)
                    await self.redis.set(cache_key, serialized_data, ex=expire)
                    print(f'from DB, cached in Redis -> key - {cache_key}')
                else:
                    serialized_data = json.dumps(result)
                    await self.redis.set(cache_key, serialized_data, ex=expire)
                    print(f'from DB, cached in Redis -> key - {cache_key}')
            except TypeError as e:
                    print(f"Error serializing data: {e}")
            return result

        return wrapper
    return decorator
