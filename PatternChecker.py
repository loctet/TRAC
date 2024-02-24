import re
from Extension import replace_assertion

class PatternChecker:
    @staticmethod
    def follows_pattern(input_string):
        input_string = input_string.strip()
        if input_string == '':
            return True
        
        pattern = r'^(\s*([a-zA-Z_]\w*|\w+\[\s*-?\d+\s*\])\s*:=\s*[^&|]+(&\s*([a-zA-Z_]\w*|\w+\[\s*-?\d+\s*\])\s*:=\s*[^&|]+)*)$'
        return bool(re.match(pattern, input_string))

    @staticmethod
    def get_all_old_variables(input_string):
        pattern = r'\b\w+_old\b'
        old_words = list(set(re.findall(pattern, input_string)))
        return old_words
    

    @staticmethod

    def append_old_to_vars_and_return_updated(assertion, vars):
        
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
        if len(PatternChecker.get_all_old_variables(preC)) > 0:
            print(f"{preC} should not contain _old variables")
            exit() 
    
    @staticmethod        
    def replace_var_with_old_in_pre(preC, postC_vars, var_names):
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