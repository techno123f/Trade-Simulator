# utils/latency_tracker.py
import time

def measure_latency(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        out = func(*args, **kwargs)
        end = time.perf_counter()
        return out, end - start
    return wrapper
