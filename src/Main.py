import os
import argparse
import json
from TransactionsGrinder import TransactionsGrinder
from VariableDeclarationConverter import VariableDeclarationConverter
from The_Validator import *
from Settings import s_non_stop
from Visual_graph import *

def exitWithMessage(message):
    """
    Prints a message and exits the program.

    Parameters:
    - message (str): The message to print before exiting.
    """
    print(f"\n /!\\ {message} \n")
    exit()

def main():
    """
    Processes a given JSON or TXT file based on the specified check type and other command-line arguments.

    This script supports performing well-formedness checks, individual function checks, path checks on the specified file,
    and generating a visual representation of the FSM (Finite State Machine) defined in the file.
    """
    parser = argparse.ArgumentParser(description="""Process a JSON or TXT file.\n
    Examples:\n
    python main.py examplefile - Performs a Well-Formedness Check on examplefile.json.\n
    python main.py examplefile 2 - Performs an Individual Function Check on examplefile.json.\n
    python main.py examplefile 3 --filetype txt - Performs a Path Check on examplefile.txt.\n
    python main.py examplefile fsm --filetype json - Prints FSM for examplefile.json.\n
    """)
    parser.add_argument('file_name', type=str, help='The name of the JSON or TXT file for processing (without extension).')
    parser.add_argument('check_type', nargs='?', default='1', choices=['1', '2', '3', 'fsm', 'fsm2'], help='The type of check to perform: 1 - Well-Formedness, 2 - Individual Function, 3 - Path Check, fsm - Print FSM')
    parser.add_argument('--filetype', choices=['json', 'txt'], default='json', help='Specify the file type (json or txt). Default is json.')
    parser.add_argument('--non_stop', default= s_non_stop, choices=['1', '2'], help='Checking And Stopping Immediately When Error Default is non_stop = 1, 2 means stop mode.')
    parser.add_argument('--time_out', type=int, default = 0, help='Time out number')

    args = parser.parse_args()

    file_name = f"{args.file_name}"
    trGrinder = TransactionsGrinder(file_name, non_stop = args.non_stop == "1", time_out = args.time_out)
    
    if args.filetype == "txt":
        if not os.path.isfile(trGrinder.get_full_txt_path()):
            exitWithMessage(f"{trGrinder.get_full_txt_path()} does not exist")

        print("--Parsing Txt to generate Json file")
        sParser = The_Validator()
        sParser.transitions_to_json(trGrinder.get_full_txt_path(), trGrinder.get_full_json_path())
        print()
        file_name = f"{file_name}"

        #setattr(trGrinder, "file_name", file_name)
    elif not os.path.isfile(trGrinder.get_full_json_path()):
        exitWithMessage(f"{trGrinder.get_full_json_path()} does not exist")

    input_text = trGrinder.get_json_from_file()
    trGrinder.pre_process_fsm()

    # Write the JSON output

    if args.check_type == '1':
        trGrinder.tr_grinding(True)
    elif args.check_type == '2':
        trGrinder.check_independant_sat()
    elif args.check_type == '3':
        trGrinder.check_path_sat()
    elif args.check_type == 'fsm':
        os.system(f"java -jar ./GraphGen/GraphGen.jar -i {trGrinder.get_full_json_path()} -visualize ")
        os.system(f"cls")
        print("--Generated the visual FSM")
    elif args.check_type == 'fsm2':
        print("--Generating the visual FSM")
        draw_fsm_graph(generate_fsm_graph(''.join(input_text)))        
    else:
        # Perform all checks if no specific check type is provided
        trGrinder.tr_grinding(True)
        #trGrinder.check_independant_sat()
        #trGrinder.check_path_sat()

if __name__ == "__main__":
    main()
