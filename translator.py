# global_vars = {}
#
# def parse_code(code):
#     lines = code.split('\n')
#     global_vars = {}
#     for line in lines:
#         line = line.strip()
#         if line:
#             exec(parse_line(line), global_vars)
#
# def parse_line(line):
#     tokens = line.split()
#     if tokens[0] == 'out':
#         arg = parse_output_arg(tokens[0][4:-1], global_vars)
#         return f"print({arg})"
#     elif len(tokens) >= 3 and tokens[1] == 'is':
#         var_type = tokens[0][0]
#         var_name = tokens[0][1:]
#         value = parse_expr(var_type, tokens[2:], global_vars)
#         return f"{var_name} = {value}"
#     elif tokens[0] == 'in':
#         var_name = tokens[1]
#         prompt = ' '.join(tokens[3:])[1:-1]
#         return f"{var_name} = input('{prompt}')"
#     elif tokens[0] == 'for':
#         init = parse_line(' '.join(tokens[1:tokens.index(';')])) + ';'
#         condition = parse_bool_expr(' '.join(tokens[tokens.index(';') + 1:tokens.index('{')])) + ';'
#         update = parse_line(' '.join(tokens[tokens.index('{') + 1:-1])) + ';'
#         body = '\n'.join([parse_line(' '.join(tokens[tokens.index('{') + 1:-1]))])
#         return f"for {init}\n    if not {condition}:\n        break\n    {body}\n    {update}"
#     elif tokens[0] == 'if':
#         condition = parse_bool_expr(' '.join(tokens[1:tokens.index(')')]))
#         true_body = '\n'.join([parse_line(' '.join(tokens[tokens.index('{') + 1:tokens.index('}')]))])
#         false_body = '\n'.join([parse_line(' '.join(tokens[tokens.index('}') + 2:-1]))])
#         return f"if {condition}:\n    {true_body}\nelse:\n    {false_body}"
#     else:
#         raise ValueError(f"Invalid token: {tokens[0]}")
#
# def parse_output_arg(arg, global_vars):
#     if arg.startswith('"'):
#         return arg
#     else:
#         return f"global_vars['{arg}']"
#
# def parse_expr(var_type, tokens, global_vars):
#     if '"' in tokens:
#         value = '"' + ' '.join(tokens[tokens.index('"') + 1:tokens.index('"', tokens.index('"') + 1)]) + '"'
#         if var_type == 'x':
#             raise ValueError("Cannot assign string to integer variable")
#         elif var_type == 'b':
#             raise ValueError("Cannot assign string to boolean variable")
#         return value
#     elif any(char.isdigit() for char in tokens[0]) or (tokens[0].startswith('-') and any(char.isdigit() for char in tokens[0][1:])):
#         value = tokens[0]
#         if var_type == 'b':
#             return 'True' if value != '0' else 'False'
#         return value
#     else:
#         return f"global_vars['{tokens[0]}']"
#
# def parse_bool_expr(expr, global_vars):
#     tokens = expr.split()
#     expr = parse_expr('b', tokens, global_vars)
#     while tokens and tokens[0] in ('<', '>', '=', '!', '='):
#         op = tokens.pop(0)
#         if op == '=':
#             op = '=='
#         elif op == '!=':
#             op = '!='
#         expr = f"{expr} {op} {parse_expr('b', tokens, global_vars)}"
#     return expr
#
# # Example usage
# input_code = """
# xNum is 5
# out (xNum)
# """
# parse_code(input_code)


global_vars = {}

def parse_code(code):
    lines = code.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            exec(parse_line(line))

def parse_line(line):
    tokens = line.split()
    if tokens[0] == 'out(':
        arg = parse_output_arg(tokens[0][4:-1])
        return f"print({arg})"
    elif len(tokens) >= 3 and tokens[1] == 'is':
        var_type = tokens[0][0]
        var_name = tokens[0][1:]
        value = parse_expr(var_type, tokens[2:])
        global global_vars
        global_vars[var_name] = eval(value)
        return f"{var_name} = {value}"
    elif tokens[0] == 'in':
        var_name = tokens[1]
        prompt = ' '.join(tokens[3:])[1:-1]
        global global_vars
        global_vars[var_name] = input(prompt)
        return f"{var_name} = input('{prompt}')"
    elif tokens[0] == 'for':
        init = parse_line(' '.join(tokens[1:tokens.index(';')])) + ';'
        condition = parse_bool_expr(' '.join(tokens[tokens.index(';') + 1:tokens.index('{')])) + ';'
        update = parse_line(' '.join(tokens[tokens.index('{') + 1:-1])) + ';'
        body = '\n'.join([parse_line(' '.join(tokens[tokens.index('{') + 1:-1]))])
        return f"for {init}\n    if not {condition}:\n        break\n    {body}\n    {update}"
    elif tokens[0] == 'if':
        condition = parse_bool_expr(' '.join(tokens[1:tokens.index(')')]))
        true_body = '\n'.join([parse_line(' '.join(tokens[tokens.index('{') + 1:tokens.index('}')]))])
        false_body = '\n'.join([parse_line(' '.join(tokens[tokens.index('}') + 2:-1]))])
        return f"if {condition}:\n    {true_body}\nelse:\n    {false_body}"
    else:
        raise ValueError(f"Invalid token: {tokens[0]}")

def parse_output_arg(arg):
    if arg.startswith('"'):
        return arg
    else:
        global global_vars
        return f"global_vars['{arg}']"

def parse_expr(var_type, tokens):
    if '"' in tokens:
        value = '"' + ' '.join(tokens[tokens.index('"') + 1:tokens.index('"', tokens.index('"') + 1)]) + '"'
        if var_type == 'x':
            raise ValueError("Cannot assign string to integer variable")
        elif var_type == 'b':
            raise ValueError("Cannot assign string to boolean variable")
        return value
    elif any(char.isdigit() for char in tokens[0]) or (tokens[0].startswith('-') and any(char.isdigit() for char in tokens[0][1:])):
        value = tokens[0]
        if var_type == 'b':
            return 'True' if value != '0' else 'False'
        return value
    else:
        global global_vars
        return f"global_vars['{tokens[0]}']"

def parse_bool_expr(expr):
    tokens = expr.split()
    expr = parse_expr('b', tokens)
    while tokens and tokens[0] in ('<', '>', '=', '!', '='):
        op = tokens.pop(0)
        if op == '=':
            op = '=='
        elif op == '!=':
            op = '!='
        expr = f"{expr} {op} {parse_expr('b', tokens)}"
    return expr

# Example usage
input_code = """
xNum is 5
out(xNum)
"""
parse_code(input_code)
print(global_vars)