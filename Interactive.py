from translator import translate_line_by_line
import re

print("Type 'exit' to leave and open(\"File_name\") to run a file")
user = input()
while(user != "exit"):
    if(re.match(r'open\("([^"]+)"\)', user)):
        fileName = re.match(r'open\("([^"]+)"\)', user).group(1)
        exec(translate_line_by_line(open(fileName, "r").read()))
    else:
        exec(translate_line_by_line(user))
    user = input()