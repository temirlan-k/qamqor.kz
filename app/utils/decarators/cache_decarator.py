import json
from functools import wraps
from uuid import UUID

def cache_redis(key_prefix: str, expire: int):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            product_id = args[0] if args else kwargs.get('id')
            cache_key = f"{key_prefix}:{product_id}"
            cached_data = await self.redis.get(cache_key)
            print(cache_key)

            if cached_data:
                print('Data retrieved from Redis cache')
                return json.loads(cached_data)
            result = await func(self, *args, **kwargs)
            if result:
                await self.redis.set(cache_key, json.dumps(result), ex=expire)
                print('Data cached in Redis')
            
            return result
        return wrapper
    return decorator
