from pprint import pprint
import re

def remove_comments(text):
    # Remove single-line comments (// ...)
    text = re.sub(r'//.*', '', text)
    # Remove multi-line comments (/* ... */)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def extract_transitions(text: str):
    # Match pattern: [from] ... [to]
    pattern = re.compile(r"\[(\w+\+?)\](.*?)\[(\w+\+?)\]", re.DOTALL)

    transitions = []
    for match in pattern.finditer(text):
        from_state = match.group(1)
        data = match.group(2)
        to_state = match.group(3)

        # Clean the data: remove newlines, excessive spaces
        cleaned_data = ' '.join(data.strip().split())

        # Format result
        transition_line = f"[{from_state}] {cleaned_data} [{to_state}]"
        transitions.append(transition_line)
    return transitions


def extract_braces_content(text):
    # This pattern matches everything between { and }, non-greedy
    pattern = r'\{(.*?)\}'
    matches = re.findall(pattern, text, flags=re.DOTALL)
    return [match.strip() for match in matches if match.strip()]

def parse_transitions(input_text_list, contract_name: str, roles: list[str]):
    transition_pattern_with_guard = re.compile(
        r"\[(\w+\+?)\]\s*(?:\{(.*?)\})?\s*(?:(new|any)?\s*(\w+))?\s*\s*(\w+)?\s*>\s*(\w+)\((.*?)\)\s*(\{.*?\})?\s*\[(\w+\+?)\]"
    )

    # Rebuild output lines with guard support
    transitions = []
    for input_text in input_text_list:
        match = transition_pattern_with_guard.findall(input_text)
        if not match :
            raise Exception(f"Error parsing transition : {input_text}")
        source, guard, party_type, role, party_name, op, param_str, assigns, target = match[0]
        
        if (not role and not party_name) or (party_type and role and not party_name) :
            raise Exception(f"Error parsing transition : {input_text}")
       
        if role and not party_name:
            party_name = role 
            role = ""
       
        if assigns:
            assigns = assigns.replace("{", "").replace("}", "")
        # Construct participant string
        participant_str = f"{party_name}".strip() if party_type == "new" or not party_type else f"{party_type} {party_name}".strip()

        # Format parameters (support participant roles)
        formatted_params = []
        for param in param_str.split(','):
            param = param.strip()
            if not param:
                continue
            parts = param.split()
            if len(parts) == 2:
                typ, var = parts
                if typ in roles:
                    formatted_params.append(f"participant {typ} {var}")
                else:
                    formatted_params.append(f"{typ} {var}")
            else:
                formatted_params.append(param)


        # Format assignments
        assign_list = [a.strip() for a in assigns.split(';') if a.strip()]
        assign_str = ' & '.join(assign_list)

        # Format transition line
        transition_line = f"{source}"
        if guard:
            transition_line += f" {{{guard}}}"
        else :
            transition_line += f" {{True}}"
        transition_line += f" {participant_str}"
        if role:
            transition_line += f":{role}"
        transition_line += f" > {contract_name}.{op}({', '.join(formatted_params)})"
        transition_line += f" {{{assign_str}}} {target}"
        transitions.append(transition_line.strip())

    return transitions

class DafsnSyntaxPerser :
    @staticmethod
    def parse(input_text: str) -> str :
        input_text = remove_comments(input_text)
        # 1. Parse roles
        lines = input_text.strip().splitlines()
        roles_line = lines[0]
        roles = roles_line.split()[1:]

        # 2. Parse dafsm header
        header_line = lines[1]
        header_match = re.match(r"dafsm (\w+)\((.*?)\) by (\w+) (\w+)", header_line)
        contract_name, params_str, caller_role, caller = header_match.groups()

        if not caller_role in roles :
            raise Exception(f"{caller_role} should be in the list of roles {roles}")
        
        # 3. Format parameters
        params = []
        for param in params_str.split(','):
            param = param.strip()
            if not param:
                continue
            typ, var = param.split()
            if typ in roles:
                param_fmt = f"participant {typ} {var}"
            else:
                param_fmt = f"{typ} {var}"
            params.append(param_fmt)

        # 4. Extract assignments, declarations, and guard
        _blocks = extract_braces_content(input_text.split("[")[0])
        assignments_block = []
        assignments = []
        typed_vars = {}
        guard = "True"
       
        if _blocks :
            guard_lines = _blocks[0].strip().split("if")
            if guard_lines:
                assignments_block = guard_lines[0].strip().replace("\n", "").split(";")
                if len(guard_lines) == 2 :
                    guard = re.search(r"if (.*)", f"if {guard_lines[1]}").group(1)
                              
        for line in assignments_block:
            line = line.strip()
            if ":=" in line:
                match = re.match(r"(.*?) (.*?) *:= *(.*)", line)
                if match:
                    typ, var, expr = match.groups()
                    assignments.append(f"{var}:= {expr}")
                    typed_vars[var] = typ
            elif re.match(r"(.*?) (.*);", line):
                match = re.match(r"(.*?) (.*);", line)
                if match:
                    typ, var = match.groups()
                    typed_vars[var.strip()] = typ.strip()
        # 5. Generate variable type list (all declared variables)
        types = [f"{typ} {var}" for var, typ in typed_vars.items()]

        # 6. Extract initial state
        initial_state = re.search(r"\[(\w+)\]", input_text).group(1)

        # 7. Format initial transition
        initial_line = f"_ {{{guard}}} {caller}:{caller_role} > starts({contract_name}, {', '.join(params)}) "
        initial_line += "{" + '  &  '.join(assignments) + "} "
        initial_line += "{" + '; '.join(types) + "} "
        initial_line += f"{initial_state}"

        
        
        # 8. Parse and format regular transitions
        transitions = parse_transitions(extract_transitions(input_text), contract_name, roles)
        
        
        return ("\n".join([initial_line] + transitions))
