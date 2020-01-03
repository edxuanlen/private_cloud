import redis


pool = redis.ConnectionPool(host='localhost', port=6379)
class Session:
    def __init__(self):
        self.client = redis.Redis(connection_pool=pool)

    def set_sessoion(self, key, value):
        self.client.setex(key, 60 * 60, value)

    def get_session(self, key):
        return self.client.get(key)

    def delete_session(self, key):
        self.client.delete(key)
