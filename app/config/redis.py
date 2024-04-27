import aioredis

async def get_redis_connection():
    redis = await aioredis.from_url('redis://localhost', encoding='utf-8',decode_responses=True)
    return redis
