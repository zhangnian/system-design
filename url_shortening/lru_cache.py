
class LRUCache:
    def __init__(self, capacity=1000):
        self.capacity = capacity
        self.data = {}
        self.hits = {}
        self.hits_count = 0
        self.miss_count = 0

    def clear(self):
        s = sorted(self.hits.items(), key=lambda v: v[1])
        if not s:
            return

        remove_key, _ = s[0]
        self.data.pop(remove_key)

    def add(self, key, value):
        if len(self.data) >= self.capacity:
            self.clear()

        self.data[key] = value
        self.hits[key] = 0


    def get(self, key):
        if key not in self.data:
            self.miss_count += 1
            return None

        self.hits[key] += 1
        self.hits_count += 1
        return self.data[key]

    def __str__(self):
        return 'current size: {} hits: {} miss: {}'.\
            format(len(self.data), self.hits_count, self.miss_count)


local_cache = LRUCache(100)
