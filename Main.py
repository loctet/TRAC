import os
import argparse
import json
from TransactionsGrinder import TransactionsGrinder
from VariableDeclarationConverter import VariableDeclarationConverter
from The_Validator import *
from Settings import s_non_stop

def well_formedness_check(file_name):
    try:
        with open(file_name, 'r') as file:
            json.load(file)
        print("JSON is well-formed.")
    except json.JSONDecodeError as e:
        print(f"JSON is not well-formed: {e}")

def individual_function_check(file_name):
    # Placeholder for actual function check
    print(f"Performing individual function check on {file_name}.")

def path_check(file_name):
    # Placeholder for actual path check
    print(f"Performing path check on {file_name}.")

def exitWithMessage(message):
    print(f"\n /!\\ {message} \n")
    exit()

def main():
    parser = argparse.ArgumentParser(description="""Process a JSON or TXT file.\n
    Examples:\n
    python main.py examplefile - Performs a Well-Formedness Check on examplefile.json.\n
    python main.py examplefile 2 - Performs an Individual Function Check on examplefile.json.\n
    python main.py examplefile 3 --filetype txt - Performs a Path Check on examplefile.txt.\n
    python main.py examplefile fsm --filetype json - Prints FSM for examplefile.json.\n
    """)
    parser.add_argument('file_name', type=str, help='The name of the JSON or TXT file for processing (without extension).')
    parser.add_argument('check_type', nargs='?', default='1', choices=['1', '2', '3', 'fsm'], help='The type of check to perform: 1 - Well-Formedness, 2 - Individual Function, 3 - Path Check, fsm - Print FSM')
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
        print("--Generating the visual JAVA FSM")
        os.system(f"java -jar ./Java_parser/javaParser.jar -i {trGrinder.get_full_json_path()} -visualize ")
            
    else:
        # Perform all checks if no specific check type is provided
        trGrinder.tr_grinding(True)
        trGrinder.check_independant_sat()
        trGrinder.check_path_sat()

if __name__ == "__main__":
    main()
