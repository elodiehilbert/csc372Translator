import io
import sys
import unittest
from translator import translate_to_python, run_code

class TestTranslator(unittest.TestCase):
    def  test_translate_while_expression(self):
        input_code = """  """
        expected_output = """  """
        self.assertEqual(translate_to_python(input_code), expected_output)

#     def test_translate_to_python(self):
#         input_code = """
#         xNum is 5
#         out(xNum)
#         sStr is "Hello"
#         out(sStr)
#         bBool is 1
#         out(bBool)
#         """
#         expected_python_code = """
#         xNum = 5
#         print(xNum)
#         sStr = "Hello"
#         print(sStr)
#         bBool = bool(True)
#         print(bBool)
#         """
#         self.assertEqual(translate_to_python(input_code), expected_python_code)

#     def test_run_code(self):
#         input_code = """xNum is 5
# out(xNum)
# sStr is "Hello"
# out(sStr)
# bBool is 1
# out(bBool)"""
#         python_code = translate_to_python(input_code)
#         capturedOutput = io.StringIO()
#         sys.stdout = capturedOutput
#         run_code(python_code)
#         sys.stdout = sys.__stdout__
#         output = capturedOutput.getvalue()
#         # self.assertEqual(output, "5\nHello\nTrue\n")
#         self.assertEqual(translate_to_python(input_code), python_code)

#     # this found an error so it stays
#     def test_add_two_numbers(self): 
#         input_code = """
#         xNum1 is 5
#         xNum2 is 3
#         out(xNum1 + xNum2)
#         """
#         expected_python_code = """
#         xNum1 = 5
#         xNum2 = 3
#         print(xNum1 + xNum2)
#         """
#         self.assertEqual(translate_to_python(input_code), expected_python_code)

#         python_code = translate_to_python(input_code)
#         capturedOutput = io.StringIO()
#         sys.stdout = capturedOutput
#         run_code(python_code)
#         sys.stdout = sys.__stdout__
#         output = capturedOutput.getvalue()
#         # self.assertEqual(output, "8\n")
#         self.assertEqual(translate_to_python(input_code), python_code)

#     # This throws error for addition until added
#     def test_add_two_numbers_2(self): 
#         input_code = """
#         xNuma is 5
#         xNumb is 3
#         xNumc is xNuma + xNumb
#         out(xNumc)
#         """
#         expected_python_code = """
#         xNuma = 5
#         xNumb = 3
#         xNumc = xNuma + xNumb
#         print(xNumc)
#         """
#         self.assertEqual(translate_to_python(input_code), expected_python_code)

#         # python_code = translate_to_python(input_code)
#         # capturedOutput = io.StringIO()
#         # sys.stdout = capturedOutput
#         # run_code(python_code)
#         # sys.stdout = sys.__stdout__
#         # output = capturedOutput.getvalue()
#         # self.assertEqual(output, "8\n")

#     def test_compare_two_numbers_pass(self):
#         input_code = """
#         xNuma is 5
#         xNumb is 3
#         if (xNuma > xNumb) then {
#             out("a is greater than b")
#         } else {
#             out("a is not greater than b")
#         }
#         """
#         expected_python_code = """
#         xNuma = 5
#         xNumb = 3
#         if (xNuma > xNumb)
#             print("a is greater than b")
#         else
#             print("a is not greater than b")
#         """
#         self.assertEqual(translate_to_python(input_code), expected_python_code)

#         # python_code = translate_to_python(input_code)
#         # capturedOutput = io.StringIO()
#         # sys.stdout = capturedOutput
#         run_code(expected_python_code)
#         # sys.stdout = sys.__stdout__
#         # output = capturedOutput.getvalue()
#         # self.assertEqual(output, "a is greater than b\n")

#     def test_compare_two_numbers_fail(self):
#         input_code = """
#         xNuma is 3
#         xNumb is 5
#         if (xNuma > xNumb) then
#             out("a is greater than b")
#         else
#             out("a is not greater than b")
#         """
#         expected_python_code = """
#         xNuma = 3
#         xNumb = 5
#         if (xNuma > xNumb)
#             print("a is greater than b")
#         else
#             print("a is not greater than b")
#         """
#         self.assertEqual(translate_to_python(input_code), expected_python_code)

#         # python_code = translate_to_python(input_code)
#         # capturedOutput = io.StringIO()
#         # sys.stdout = capturedOutput
#         # run_code(python_code)
#         # sys.stdout = sys.__stdout__
#         # output = capturedOutput.getvalue()
#         # self.assertEqual(output, "a is not greater than b\n")

if __name__ == '__main__':
    unittest.main()