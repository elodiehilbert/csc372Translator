import io
import sys
import unittest
from translator import translate_to_python, run_code

class TestTranslator(unittest.TestCase):
    def test_translate_to_python(self):
        input_code = """
        xNum is 5
        out(Num)
        sStr is "Hello"
        out(Str)
        bBool is 1
        out(Bool)
        """
        expected_python_code = """
        Num = 5
        print(Num)
        Str = "Hello"
        print(Str)
        Bool = bool(True)
        print(Bool)
        """
        self.assertEqual(translate_to_python(input_code), expected_python_code)

    def test_run_code(self):
        input_code = """
        xNum is 5
        out(Num)
        sStr is "Hello"
        out(Str)
        bBool is 1
        out(Bool)
        """
        python_code = translate_to_python(input_code)
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        run_code(python_code)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertEqual(output, "5\nHello\nTrue\n")

    # this found an error so it stays
    def test_add_two_numbers(self): 
        input_code = """
        xNum1 is 5
        xNum2 is 3
        out(Num1 + Num2)
        """
        expected_python_code = """
        Num1 = 5
        Num2 = 3
        print(Num1 + Num2)
        """
        self.assertEqual(translate_to_python(input_code), expected_python_code)

        python_code = translate_to_python(input_code)
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        run_code(python_code)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertEqual(output, "8\n")

    # This throws error for addition until added
    def test_add_two_numbers(self): 
        input_code = """
        xNuma is 5
        xNumb is 3
        out(Numa+Numb)
        """
        expected_python_code = """
        Numa = 5
        Numb = 3
        print(Numa+Numb)
        """
        self.assertEqual(translate_to_python(input_code), expected_python_code)

        python_code = translate_to_python(input_code)
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        run_code(python_code)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertEqual(output, "8\n")

    def test_compare_two_numbers_pass(self):
        input_code = """
        xN is 5
        xNu is 3
        if (N>Nu) then
            out("N is greater than Nu")
        else
            out("N is not greater than Nu")
        """
        expected_python_code = """
        N = 5
        Nu = 3
        if (N>Nu)
            print("N is greater than Nu")
        else
            print("N is not greater than Nu")
        """
        self.assertEqual(translate_to_python(input_code), expected_python_code)

        python_code = translate_to_python(input_code)
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        run_code(python_code)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertEqual(output, "N is greater than Nu\n")

    def test_compare_two_numbers_fail(self):
        input_code = """
        xN is 3
        xNu is 5
        if (N > Nu) then
            out("N is greater than Nu")
        else
            out("N is not greater than Nu")
        """
        expected_python_code = """
        N = 3
        Nu = 5
        if (N > Nu)
            print("N is greater than Nu")
        else
            print("N is not greater than Nu")
        """
        self.assertEqual(translate_to_python(input_code), expected_python_code)

        python_code = translate_to_python(input_code)
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        run_code(python_code)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        self.assertEqual(output, "N is not greater than Nu\n")

if __name__ == '__main__':
    unittest.main()