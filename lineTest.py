from translator import translate_to_python
import re

assignment_pattern =  r'(?<!\")\b(x|b|s|l)\s*(\w+)\s*is\s*(.+?)(?!\")'
variable_pattern = r'\b(x|b|s|l)(\w+)'
for_loop_pattern = r'for\(\s*(.*?)\;\s*(.*?)\;\s*(.*?)\)\s*\{'
while_loop_pattern = r'while\s*\((.*?)\)\s*\{\s*'
if_smt_pattern = r'if\s*\((.*?)\)\s*\{\s*'
else_smt_pattern = r'else\s*\{'
output_pattern = r'out\("(.*?)"\)|out\((.*?)\)'
input_pattern = r'(\w+)\s*is\s*in\("(.*?)"\)'
bool_expr_pattern = r'(?<![\w\d])\b([a-zA-Z0-9_]+)\b\s*(<=|>=|!=|<|>)\s*([a-zA-Z0-9_]+)\b(?![\w\d])'
int_expr_pattern = r'(?<![\w\d])\b(\d+)\b|(?!x|b|s|l)(.*?)\s*([-+*/])\s*(.*?)\b(?![\w\d])'
list_expr_pattern = r'\[(.*?)\]'

def translate_line_by_line(code):
        lines = code.split("\n")
        indent = 0
        output = ""
        endings = []
        for line in lines:
                # Remove indents if it is ending an indented block thing
                if line.find("}") != -1:
                        line = line.replace("}", "")
                        if(len(endings) > 0):
                             index = len(endings) - 1
                             output += ("\t" * indent) + endings[index] + "\n"
                             endings.remove(endings[index])
                        indent -= 1
                

                output += "\t" * indent
        
                # Translate assignments
                line = re.sub(assignment_pattern, lambda m: translate_assignment(m), line)

                # Translate variables
                line = re.sub(variable_pattern, lambda m: translate_variable(m), line)

                # # Translate output and input
                line = re.sub(output_pattern, lambda m: translate_output(m), line)
                line = re.sub(input_pattern, lambda m: translate_input(m), line)

                # # Translate expressions
                # line = re.sub(bool_expr_pattern, lambda m: translate_bool_expr(m), line)
                # line = re.sub(int_expr_pattern, lambda m: translate_int_expr(m), line)
                # line = re.sub(list_expr_pattern, lambda m: translate_list_expr(m), line)

                # Translate loops
                if(re.search(while_loop_pattern, line)):
                        line = re.sub(while_loop_pattern, lambda m: translate_while_loop(m), line)
                        indent += 1

                if(re.search(for_loop_pattern, line)):
                        init, condition, every = re.match(for_loop_pattern, line).groups()
                        real_line = init + "\n" + ("\t" * indent)
                        real_line += "while " + condition + ":"
                        line = real_line
                        endings.append(every)
                        indent += 1

                # Translate if statements
                if(re.search(if_smt_pattern, line)):
                        line = re.sub(if_smt_pattern, lambda m: translate_if_smt(m), line)
                        indent += 1

                # Translate else statements
                if(re.search(else_smt_pattern, line)):
                        line = re.sub(else_smt_pattern, lambda m: translate_else_smt(m), line)
                        indent += 1

                line = line.lstrip()
                output += line + "\n"

        return output

def translate_assignment(match):
    var_type, var_name, value = match.groups()
    if var_type == 'x':
        return f'{var_type + var_name} = {value}'
    elif var_type == 'b':
        if value == "1":
            return f'{var_type + var_name} = bool(True)'
        elif value == "0":
            return f'{var_type + var_name} = bool(False)'
        else:
            return f'{var_type + var_name} = bool({value})'
    elif var_type == 's':
        return f'{var_type + var_name} = {value}'
    elif var_type == 'l':
        return f'{var_type + var_name} = [{value}]'

def translate_variable(match):
    var_type, var_name = match.groups()
    return f'{var_type+ var_name}'


def translate_for_loop(match):
    init, condition, every = match.groups()
    return f'for {condition}:\n{indent(translate_to_python(body), 4)}'


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
    var_name, prompt = match.groups()
    return f'{var_name} = input("{prompt}")'


def translate_bool_expr(match):
    if match.group(1):
        return str(match.group())
    else:
        left, op, right = match.groups()[1:]
        left = translate_to_python(left)
        right = translate_to_python(right)
        return f'{left} {op} {right}'


def translate_int_expr(match):
    print(match.groups())
    if match.group(1):
        return match.group(1)
    else:
        left, op, right = match.groups()[1:]
        left = translate_to_python(left)
        right = translate_to_python(right)
        return f'{left} {op} {right}'


def translate_list_expr(match):
    values = match.group(1).split(',')
    return f'[{", ".join(translate_to_python(v) for v in values)}]'

def indent(code, spaces=4):
    indent_str = ' ' * spaces
    return indent_str + ('\n' + indent_str).join(code.split('\n'))

input_code = """
xNum is 5
out(xNum)
                sStr is "Hello"
out(sStr)
        bBool is 1

while(xNum < 10){
        xNum += 1
}
        
                        if(xNum == 10){
        out(5)
                        } else{
                        out(10)
                        }
        out(bBool)

for(xVal = 0; xVal < 5; xVal += 1){
        out(xVal)
}
"""
expected_python_code = """
xNum = 5
print(xNum)
sStr = "Hello"
print(sStr)
bBool = bool(1)
print(bBool)
"""

print(translate_line_by_line(input_code))
exec(translate_line_by_line(input_code))