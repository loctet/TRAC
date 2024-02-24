import csv
import os 
import concurrent.futures
from Settings import s_csv_headers

def write_csv(path, data):
    with open(path, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(s_csv_headers)
        write.writerows(data)


def run_parallel_generations(works):
    # Determine the number of workers based on available CPUs minus 1
    num_workers = max(1, os.cpu_count() - 1)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Schedule the function to be executed in parallel
        futures = [executor.submit(*args) for args in works]
        for future in concurrent.futures.as_completed(futures):
            future.result()
