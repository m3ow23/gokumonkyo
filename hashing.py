import hashlib

HASHING_ITERATIONS = 1000

def get_full_hash(string):
    hashed_string = string
    for _ in range(HASHING_ITERATIONS):
        hashed_string = hashlib.sha256((hashed_string + string).encode('utf-8')).hexdigest()

    return hashed_string

def get_single_hash(string):
    return hashlib.sha256((string).encode('utf-8')).hexdigest()