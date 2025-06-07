from z3 import *
import re

formulas = {}

def is_in_set(value, set):
  """
  Checks if a given value is in a set using Z3 solver.

  :param value: The value to be checked for presence in the set.
  :param set: The set against which the value is checked.
  :return: Returns True if the value is found in the set, False otherwise.
  :rtype: bool
  """

  value = str(value)
  # Create a Z3 solver.
  solver = z3.Solver()

  # Create a strins variable for each element in the set and add rule it must be equal to value in array.
  set_elements = [z3.String('set_element_%d' % i) for i in range(len(set))]
  for i in range(len(set_elements)):
    solver.add(set_elements[i] == str(set[i]))

  # Create a constraint that the value is equal to one of the elements in the set.
  solver.add(z3.Or([value == set_element for set_element in set_elements]))

  # Check if the solver has a solution.
  return solver.check() == z3.sat
  
def exist_in_set(formula, set):
  """
  Checks if there exists an element in the set that satisfies a given formula using Z3 solver.

  :param formula: The condition or formula each element in the set is tested against.
  :param set: The collection of elements to be tested against the formula.
  :return: Returns True if at least one element in the set satisfies the given formula, False otherwise.
  :rtype: bool
  """

  solver = z3.Solver()
  # Create a strins variable for each element in the set and add rule it must be equal to value in array.
  set_elements = [z3.String('set_element_%d' % i) for i in range(len(set))]
  for i in range(len(set_elements)):
    solver.add(set_elements[i] == str(set[i]))

  # Create a constraint that the value is equal to one of the elements in the set.
  solver.add(z3.Or([formula(set_element) for set_element in set]))

  # Check if the solver has a solution.
  return solver.check() == z3.sat
  
def forall_in_set(formula, set):
  """
  Checks if all elements in the set satisfy a given formula using Z3 solver.

  :param formula: The condition or formula to test against each element in the set.
  :param set: The collection of elements to be evaluated against the formula.
  :return: Returns True if every element in the set satisfies the given formula, False otherwise.
  :rtype: bool
  """

  solver = z3.Solver()
  # Create a strins variable for each element in the set and add rule it must be equal to value in array.
  set_elements = [z3.String('set_element_%d' % i) for i in range(len(set))]
  for i in range(len(set_elements)):
    solver.add(set_elements[i] == str(set[i]))

  # Create a constraint that the value is equal to one of the elements in the set.
  solver.add(z3.And([formula(set_element) for set_element in set]))

  # Check if the solver has a solution.
  return solver.check() == z3.sat

# Function to parse and replace assertions
def replace_assertion(assertion): 
    """
    Parses and replaces assertions within a given string with appropriate function calls for evaluation.

    :param assertion: The assertion string to be parsed and modified.
    :type assertion: str
    :return: A modified version of the assertion string where assertions have been replaced with function calls suitable for evaluation.
    :rtype: str
    """

    # Define a replacement function for re.sub

    def replace(match):
        if match.group(1) == 'in':
            return f'is_in_set({match.group(2)}, {match.group(3)})'
        if match.group(1) == 'sum':
            bound =  match.group(3) if match.group(3) else 100
            if bound == "0" or not is_int(bound):
               bound = 2
            return f'Sum([If(And(i >= 0, i < {bound}), Select({match.group(2)}, i), 0) for i in range({bound})])'
        elif match.group(1) == 'exist':
            set_name = match.group(2)
            formula = match.group(3)
            # Define a function to evaluate the formula
            formula_function = f"formula_{len(formulas)}"
            formulas[formula_function] = formula
            return f'exist_in_set({formula_function}, {set_name})'
        elif match.group(1) == 'forall':
            set_name = match.group(2)
            formula = match.group(3)
            # Define a function to evaluate the formula
            formula_function = f"formula_{len(formulas)}"
            formulas[formula_function] = formula
            return f'forall_in_set({formula_function}, {set_name})'
        else:
            return match.group(0)

    # Use re.sub with the replacement function to replace all occurrences
    assertion = re.sub(r'(in|exist|forall|sum)\((.*?),(.*?)\)', replace, assertion.replace(" ", ""))

    return assertion

def generateFuntionsFormulas():
  """
  Generates Python function definitions for formulas stored in a global `formulas` dictionary. Each formula is turned into a Python function that can be evaluated.

  :return: A string containing Python code with generated function definitions for each formula.
  :rtype: str
  """

  code = ""
  for name in formulas:
    code += f"""\n
def {name}(item):
  solver = z3.Solver()
  solver.add({formulas[name]})
  return solver.check() == z3.sat
  """
  return code
