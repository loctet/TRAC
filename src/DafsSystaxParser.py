import re

class DafsnSyntaxPerser :
    @staticmethod
    def parse(input_text: str) -> str :
        # 1. Parse roles
        lines = input_text.strip().splitlines()
        roles_line = lines[0]
        roles = roles_line.split()[1:]

        # 2. Parse dafsm header
        header_line = lines[1]
        header_match = re.match(r"dafsm (\w+)\((.*?)\) by (\w+) ?: (\w+)", header_line)
        contract_name, params_str, caller, caller_role = header_match.groups()

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
        assignments_block = lines[2:7]
        assignments = []
        typed_vars = {}
        guard = ""

        for line in assignments_block:
            line = line.strip()
            if ":=" in line:
                match = re.match(r"(.*?) (.*?) *:= *(.*);", line)
                if match:
                    typ, var, expr = match.groups()
                    assignments.append(f"{var}:= {expr}")
                    typed_vars[var] = typ
            elif re.match(r"(.*?) (.*);", line):
                match = re.match(r"(.*?) (.*);", line)
                if match:
                    typ, var = match.groups()
                    typed_vars[var.strip()] = typ.strip()
            elif re.match(r"if (.*)", line):
                guard = re.search(r"if (.*)", line).group(1)

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
        transition_pattern_with_guard = re.compile(
            r"\[(\w+\+?)\]\s*(?:\{(.*?)\})?\s*(?:(new|any)?\s*(\w+))?\s*:?\s*(\w+)?\s*>\s*(\w+)\((.*?)\)\s*\{(.*?)\}\s*\[(\w+\+?)\]"
        )

        # Rebuild output lines with guard support
        output_lines = []

        for match in transition_pattern_with_guard.findall(input_text):
            source, guard, party_type, party_name, role, op, param_str, assigns, target = match

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
            output_lines.append(transition_line.strip())

        return ("\n".join([initial_line] + output_lines))
