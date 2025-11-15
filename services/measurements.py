import time
from functools import wraps

def measure_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = f"{end - start:.4f} seconds"
        return result, elapsed
    return wrapper

@measure_execution_time
def dummy_long_func():
    for _ in range(2):
        time.sleep(2)

if __name__ == "__main__":
    x, time_taken = dummy_long_func()
    print(x, time_taken)
