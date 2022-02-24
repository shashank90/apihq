from concurrent.futures import ThreadPoolExecutor

THREAD_POOL = 10
pool = ThreadPoolExecutor(max_workers=THREAD_POOL)


def get_thread_pool_executor():
    return pool
