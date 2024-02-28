
from Extension import generateFuntionsFormulas
from MessagesTemplates import MessagesTemplates

class Fbuilder :
    """
    Provides functionalities to build Z3 formulas models from transitions and save them into a file.
    """
    @staticmethod
    def build_z3_formulas_model_and_save(trGrinder, file_name, only_latest = False):
        """
        Builds a Z3 formulas model from the transitions processed by a TransactionsGrinder instance and saves it into a file.

        :param trGrinder: An instance of TransactionsGrinder containing processed transitions.
        :type trGrinder: TransactionsGrinder
        :param file_name: The name of the file where the Z3 model will be saved.
        :type file_name: str
        :param only_latest: If True, only the latest transition formula is included in the model, defaults to False.
        :type only_latest: bool, optional
        :return: The name of the file where the model is saved.
        :rtype: str
        """
        str_code = trGrinder.transition_processor.str_code
        #create formulas functions
        str_code += generateFuntionsFormulas() + "\n"
        with_log = False
        
        
        if trGrinder.non_stop:
            if not only_latest and trGrinder.log:
               with_log = True 

        elif trGrinder.log: 
            with_log = True
        else:
            with_log = True
        
        
        checks = []
        solvers = trGrinder.transition_processor.solvers
        if only_latest:
            solvers = {"latest":[trGrinder.transition_processor.latest]}

        for s in solvers:
           str_code += "\n\n"
           for item in solvers[s]:
                str_code += MessagesTemplates.getFunctionActionDefinition(item) + "\n"
                checks.append(f"{item['snameF']}({with_log})")
                
        str_code += f"try:\n    check_resut = (" + " and ".join(checks) + ")" + "\n"
        str_code += MessagesTemplates.getResultCheckPart() + "\n"
        str_code += "\nexcept Exception as e:\n    print(f\"Error in Z3 runner, could be state variable non declared, types not matching in assignment....: {e}\")"
        
        Fbuilder.save_infile(str_code, file_name)
        
        return file_name

    
    @staticmethod
    def save_infile(str_code, file_name = "str_code"):
        """
        Saves the given string code into a file.

        :param str_code: The string code to be saved.
        :type str_code: str
        :param file_name: The name of the file to save the code into, defaults to "str_code".
        :type file_name: str, optional
        """
        # Specify the file name with a .py extension
        file_name = f"{file_name}"

        # Open the file for writing and write the code
        with open(file_name, "w") as file:
            file.write(f"from z3 import * \n# setting path\nsys.path.append('../../') \nfrom TRAC.src.Extension import *\n\n{str_code}")