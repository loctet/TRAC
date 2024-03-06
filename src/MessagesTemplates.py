class MessagesTemplates:
    """
    Provides templates for generating Z3 solver function definitions, result checks,
    global variable reset functions, and variable declaration blocks for use in
    smart contract verification scripts.
    """
    @staticmethod
    def getFunctionActionDefinition(funtionData):
        """
        Generates a Z3 solver function definition from provided function data.

        :param functionData: A dictionary containing information about the function,
            such as name, global variables, parameters, and conditions.
        :type functionData: dict
        :return: A string representing the complete function definition in Python code.
        :rtype: str
        """

        item = funtionData
        return f"""
def {item['snameF']}(infos = False):
    {item['sglobalVars']}
    # Declare variable before   
    {item["sparams"]}
    
    #building the solver for the predancontion
    solver_{item['snameF']} = z3.Solver() 
    solver_{item['snameF']}2 = z3.Solver() 
    #check if post condition implies any pre precondition
    solver_{item['snameF']}.push()
    
    solver_{item['snameF']}.add({item['sformula']})
    post_result = solver_{item['snameF']}.check() == z3.unsat
    
    #check determinism
    solver_{item['snameF']}.pop()
    solver_{item['snameF']}.push()
    solver_{item['snameF']}.add({item['epsformula']}) 
    eps_result = solver_{item['snameF']}.check() == z3.unsat

    #check participants
    solver_{item['snameF']}.pop()
    solver_{item['snameF']}.add({item['sparticipants']}) 
    part_result = solver_{item['snameF']}.check() == z3.sat
    
    result = post_result and eps_result and part_result
    
    if infos :
        if not result:
            print()
            print("--For {item['snameF']}: "," Check result :: ", result)

        if not part_result :
            print(f"--- Participants       : {{part_result}}")

        if  not eps_result :
            print ("--- Non Determinism  : ", ({item['epsformula']}))
            
        if not post_result: 
            print(f"--- A-Consistency: {{post_result}}")
            solver_{item['snameF']}2.add(Not({item['sformula']}))
            print("\\nSimplification of the of the negation of the formula: ", simplify(Not({item['sformula']})), " :: ", solver_{item['snameF']}2.check() == z3.sat)
            
          
                   
    return result
    """
    
    @staticmethod
    def getResultCheckPart():
        """
        Returns a template string for printing the verification result.

        :return: A string containing Python code for printing the verification verdict.
        :rtype: str
        """


        return f"""
    print("\\n(!) Verdict: "+ ("Well Formed" if  check_resut == True else "Not Well Formed"))
        """
        
    @staticmethod
    def getResetGlobalFunction(deploy_vars, var_names = []):
        """
        Generates a function for resetting global variables to their deployment values.

        :param deploy_vars: A string containing the deployment variable assignments.
        :type deploy_vars: str
        :param var_names: A list of variable names to be declared as global.
        :type var_names: list[str]
        :return: A string representing the function definition in Python code.
        :rtype: str
        """

        var_names = ("global " + ", ".join(var_names)) if len(var_names) > 0 else ""
        return f"""
def reset_deploy_vars():
    1 == 1
    {var_names}
    {deploy_vars}
"""

    @staticmethod
    def getFunctionVariableDeclaration(variable_name, value,  solver_name):
        """
        Generates code for declaring a variable and adding it to a Z3 solver instance.

        :param variable_name: The name of the variable to declare.
        :type variable_name: str
        :param value: The value to assign to the variable.
        :param solver_name: The name of the Z3 solver instance.
        :type solver_name: str
        :return: A string containing Python code for the variable declaration and solver addition.
        :rtype: str
        """

        partern = "r'[^\[\]{}()]*[^\[\]{}()\s]'"
        return f"""
    # Define a regular expression pattern to match variable names inside brackets or parentheses
    pattern = {partern}
    # Use re.search to find the first match in the expression
    match = re.search(pattern, "{variable_name.strip()}")
    
    # Check if the variable exists in locals() or globals()
    if match.group(0) in globals():
        # If the variable exists, create a valid assignment
        {variable_name} = {value}
        _tmp_ = {value}
        {solver_name}.add({variable_name} == _tmp_)
    else:
        raise NameError(f"State Variable '{{match.group(0)}}' does not exist")
"""

    @staticmethod
    def getMessageWhenVarNotGlobal(assignation_str, solver_name):
        """
        Generates a message indicating that a variable does not meet assignment requirements.

        :param assignation_str: The assignment string that failed to meet requirements.
        :type assignation_str: str
        :param solver_name: The name of the Z3 solver instance.
        :type solver_name: str
        :return: A string containing Python code to add a false condition to the solver.
        :rtype: str
        """

        return f"""
    #{assignation_str} do not meet the assignations requirements
    {solver_name}.add(False)              
            """