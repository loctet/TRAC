import subprocess
from Settings import s_well_formed_message

class Z3Runner:
    @staticmethod
    def execute_model(chercker, path) -> bool:  
        try:
            chercker.logIt("Execution by Z3\n")
            result = subprocess.run(["python3", f'{path}'], capture_output=True, text=True)
            chercker.output =  result.stdout

        except FileNotFoundError:
            print(f"Error: The file '{path}' does not exist.")
        except Exception as e:
            print("Error processing the check")
            print(e)
       
        chercker.logIt(chercker.output) 
        chercker.logIt(f"\n(Check the generated file  {path} to fine the z3 code generated)\n") 
        return Z3Runner.analyser(chercker.output)
    
    @staticmethod
    def analyser(result) -> bool:
        return s_well_formed_message in result