
from Extension import generateFuntionsFormulas
from MessagesTemplates import MessagesTemplates

class Fbuilder :
    @staticmethod
    def build_z3_formulas_model_and_save(trGrinder, file_name, only_latest = False):
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
        # Specify the file name with a .py extension
        file_name = f"{file_name}"

        # Open the file for writing and write the code
        with open(file_name, "w") as file:
            file.write(f"from z3 import * \n# setting path\nsys.path.append('../../') \nfrom TRAC.src.Extension import *\n\n{str_code}")