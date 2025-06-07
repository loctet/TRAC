from PatternChecker import PatternChecker
import re

class VariableDeclarationConverter:
    """
    A class responsible for converting variable declarations into Z3 solver compatible format.

    This class provides static methods to convert variable declarations from a custom format into
    Z3 declarations, handling different data types including integers, strings, booleans, sets,
    arrays, and participant types. It supports initial value assignment and checks for correct
    syntax using a pattern checker.
    """
    
    @staticmethod
    def convert_to_z3_declarations(declarations_str, deploy_init_var_val = [], var_names = {},  deploy=False):
        """
        Converts variable declarations into Z3 declarations with optional initial values.

        :param declarations_str: String containing variable declarations separated by semicolons or commas.
        :type declarations_str: str
        :param deploy_init_var_val: List to append initial values of variables for deployment.
        :type deploy_init_var_val: list
        :param var_names: Dictionary to map variable names to their types.
        :type var_names: dict
        :param deploy: Flag to indicate if the conversion is for deployment purposes.
        :type deploy: bool
        :return: A tuple containing the Z3 declarations as a string, a list of initial values for deployment,
                    a dictionary of variable names and types, and a dictionary of participant variables.
        :rtype: tuple[str, list, dict, dict]
        """


        declarations = [declaration.strip() for declaration in re.split(';|,', declarations_str) if declaration.strip()]  # Split input into separate variable declarations and # Remove any empty declarations
        var_names = {}
        participants = {}
        result = ""
        for declaration in declarations:
            try:
                # Split each declaration into type, variable name, and optional initial value
                parts = declaration.split(":=") # Assuming the initial value is after ":="
                splited = [s.strip() for s in parts[0].split()]

                var_type, var_name = [splited[0], splited[1]] if len(splited) == 2 else [splited[0], splited[2]]
                
                if len(PatternChecker.get_all_old_variables(var_name)) >= 1 and deploy:
                    print(f"{var_name} not correct")
                    exit()
                
                z3_var = None
                z3_var_init = None
                if len(parts) == 2:
                    initial_value = parts[1]
                    # Create Z3 variables based on the declared type and assign the initial value
                    if var_type == 'int':
                        initial_value = int(initial_value)
                        z3_var = f"{var_name} = Int('{var_name}')"
                        z3_var_init = f"{var_name} = {initial_value}"

                    if var_type == 'string':
                        initial_value = str(initial_value)
                        z3_var = f"{var_name} = String('{var_name}')"
                        z3_var_init = f"{var_name} = \"{initial_value}\""
                    
                    elif var_type == 'bool':                     
                        z3_var = f"{var_name} = Bool('{var_name}')"
                        z3_var_init = f"{var_name} = {initial_value}"
                        
                    elif var_type == 'set':
                        if len(splited) == 3 :
                            z3_var = f"{splited[2]} = Array('{splited[2]}', IntSort(), {splited[1]}Sort())"
                        else: 
                            z3_var = f"{var_name} = []"

                    elif var_type == 'array':
                        if len(splited) == 3 :
                            z3_var = f"{splited[2]} = Array('{splited[2]}', IntSort(), {splited[1]}Sort())"
                        else:
                            z3_var = f"{var_name} =  []"

                    elif var_type == 'participant':
                        if len(splited) == 3 :
                            participants[splited[2]] = splited[1]
                        else :
                            print(f"Wrong participant {splited[:]} declaration")
                            exit()
                        
                            
                else:
                    # Create Z3 variables without initial values
                    if var_type == 'int':
                        z3_var = f"{var_name} = Int('{var_name}')"
                    if var_type == 'string':
                        z3_var = f"{var_name} = String('{var_name}')"
                    elif var_type == 'float':
                        z3_var = f"{var_name} = Real('{var_name}')"
                    elif var_type == 'bool':
                        z3_var = f"{var_name} = Bool('{var_name}')"
                    elif var_type == 'set':
                        if len(splited) == 3 :
                            z3_var = f"{splited[2]} = Array('{splited[2]}', IntSort(), {splited[1]}Sort())"
                        else:
                            z3_var = f"{var_name} = []"
                    elif var_type == 'array':
                        if len(splited) == 3 :
                            z3_var = f"{splited[2]} = Array('{splited[2]}', IntSort(), {splited[1]}Sort())"
                        else:
                            z3_var = f"{var_name} = []"

                    elif var_type == 'participant':
                        if len(splited) == 3 :
                            participants[splited[2]] = splited[1]
                        else :
                            print(f"Wrong participant {splited[:]} declaration")
                            exit()

                if z3_var is not None:
                    result += f"{z3_var}\n"
                    
                    if var_name not in var_names:
                        var_names[var_name] = var_type
                    
                    if z3_var_init is not None:
                        result += f"{z3_var_init}\n"
                        deploy_init_var_val.append(z3_var_init)
            except Exception:
                print(f"{declaration} is not correcly written")   
       
        return [result, deploy_init_var_val, var_names, participants]
    

    def convert_assignements_to_z3_assignment(declarations_str):
        """
        Converts assignment statements into Z3 assignment format.

        :param declarations_str: String containing assignment declarations separated by '&' symbols.
        :type declarations_str: str
        :return: A string containing the converted Z3 assignment statements.
        :rtype: str
        """


        declarations = [declaration.strip() for declaration in declarations_str.split('&') if declaration.strip()]  # Split input into separate variable declarations and # Remove any empty declarations
        
        result = ""
        for declaration in declarations:
            # Split each declaration into type, variable name, and optional initial value
            parts = declaration.split(":=") # Assuming the initial value is after ":="
            
            z3_var = None
            if len(parts) == 2:
                var_name = parts[0].strip()
                initial_value = parts[1]
                
                z3_var = f"{var_name} = {initial_value}"

            if z3_var is not None:
                result += f"{z3_var}\n"    
                   
        return result
