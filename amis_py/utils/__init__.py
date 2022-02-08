import hashlib
import random


def is_default(value, default):
    if value is None and default is None:
        return True
    if value == default:
        return True
    return False


def get_random_hash(length=6):
    res = ""
    chars = "abcdefghijklmnopqrstuvwsxy0123456789"
    for _ in range(length):
        res += chars[random.randint(0, len(chars)-1)]
    return hashlib.sha1(res.encode()).hexdigest()
