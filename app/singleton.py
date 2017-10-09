from functools import wraps

def singleton(cls):
    instances = {}
    @wraps(cls)
    def getInstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getInstance
