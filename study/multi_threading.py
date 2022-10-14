import threading
import time
import concurrent.futures


def thread_function(name):
    print(f'Start[{name}]')
    time.sleep(2)
    print(f'Finish[{name}]')


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(thread_function, range(100))




