from translator import translate_line_by_line
import re

input = """xNum is 5
        xTwo is 2
                out(xTwo)
        while(xNum > 1){
    out(xNum)
            xNum -= 1
        }"""

translated = translate_line_by_line(input)
print(translated)
