import re
from Extension import replace_assertion

class PatternChecker:
    """
    Provides utility functions for checking patterns, extracting variables,
    and modifying assertions in strings related to smart contract verification.
    """

    @staticmethod
    def follows_pattern(input_string):
        """
        Checks if the input string follows a specific pattern for variable assignments.

        :param input_string: The string to check.
        :type input_string: str
        :return: True if the input string follows the pattern, False otherwise.
        :rtype: bool
        """

        input_string = input_string.strip()
        if input_string == '':
            return True
        
        pattern = r'^(\s*([a-zA-Z_]\w*|\w+\[\s*-?\d+\s*\])\s*:=\s*[^&|]+(&\s*([a-zA-Z_]\w*|\w+\[\s*-?\d+\s*\])\s*:=\s*[^&|]+)*)$'
        return bool(re.match(pattern, input_string))

    @staticmethod
    def get_all_old_variables(input_string):
        """
        Extracts all variables with '_old' suffix from the input string.

        :param input_string: The string to search.
        :type input_string: str
        :return: A list of unique variable names with '_old' suffix found in the input string.
        :rtype: list
        """

        pattern = r'\b\w+_old\b'
        old_words = list(set(re.findall(pattern, input_string)))
        return old_words
    

    @staticmethod

    def append_old_to_vars_and_return_updated(assertion, vars):
        """
        Appends '_old' suffix to specified variables in an assertion and returns the updated assertion.

        :param assertion: The assertion to process.
        :type assertion: str
        :param vars: A list of variable names to be updated.
        :type vars: list
        :return: The updated assertion with specified variables appended with '_old'.
        :rtype: str
        """

        updated_vars = []  # List to store updated variable names
        var_in_f = set()
        processed_assignments = []
        for d in assertion.split("&"):
            parts = [part.strip() for part in d.split(":=")]
            if len(parts) == 2 and parts[0] in vars:
                var_in_f.add(parts[0])
        
        pattern = r'\b(' + '|'.join(re.escape(var) for var in list(var_in_f)) + r')\b'

        def replace(match):
            updated_var = match.group(1) + '_old '
            updated_vars.append(updated_var)  # Collect the updated variable name
            return updated_var
        
        for d in assertion.split("&"):
            parts = [part.strip() for part in d.split(":=")]
            if len(parts) == 2:      
                updated_expression = re.sub(pattern, replace, parts[1])
                processed_assignments.append(f"{parts[0]} := {updated_expression}")

        modified_assertion = " & ".join(processed_assignments)
        updated_vars = list(set(updated_vars))

        return modified_assertion

    @staticmethod
    def z3_post_condition(postC, var_names):
        """
        Processes and returns a Z3 compatible post-condition assertion.

        :param postC: The post-condition assertion to process.
        :type postC: str
        :param var_names: A dictionary mapping variable names to their types.
        :type var_names: dict
        :return: A tuple containing the processed post-condition assertion and a list of variable names.
        :rtype: tuple[str, list[str]]
        """

        if  postC.strip() == "" :
            return ["True", []]
        
        try:
            _list = postC.split("&")
            parts = []
            _varnames = []
            for item in _list:
                if item.strip() == "":
                    print(f"{postC} in not correct")
                    exit()
                    
                _varname, _assign = [a.strip() for a in item.split(":=")]
                _assign = replace_assertion(_assign)
                
                if _varname in var_names and var_names[_varname] == 'string':
                    parts.append(f"{_varname} == {_assign}")
                else:
                    parts.append(f"{_varname} == {_assign}")
                _varnames.append(_varname)
            formula = ", ".join(parts)
            
        except Exception as e:
            print(f"z3_post_condition: {e}")
        return  [f"And({formula})", _varnames]
    
    @staticmethod
    def pre_condition_not_having_old_vars(preC, postC):
        """
        Validates that a pre-condition does not contain variables with '_old' suffix.

        :param preC: The pre-condition to validate.
        :type preC: str

        :param postC: The post-condition, used for context.
        :type postC: str

        :raises Exception: If '_old' variables are found in the pre-condition.
        """
        if len(PatternChecker.get_all_old_variables(preC)) > 0:
            print(f"{preC} should not contain _old variables")
            exit() 
    
    @staticmethod        
    def replace_var_with_old_in_pre(preC, postC_vars, var_names):
        """
        Replaces variables in a pre-condition with their '_old' counterparts.

        :param preC: The pre-condition to process.
        :type preC: str
        :param postC_vars: A list of variables from the post-condition.
        :type postC_vars: list
        :param var_names: A dictionary mapping variable names to their types.
        :type var_names: dict

        :return: A tuple containing the updated pre-condition and a list of input variables.
        :rtype: tuple
        """
        def replace(match):
            return match.group(0) + "_old"

        try:
            z3_reserved_words = ['And', 'Or', 'Not', 'Implies', 'ForAll', 'Exists', 'Bool', 'Int', 'Real', 'eq']
            reserved_words = z3_reserved_words + ['and', 'or', 'not', 'if', 'else', 'for', 'while', 'in', 'True', 'False', 'None', 'len', 'append']
            pattern = r'\b(?:[a-zA-Z_]\w*)\b'
            variable_names = re.findall(pattern, preC)

            inputs = []
            for name in variable_names:
                if name not in reserved_words and name in postC_vars:
                    preC = re.sub(r'\b' + re.escape(name) + r'\b', replace, preC)
                    inputs.append(f"{var_names[name]} {name}_old")
                    
        except Exception as e:
            print(f"replace_var_with_old_in_pre: {e}")        
        return (preC, inputs)