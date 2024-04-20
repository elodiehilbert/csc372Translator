from lineTest import translate_line_by_line

print("Type 'exit' to leave")
user = input()
while(user != "exit"):
    exec(translate_line_by_line(user))
    user = input()