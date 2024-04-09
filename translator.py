import re


def translate_to_python(code):
    # Regex patterns
    assignment_pattern = r'(x|b|s|l)\s*(\w+)\s*is\s*(.+)'
    for_loop_pattern = r'for\((.*?)\s*(.*?)\;\s*(.*?)\)\{(.*?)\}'
    while_loop_pattern = r'while\((.*?)\)\{(.*?)\}'
    if_smt_pattern = r'if\((.*?)\)\s*then\s*\{(.*?)\}\s*else\s*\{(.*?)\}'
    output_pattern = r'out\("(.*?)"\)|out\((.*?)\)'
    input_pattern = r'(\w+)\s*is\s*in\("(.*?)"\)'
    bool_expr_pattern = r'(0|1)|(.*?)\s*(<=|>=|!=|<|>)\s*(.*?)'
    int_expr_pattern = r'(\d+)|(.*?)\s*([-+*/])\s*(.*?)'
    list_expr_pattern = r'\[(.*?)\]'

    # Translate assignments
    code = re.sub(assignment_pattern, lambda m: translate_assignment(m), code)

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
        return f'{var_name} = {value}'
    elif var_type == 'b':
        return f'{var_name} = bool({value})'
    elif var_type == 's':
        return f'{var_name} = "{value}"'
    elif var_type == 'l':
        return f'{var_name} = [{value}]'


def translate_for_loop(match):
    init, condition, update, body = match.groups()
    return f'for {init}; {condition}; {update}:\n{indent(translate_to_python(body), 4)}'


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
    var_name, prompt = match.groups()
    return f'{var_name} = input("{prompt}")'


def translate_bool_expr(match):
    if match.group(1):
        return str(bool(int(match.group(1))))
    else:
        left, op, right = match.groups()[1:]
        left = translate_to_python(left)
        right = translate_to_python(right)
        return f'({left} {op} {right})'


def translate_int_expr(match):
    if match.group(1):
        return match.group(1)
    else:
        left, op, right = match.groups()[1:]
        left = translate_to_python(left)
        right = translate_to_python(right)
        return f'({left} {op} {right})'


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
out(Num)
"""
    python_code = translate_to_python(input_code)
    print(python_code)
    run_code(python_code)
