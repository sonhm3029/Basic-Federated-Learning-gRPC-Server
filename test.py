from concurrent.futures import ThreadPoolExecutor
import time
import concurrent.futures as futures

def task(x):
    time.sleep(x)
    print(x)
    return x
    
start = time.time()
with ThreadPoolExecutor() as executor:
    submitted_fs = {
        executor.submit(task, value)
        for value in [1,2,3,4,5]
    }
    
    finished_fs, _ = futures.wait(
        fs=submitted_fs,
        timeout=None
    )
    print("OKOKOKOKKO")
    print(finished_fs)
end = time.time()
print(f"Finished after {end -start} seconds")