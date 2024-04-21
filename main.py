from translator import translate_line_by_line

file = input("Name of file to translate/run: ")
f = open(file, "r")
translated = translate_line_by_line(f.read())
out = open("translated.py", "w")
out.write(translated)
exec(translated)