import re


def translate_to_python(code):
    # Regex patterns
    # string_pattern = r'\"(.*?)\"'
    assignment_pattern =  r'(?<!\")\b(x|b|s|l)\s*(\w+)\s*is\s*([^;]+)(?!\")'
    variable_pattern = r'\b(x|b|s|l)(\w+)'
    for_loop_pattern = r'for\s*\((.*?)\)\s*\{\s*([\s\S]*?)\s*\}'
    while_loop_pattern = r'while\s*\((.*?)\)\s*\{\s*([\s\S]*?)\s*\}'
    if_smt_pattern = r'if\s*\((.*?)\)\s*\{\s*([\s\S]*?)\s*\}(?:\s*else\s*\{\s*([\s\S]*?)\s*\})?'
    output_pattern = r'out\("(.*?)"\)|out\((.*?)\)'
    input_pattern = r'in\("(.*?)"\)'
    bool_expr_pattern = r'(?<![\w\d])\b([a-zA-Z0-9_]+)\b\s*(<=|>=|!=|<|>)\s*([a-zA-Z0-9_]+)\b(?![\w\d])'
    int_expr_pattern = r'(?<![\w\d])\b(\d+)\b|(?!x|b|s|l)(.*?)\s*([-+*/])\s*(.*?)\b(?![\w\d])'
    list_expr_pattern = r'\[(.*?)\]'



    # Translate assignments
    code = re.sub(assignment_pattern, lambda m: translate_assignment(m), code)

    # Translate variables
    code = re.sub(variable_pattern, lambda m: translate_variable(m), code)

    # Translate loops
    code = re.sub(for_loop_pattern, lambda m: translate_for_loop(m), code)
    code = re.sub(while_loop_pattern, lambda m: translate_while_loop(m), code)

    # Translate if statements
    code = re.sub(if_smt_pattern, lambda m: translate_if_smt(m), code)

    # Translate output and input
    code = re.sub(output_pattern, lambda m: translate_output(m), code)
    code = re.sub(input_pattern, lambda m: translate_input(m), code)

    # Translate expressions
    code = re.sub(bool_expr_pattern, lambda m: translate_bool_expr(m), code)
    code = re.sub(int_expr_pattern, lambda m: translate_int_expr(m), code)
    code = re.sub(list_expr_pattern, lambda m: translate_list_expr(m), code)

    return code


def translate_assignment(match):
    var_type, var_name, value = match.groups()
    if var_type == 'x':
        try:
            int(value)
        except ValueError as e:
            raise Exception("ERROR: x variable must be int.") from e
        return f'{var_type + var_name} = {value}'
    elif var_type == 'b':
        if value != '0' and value != '1':
            raise Exception("ERROR: b variable must be 0(False) or 1(True).")
        if value == "1":
            return f'{var_type + var_name} = bool(True)'
        elif value == "0":
            return f'{var_type + var_name} = bool(False)'
        else:
            return f'{var_type + var_name} = bool({value})'
    elif var_type == 's':
        if value != '"':
            raise Exception("ERROR: s variable must be string.")
        return f'{var_type + var_name} = {value}'
    elif var_type == 'l':
        return f'{var_type + var_name} = [{value}]'


def translate_variable(match):
    var_type, var_name = match.groups()
    return f'{var_type+ var_name}'


def translate_for_loop(match):
    condition, body = match.groups()
    return f'for {condition}:\n{indent(translate_to_python(body), 4)}'


def translate_while_loop(match):
    condition, body = match.groups()
    return f'while {condition}:\n{indent(translate_to_python(body), 4)}'


def translate_if_smt(match):
    condition, true_body, false_body = match.groups()
    true_body = indent(translate_to_python(true_body), 4)
    false_body = indent(translate_to_python(false_body), 4)
    return f'if {condition}:\n{true_body}\nelse:\n{false_body}'


def translate_output(match):
    if match.group(1):
        return f'print("{match.group(1)}")'
    else:
        return f'print({match.group(2)})'


def translate_input(match):
    prompt = match.group(1)
    return f'input("{prompt}")'


def translate_bool_expr(match):
    if match.group(1):
        return str(match.group())
    else:
        left, op, right = match.groups()[1:]
        left = translate_to_python(left)
        right = translate_to_python(right)
        return f'{left} {op} {right}'


def translate_int_expr(match):
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


def run_code(code):
    exec(code)


if __name__ == '__main__':
    input_code = """
xNum is 5
out(xNum)
sStr is "Hello"
out(sStr)
bBool is 1
out(bBool)
"""
    python_code = translate_to_python(input_code)
    print(input_code)
    print(python_code)
    run_code(python_code)