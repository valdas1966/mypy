import concurrent.futures as pool


class C:

    def __init__(self, name: str, size: int) -> None:
        print(name, size)


params = [['a', 'b'], [2, 2]]

worker = pool.ThreadPoolExecutor(max_workers=len(params))
worker.map(C, *params)
worker.shutdown()