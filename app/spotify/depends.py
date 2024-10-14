import redis

r = redis.Redis(host="redis", decode_responses=True)
