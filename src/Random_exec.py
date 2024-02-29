import csv
import glob
import os
import time
import traceback
import argparse
import pandas as pd
from Fbuilder import Fbuilder
from TransactionsGrinder import TransactionsGrinder
from The_Validator import The_Validator
from MiniTimer import MiniTimer
from Settings import *
from Helpers import run_parallel_generations, write_csv
from Z3Runner import Z3Runner


def function_to_count_num_path(list_, csv_data, index, directory, time_out = s_time_out ):
    """ 
    Counts the number of paths in FSMs defined in text files and updates a CSV data structure with the counts.
    
    :param list_: List of text file paths containing FSM definitions.
    :type list_: list[str]

    :param csv_data: Dictionary mapping text file paths to CSV data rows.
    :type csv_data: dict[str, Any]

    :param index: Index to distinguish output CSV files.
    :type index: int

    :param directory: Directory to save the output CSV file.
    :type directory: str

    :param time_out: Timeout limit for processing each FSM.
    :type time_out: float
    """
    sValidator = The_Validator()
    n_csv_data = []
    timer = MiniTimer()
    for txt_file_path in list_:
        if txt_file_path not in list(csv_data.keys()):
            continue
        try:
            txt_file_path = txt_file_path.replace("\\", "/")
            folder, filename = os.path.split(txt_file_path)
            file_base_name = os.path.splitext(filename)[0]
            folder += "/"
            part = folder.split("random_txt")
            trGrinder = TransactionsGrinder(file_base_name, f"./Z3_models/random_tests/" + part[1], folder, folder.replace('random_txt', 'random_json'), False, time_out = time_out)
            sValidator.transitions_to_json(trGrinder.get_full_txt_path(), trGrinder.get_full_json_path())
            trGrinder.get_json_from_file()
            print(f"Counting Paths-- {trGrinder.get_full_txt_path()} -----")
            csv_data[txt_file_path][1]["num_paths"] = trGrinder.transition_processor().fsmGraph.get_number_of_paths(trGrinder.fsm['states'])
            n_csv_data.append(list(csv_data[txt_file_path][1].values()))
            print()
        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()
            exit()
    
    path = f"./examples/random_txt/{directory}/list_of_files_info_{index}.csv"
    print("Writing data in : ", path)
    write_csv(path, n_csv_data)
    return []

def function_to_run(list_, csv_data, index, directory, number_runs_per_each, time_out = s_time_out ):
    """
    Processes Finite State Machines (FSMs) defined in text files, runs verification, and updates CSV data with the results.

    :param list_: List of text file paths containing FSM definitions.
    :type list_: list[str]
    :param csv_data: Dictionary mapping text file paths to CSV data rows.
    :type csv_data: dict
    :param index: Index to distinguish output CSV files.
    :type index: int
    :param directory: Directory to save the output CSV file.
    :type directory: str
    :param number_runs_per_each: Number of verification runs for each FSM.
    :type number_runs_per_each: int
    :param time_out: Timeout limit for processing each FSM.
    :type time_out: int
    """

    sValidator = The_Validator()
    n_csv_data = []
    timer = MiniTimer()
    for txt_file_path in list_:
        if txt_file_path not in list(csv_data.keys()):
            continue
        try:
            txt_file_path = txt_file_path.replace("\\", "/")
            folder, filename = os.path.split(txt_file_path)
            file_base_name = os.path.splitext(filename)[0]
            folder += "/"
            part = folder.split("random_txt")
            
            trGrinder = TransactionsGrinder(
                file_base_name, 
                f"./Z3_models/random_tests/" + part[1], 
                folder, 
                folder.replace('random_txt', 'random_json'), 
                False, 
                time_out = time_out
            )
            sValidator.transitions_to_json(trGrinder.get_full_txt_path(), trGrinder.get_full_json_path())
            trGrinder.get_json_from_file()
            trGrinder.pre_process_fsm()

            print(f"Building-- and running -- {trGrinder.get_full_z3model_path()} -----")
            if txt_file_path not in list(csv_data.keys()):
                exit()

            buidingTime = runningTime = nb_time_out = 0
            times = {}
            times["participants"] = times["non_determinism"] = times["a_consistency"] = times["f_building"] = 0
            nb_runs = 0
            verdict = ""
            for _ in range(number_runs_per_each):
                nb_runs += 1
                timer.start_time()
                trGrinder.tr_grinding(False)
                buidingTime += timer.get_ellapsed_time()

                times["participants"] += trGrinder.info["t_participants"]
                times["non_determinism"] += trGrinder.info["t_non_determinism"]
                times["a_consistency"] += trGrinder.info["t_a_consistency"]

                if trGrinder.info["is_time_out"]:
                    if nb_time_out > 2:
                        break

                    nb_time_out += 1
                    continue
                
                
                timer.start_time()
                Fbuilder.build_z3_formulas_model_and_save(trGrinder, trGrinder.get_full_z3model_path(), False)
                times["f_building"] += timer.get_ellapsed_time()

                timer.start_time()
                verdict = Z3Runner.execute_model(trGrinder,trGrinder.get_full_z3model_path())
                runningTime += timer.get_ellapsed_time()
            
            print(trGrinder.output)
            
            if txt_file_path in list(csv_data.keys()):
                csv_data[txt_file_path][1]["num_paths"] = trGrinder.info["nb_path"]
                csv_data[txt_file_path][1]["verdict"] = verdict
                csv_data[txt_file_path][1]["participants_time"] = times["participants"] / nb_runs
                csv_data[txt_file_path][1]["non_determinism_time"] = times["non_determinism"] / nb_runs
                csv_data[txt_file_path][1]["a_consistency_time"] = times["a_consistency"] / nb_runs
                csv_data[txt_file_path][1]["f_building_time"] = times["f_building"] / nb_runs
                csv_data[txt_file_path][1]["building_time"] = buidingTime / nb_runs
                csv_data[txt_file_path][1]["z3_running_time"] = runningTime /nb_runs
                csv_data[txt_file_path][1]["total"] = (buidingTime + runningTime) / nb_runs
                csv_data[txt_file_path][1]["is_time_out"] = trGrinder.info["is_time_out"]
                n_csv_data.append(list(csv_data[txt_file_path][1].values()))

            print()
        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()
            exit()
    path = f"./examples/random_txt/{directory}/list_of_files_info_{index}.csv"
    print("Writing data in : ", path)
    write_csv(path, n_csv_data)
    return []

       
class RandomTransitionsExecuter: 
    """
    Executes verification for randomly generated Finite State Machine (FSM) transitions, storing results in CSV files.

    :param directory: Directory where FSM definitions and results are stored.
    :type directory: str
    :param merge_csv: Flag to merge individual CSV results into a single file.
    :type merge_csv: bool
    :param number_test_per_cpu: Number of tests to process concurrently per CPU.
    :type number_test_per_cpu: int
    :param number_runs_per_each: Number of verification runs for each FSM.
    :type number_runs_per_each: int
    :param time_out: Timeout limit for processing each FSM.
    :type time_out: int
    """

    def __init__(self, directory, merge_csv = 0, 
                 number_test_per_cpu = s_number_test_per_cpu, 
                 number_runs_per_each = s_number_runs_per_each, time_out =  s_time_out) -> None:
        self.directory = directory
        self.merge_csv = merge_csv
        self.headers = s_csv_headers
        self.number_runs_per_each = number_runs_per_each
        self.number_test_per_cpu = number_test_per_cpu
        self.csv_file_path = os.path.join('./examples/random_txt/', self.directory, 'list_of_files_info.csv')
        self.csv_merged_file_path = os.path.join('./examples/random_txt/', self.directory, 'merged_list_of_files_info.csv')
        self.csv_data = self.read_csv_data(self.csv_file_path)
        self.base_dir =  os.path.join('./examples/random_txt/', self.directory)
        self.timer = MiniTimer()
        self.time_out = time_out
        print("Init Done")

    def read_csv_data(self, path):
        """
        Reads CSV data from a given path into a dictionary.
        """
        csv_data = {}
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=self.headers, delimiter=',')
            next(reader)  # Skip the header
            for row in reader:
                item = "|".join(f"{header}: {row[header]}" for header in self.headers)
                row['path'] = row['path'].replace("\\", "/")
                csv_data[row['path']] = [item, row]
        
        return csv_data

    def merge_and_delete(self):
        """
        Merges individual CSV result files into a single file and cleans up.
        """
        time_ = time.time()
        #create a dir to keep old csvs
        os.makedirs(os.path.join(self.base_dir, f"{time_}"), exist_ok=True)
        merged_csv = self.csv_merged_file_path
        #rename it to avoid deleting the merges already
        if os.path.exists(merged_csv):
            os.rename(merged_csv, merged_csv.replace(".csv", f"_{time_}.csv"))

        pattern = os.path.join(self.base_dir, '*.csv')
        csv_files = glob.glob(pattern)
        dataframes = []
        for file in csv_files:
            # Skip the 'list_of_files_info.csv' file it contains all txt metadata
            if 'list_of_files_info.csv' not in file:
                df = pd.read_csv(file)
                dataframes.append(df)

        # Concatenate all dataframes into one
        merged_dataframe = pd.concat(dataframes, ignore_index=True)

        # Save the merged dataframe to a new CSV file
        merged_dataframe.to_csv(merged_csv, index=False)

        # Move all original CSV files except 'list_of_files_info.csv' to a new dir, to keep old onces
        for file in csv_files:
            if 'list_of_files_info.csv' not in file:
                f_name = os.path.basename(file)
                os.rename(file, file.replace(f_name, f"/{time_}/{f_name}"))

     

    def process_all_txt_files(self):
        """
        Processes all text files containing FSM definitions for verification.
        """
        data = pd.read_csv(os.path.join(self.base_dir, 'list_of_files_info.csv'))
        sorted_data = data.sort_values(by='num_transitions', ascending=True)
        txt_files = [ item.replace("\\", "/") for item in sorted_data["path"]]
        
        works = []
        num_item = self.number_test_per_cpu
        for i in range(0, len(txt_files), num_item):
            works.append((function_to_run, txt_files[i:min(i + num_item, len(txt_files))], self.csv_data, i, self.directory, self.number_runs_per_each, self.time_out))

        run_parallel_generations(works)

    def count_all_path_in_fsm(self):
        """
        Counts all paths in FSMs defined in text files and updates CSV data with the counts.
        """
        self.csv_data = self.read_csv_data(self.csv_merged_file_path)
        data = pd.read_csv(os.path.join(self.base_dir, 'merged_list_of_files_info.csv'))
        sorted_data = data.sort_values(by='num_transitions', ascending=True)
        txt_files = [item.replace("\\", "/") for item in sorted_data["path"]]

        works = []
        num_item = self.number_test_per_cpu
        for i in range(0, len(txt_files), num_item):
            end_index = min(i + num_item, len(txt_files))
            works.append((function_to_count_num_path, txt_files[i:end_index], self.csv_data, i, self.directory))

        run_parallel_generations(works)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Random Transitions and Store Them in Files')
    parser.add_argument('directory', type=str, help='Txt Dir where tests are located')
    parser.add_argument('--merge_csv', type=int, default = 0, help='Merge Only Csvs in dir 1 true 0')
    parser.add_argument('--add_path', type=int, default = 0, help='add path in dir 1 true 0')
    parser.add_argument('--number_test_per_cpu', type=int, default = s_number_test_per_cpu, help='Number per cpu / thread')
    parser.add_argument('--number_runs_per_each', type=int, default = s_number_runs_per_each, help='Number of runs per each')
    parser.add_argument('--time_out', type=int, default = s_time_out , help='Time out number')
    args = parser.parse_args()
   
    rExec = RandomTransitionsExecuter(args.directory, args.merge_csv, args.number_test_per_cpu, args.number_runs_per_each, time_out = args.time_out)

    if args.add_path == 1 :
        rExec.count_all_path_in_fsm()
    elif args.merge_csv == 1:
        rExec.merge_and_delete()
    else:
        rExec.process_all_txt_files()
        rExec.merge_and_delete()
    