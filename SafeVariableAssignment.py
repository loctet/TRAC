from PatternChecker import *
from MessagesTemplates import MessagesTemplates

class SafeVariableAssignment:
    @staticmethod
    def safe_variable_assignment(assignation_str, solver_name):
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
    
   
    