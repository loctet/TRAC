import subprocess
from Settings import s_well_formed_message

class Z3Runner:
    """
    A class to execute Z3 models and analyze the output.
    
    This class provides static methods to run a Z3 solver model file and analyze the output
    to check for a specific well-formed message indicating success.
    """
    
    @staticmethod
    def execute_model(checker, path) -> bool:
        """
        Executes a Z3 model file and captures its output.

        :param checker: An object that provides logging capabilities.
        :param path: The file path to the Z3 model to be executed.
        :type path: str
        :return: True if the Z3 model output contains the well-formed message, False otherwise.
        :rtype: bool

        The method logs the execution process and result, and handles file not found and
        general exceptions by logging the errors.
        """

        try:
            checker.logIt("Execution by Z3\n")
            result = subprocess.run(["python3", f'{path}'], capture_output=True, text=True)
            checker.output = result.stdout

        except FileNotFoundError:
            print(f"Error: The file '{path}' does not exist.")
        except Exception as e:
            print("Error processing the check")
            print(e)
       
        checker.logIt(checker.output) 
        checker.logIt(f"\n(Check the generated file  {path} to find the z3 code generated)\n") 
        return Z3Runner.analyser(checker.output)
    
    @staticmethod
    def analyser(result) -> bool:
        """
        Analyzes the output of a Z3 model execution.

        :param result: The output from the Z3 model execution.
        :type result: str
        :return: True if the output contains the predefined well-formed message, False otherwise.
        :rtype: bool
        """

        return s_well_formed_message in result
