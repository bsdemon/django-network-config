import json
import redis

class RedisService():
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)


    def publish_data(self, channel_name, json_data):
        return self.redis_client.publish(channel_name, json.dumps(json_data))
 