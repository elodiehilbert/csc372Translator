import random
import string
import re

assignment_pattern =  r'(?<!\")\b(x|b|s|l)\s*(\w+)\s*is\s*([^;]+)(?!\")'
invalid_assignment_pattern = r'(?<!\")\s*\b(x|b|s|l)\s*(\w+)\s*=\s*([^;]+)(?!\")'
variable_pattern = r'\b(x|b|s|l)(\w+)'
for_loop_pattern = r'for\s*\(\s*(.*)\;\s*(.*)\;\s*(.*)\)\s*\{'
while_loop_pattern = r'while\s*\((.*?)\)\s*\{\s*'
if_smt_pattern = r'if\s*\((.*?)\)\s*\{\s*'
else_smt_pattern = r'else\s*\{'
output_pattern = r'out\("(.*?)"\)|out\((.*?)\)'
input_pattern = r'in\("(.*?)"\)'
function_pattern = r'\s*(f\w+)\s*(\(.*\))\s*{'
curry_pattern = r'^\s*(f\w+)\s*([^(){]*)\s*{'
curry_call = r'(f\w+)\s*([\w ]*)'

def translate_line_by_line(code):
    lines = code.split("\n")
    indent = 0
    output = ""
    extra = 0
    endings = []
    for line in lines:
        # Remove indents if it is ending an indented block thing
        if line.find("}") != -1:
            line = line.replace("}", "")
            if extra > 0 and endings[len(endings) - 1] != "":
                for j in range(extra):
                        indent -= 1
                        index = len(endings) - 1
                        output += ("\t" * indent) + endings[index] + "\n"
                        endings.remove(endings[index])
                extra = 0
                indent -= 1
            else:
                index = len(endings) - 1
                output += ("\t" * indent) + endings[index] + "\n"
                endings.remove(endings[index])
                indent -= 1                

        # Add indents to start of line
        output += "\t" * indent

        # Check for unclosed string
        if (line.count("\"") - line.count("\\\"")) % 2 != 0:
            raise SyntaxError("Unclosed string at\n" + line)

        # Catch invalid assignments:
        if(re.match(invalid_assignment_pattern, line)):
            raise SyntaxError("Invalid variable assignment, use 'is' instead of '=' at\n" + line)

        # Translate assignments
        line = re.sub(assignment_pattern, lambda m: translate_assignment(m), line)

        # Translate variables
        line = re.sub(variable_pattern, lambda m: translate_variable(m), line)

        # # Translate output and input
        line = re.sub(output_pattern, lambda m: translate_output(m), line)
        line = re.sub(input_pattern, lambda m: translate_input(m), line)

        # Translate while loops
        if(re.search(while_loop_pattern, line)):
            line = re.sub(while_loop_pattern, lambda m: translate_while_loop(m), line)
            endings.append("")
            indent += 1

        # Translate for loop
        if(re.search(for_loop_pattern, line)):
            init, condition, every = re.search(for_loop_pattern, line).groups()
            real_line = init + "\n" + ("\t" * indent)
            real_line += "while " + condition + ":"
            line = real_line
            endings.append(every)
            indent += 1

        # Translate if statements
        if(re.search(if_smt_pattern, line)):
            line = re.sub(if_smt_pattern, lambda m: translate_if_smt(m), line)
            endings.append("")
            indent += 1

        # Translate else statements
        if(re.search(else_smt_pattern, line)):
            line = re.sub(else_smt_pattern, lambda m: translate_else_smt(m), line)
            endings.append("")
            indent += 1

        # Translate function heads
        if(re.search(function_pattern, line)):
            line = re.sub(function_pattern, lambda m: translate_function_head(m), line)
            endings.append("")
            indent += 1

        # Translate curry function heads
        if(re.search(curry_pattern, line)):
            name, args = re.search(curry_pattern, line).groups()
            args = args.split()
            real_line = "\t" * indent
            indent += 1
            if(len(args) == 0):
                real_line += f'def {name}():'
                endings.append("")
            else:
                real_line += f'def {name}({args[0]}):'
                
                for j in range(1, len(args)):
                    real_line += '\n' + ("\t" * indent)
                    fname = ''.join(random.choices(string.ascii_letters, k = 10))
                    real_line += f'def {fname}({args[j]}):'
                    endings.append(f'return {fname}')
                    extra += 1
                    indent += 1
            line = real_line

        # Translate curry function calls
        if(re.search(curry_call, line)):
            line = re.sub(curry_call, lambda m: translate_curry_call(m), line)

        line = line.lstrip()
        output += line + "\n"

    # Check for unclosed brackets
    if(indent != 0):
            raise SyntaxError("Unclosed Brackets")
    return output

def translate_assignment(match):
    var_type, var_name, value = match.groups()
    if var_type == 'x':
        if re.match(r'in\(.*\)|x\w+', value) == None:   
            try:
                int(value)
            except ValueError as e:
                raise Exception("ERROR: x variable must be int.") from e
        return f'{var_type + var_name} = int({value})'
    elif var_type == 'b':
        if re.match(r'in\(.*\)|s\w+|"[^"]*"', value) != None:
            raise Exception("ERROR: b variable must be boolean.")
        if value == "1":
            return f'{var_type + var_name} = bool(True)'
        elif value == "0":
            return f'{var_type + var_name} = bool(False)'
        else:
            return f'{var_type + var_name} = bool({value})'
    elif var_type == 's':
        if re.match(r'in\(.*\)|s\w+|"[^"]*"', value) == None:
            raise Exception("ERROR: s variable must be string.")
        return f'{var_type + var_name} = {value}'
    elif var_type == 'l':
        return f'{var_type + var_name} = [{value}]'

def translate_variable(match):
    var_type, var_name = match.groups()
    return f'{var_type+ var_name}'

def translate_while_loop(match):
    condition = match.group(1)
    return f'while {condition}:'

def translate_if_smt(match):
    condition = match.group(1)
    return f'if {condition}:'

def translate_else_smt(match):
    return "else:"

def translate_output(match):
    if match.group(1):
        return f'print("{match.group(1)}")'
    else:
        return f'print({match.group(2)})'

def translate_input(match):
    prompt = match.group(1)
    return f'input("{prompt}")'

def translate_curry_call(match):
        name, args = match.groups()
        output = name
        args = args.split()
        for arg in args:
            output+= f'({arg})'
        return output

def translate_function_head(match):
    name, args = match.groups()
    return f'def {name}{args}:'
