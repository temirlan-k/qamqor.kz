import aioredis

async def get_redis_connection():
    redis = aioredis.from_url('redis://localhost', encoding='utf-8',decode_responses=True)
    return await redis
