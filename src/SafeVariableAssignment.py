from PatternChecker import *
from MessagesTemplates import MessagesTemplates

class SafeVariableAssignment:
    """
    Handles the safe assignment of variables for Z3 solver scripts, ensuring that variables
    are declared and assigned in a format compatible with Z3 solvers.
    """

    @staticmethod
    def safe_variable_assignment(assignation_str, solver_name):
        """
        Splits a string of variable assignments, ensures correct format, and prepares them
        for inclusion in a Z3 solver script.

        :param assignation_str: A string containing variable assignments separated by '&'.
        :type assignation_str: str
        :param solver_name: The name of the solver, used to prefix global variables.
        :type solver_name: str
        :return: A tuple containing two strings, the first is the Z3 compatible variable
                declarations and assignments, the second is a list of global variable
                declarations.
        :rtype: tuple[str, list[str]]
        """

        result = []
        global_vars = []           
        
        # Split the input string into individual assignments
        assignments = assignation_str.split('&')

        for assignment in assignments:
            if assignment.strip() == "" :
                continue
            # Split each assignment into variable name and value
            parts = assignment.strip().split(':=')
            
            # Ensure there are exactly two parts (variable name and value)
            if len(parts) != 2 and assignment.strip() != "":
                raise Exception(f"{assignment} not correct")
             
            
            variable_name, value = parts
            variable_name = re.split(r"\[", variable_name)[0]
            
            if variable_name != "":
                global_vars.append(f"global {variable_name}")
            
            result.append(MessagesTemplates.getFunctionVariableDeclaration(variable_name, value,  solver_name))
        return  ["\n".join(result), "\n    ".join(global_vars)]
    
   
    