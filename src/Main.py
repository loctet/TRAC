import os
import argparse
import json
from TransactionsGrinder import TransactionsGrinder
from VariableDeclarationConverter import VariableDeclarationConverter
from The_Validator import *
from Settings import *
from Visual_graph import *
from Helpers import clear

def exitWithMessage(message):
    """
    Prints a message and exits the program.

    Parameters:
    - message (str): The message to print before exiting.
    """
    print(f"\n /!\\ {message} \n")
    exit()

def update_paths(file_name, filetype):
    """
    Updates the settings paths based on the given file name and file type.

    Parameters:
    - file_name (str): The full file path.
    - filetype (str): The type of the file (e.g., 'json', 'txt').

    Returns:
    - dict: A dictionary with updated paths and cleaned file name.
    """
    file_dir = os.path.dirname(file_name)
    base_name = os.path.splitext(os.path.basename(file_name))[0]

    updated_paths = {
        "s_z3model_path": os.path.join(file_dir, "Z3_models/"),
        "s_txt_path": os.path.join(file_dir),
        "s_json_path": os.path.join(file_dir, ""),
        "file_name": base_name
    }

    return updated_paths

def main():
    """
    Processes a given JSON or TXT file based on the specified check type and other command-line arguments.

    This script supports performing well-formedness checks, individual function checks, path checks on the specified file,
    and generating a visual representation of the DAFSM defined in the file.
    """
    parser = argparse.ArgumentParser(description="""Process a JSON or TXT file.\n
    Examples:\n
    python main.py examplefile - Performs a Well-Formedness Check on examplefile.json.\n
    python main.py examplefile 2 - Performs an Individual Function Check on examplefile.json.\n
    python main.py examplefile 3 --filetype txt - Performs a Path Check on examplefile.txt.\n
    python main.py examplefile fsm --filetype json - Prints DAFSM for examplefile.json.\n
    """)
    parser.add_argument('file_name', type=str, help='The name of the JSON or TXT file for processing (with full path).')
    parser.add_argument('check_type', nargs='?', default='1', choices=['1', '2', '3', 'fsm', 'fsm2'], help='The type of check to perform: 1 - Well-Formedness, 2 - Individual Function, 3 - Path Check, fsm - Print DAFSM')
    parser.add_argument('--filetype', choices=['json', 'txt'], default='txt', help='Specify the file type (json or txt). Default is txt.')
    parser.add_argument('--non_stop', default=s_non_stop, choices=['1', '2'], help='Checking And Stopping Immediately When Error Default is non_stop = 1, 2 means stop mode.')
    parser.add_argument('--time_out', type=int, default=0, help='Time out number')

    args = parser.parse_args()

    # Update paths and file name based on input
    paths = update_paths(args.file_name, args.filetype)

    global s_z3model_path, s_txt_path, s_json_path
    s_z3model_path = paths["s_z3model_path"]
    s_txt_path = paths["s_txt_path"]
    s_json_path = paths["s_json_path"]

    file_name = paths["file_name"]

    trGrinder = TransactionsGrinder(
        file_name, 
        non_stop=args.non_stop == "1", 
        time_out=args.time_out, 
        z3model_path=s_z3model_path,
        txt_path=s_txt_path,
        json_path=s_json_path
    )

    if args.filetype == "txt":
        if not os.path.isfile(trGrinder.get_full_txt_path()):
            exitWithMessage(f"{trGrinder.get_full_txt_path()} does not exist")

        print("Parsing Txt to generate Json file----")
        sParser = The_Validator()
        sParser.transitions_to_json(trGrinder.get_full_txt_path(), trGrinder.get_full_json_path())
    elif not os.path.isfile(trGrinder.get_full_json_path()):
        exitWithMessage(f"{trGrinder.get_full_json_path()} does not exist")

    input_text = trGrinder.get_json_from_file()
    trGrinder.pre_process_fsm()

    # Perform the specified check
    if args.check_type == '1':
        trGrinder.tr_grinding(True)
    elif args.check_type == '2':
        trGrinder.check_independant_sat()
    elif args.check_type == '3':
        trGrinder.check_path_sat()
    elif args.check_type == 'fsm':
        print("--Generating the visual DAFSM")
        os.system(f"java -jar ./GraphGen/GraphGen.jar -i {trGrinder.get_full_json_path()} -visualize ")
        clear()
        print(f"--Generated the visual DAFSM")
    elif args.check_type == 'fsm2':
        print("--Generating the visual DAFSM")
        draw_fsm_graph(generate_fsm_graph(''.join(input_text)))
    else:
        # Perform all checks if no specific check type is provided
        trGrinder.tr_grinding(True)

if __name__ == "__main__":
    main()
