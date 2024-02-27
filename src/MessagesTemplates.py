class MessagesTemplates:
    
    @staticmethod
    def getFunctionActionDefinition(funtionData):
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
            print("--For {item['snameF']}: ", ({item['sformula']}), " :: ", result)

        if not part_result :
            print(f"--- Participants       : {{part_result}}", "({item['sparticipants']})")

        if  not eps_result :
            print ("--- Non Determinism  : ", ({item['epsformula']}))
            
        if not post_result: 
            print(f"--- Sat of Prec-Conds: {{post_result}}")
            solver_{item['snameF']}2.add(Not({item['sformula']}))
            print("\\nSimplify of the Not Formula: ", simplify(Not({item['sformula']})), " :: ", solver_{item['snameF']}2.check() == z3.sat)
            
          
                   
    return result
    """
    
    @staticmethod
    def getResultCheckPart():
        return f"""
    print("\\n(!) Verdict: "+ ("Well Formed" if  check_resut == True else "Not Well Formed"))
        """
        
    @staticmethod
    def getResetGlobalFunction(deploy_vars, var_names = []):
        var_names = ("global " + ", ".join(var_names)) if len(var_names) > 0 else ""
        return f"""
def reset_deploy_vars():
    1 == 1
    {var_names}
    {deploy_vars}
"""

    @staticmethod
    def getFunctionVariableDeclaration(variable_name, value,  solver_name):
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
        return f"""
    #{assignation_str} do not meet the assignations requirements
    {solver_name}.add(False)              
            """