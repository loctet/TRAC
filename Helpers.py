import csv
import os 
import concurrent.futures
from Settings import s_csv_headers

def write_csv(path, data):
    """
    Writes data to a CSV file at the specified path.

    :param path: The file path where the CSV should be written.
    :type path: str
    :param data: The data to write to the CSV file, where each inner list represents a row.
    :type data: List[List]
    :return: None
    :rtype: NoneType
    """
    with open(path, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(s_csv_headers)
        write.writerows(data)


def run_parallel_generations(works):
    """
    Executes a list of functions in parallel, each with its own set of arguments.

    This function uses Python's concurrent.futures module to run multiple functions in parallel,
    utilizing multiple CPU cores for increased efficiency.

    :param works: A list where each tuple contains a function and its arguments.
    :type works: List[Tuple[Callable, Any]]
    :return: None
    :rtype: NoneType
    """
    # Determine the number of workers based on available CPUs minus 1
    num_workers = max(1, os.cpu_count() - 1)

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Schedule the function to be executed in parallel
        futures = [executor.submit(*args) for args in works]
        for future in concurrent.futures.as_completed(futures):
            future.result()

def clear():
    if(os.name == 'posix'):
        os.system('clear')
    # else screen will be cleared for windows
    else:
        os.system('cls')