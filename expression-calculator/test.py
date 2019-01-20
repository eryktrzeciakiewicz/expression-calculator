import unittest
from rpn_calculator import RPNCalculator
from validator import Validator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = RPNCalculator()

    def test_simple_operations(self):
        sum = self.calculator.calculate("1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10")
        diff = self.calculator.calculate("20 - 1 - 1 - 3 - 10")
        prod = self.calculator.calculate("1 * 1 * 1 * 1 * 5 * 1 * 2")
        quot = self.calculator.calculate("100 / 10 / 2")
        pow = self.calculator.calculate("2 ^ 10")
        
        self.assertEqual(sum, 55)
        self.assertEqual(diff, 5)
        self.assertEqual(prod, 10)
        self.assertEqual(quot, 5)
        self.assertEqual(pow, 1024)
    
    def test_can_handle_fractions(self):
        res = self.calculator.calculate("1 / 2")
        self.assertAlmostEqual(res, 0.5)

    def test_operations_have_correct_priority(self):
        res = self.calculator.calculate("1 + 2 * 2 + 2 ^ 2 * 2")
        self.assertEqual(res, 13)

    def test_can_calculate_unpadded_expressions(self):
        exp = "(6/2)*(2+1)"
        res = self.calculator.calculate(exp)
        self.assertEqual(res, 9)

    def test_can_handle_strange_braces(self):
        exp1 = "(2)+(2)"
        exp2 = "(((((((((( 1 + 1 ))))))))))"
        res1 = self.calculator.calculate(exp1)
        res2 = self.calculator.calculate(exp2)
        self.assertEqual(res1, 4)
        self.assertEqual(res2, 2)

    def test_can_parse_functions(self):
        exp1 = "sin(0)"
        res1 = self.calculator.to_rpn(exp1)
        self.assertEqual(res1, ["0","sin"])

    def can_calculate_functions(self):
        exp1 = "sin(0)"
        exp2 = "3 * cos(0)"
        res1 = self.calculator.calculate(exp1)
        res2 = self.calculator.calculate(exp2)
        self.assertAlmostEqual(exp1, 0)
        self.assertAlmostEqual(exp2, 3)

    def test_functions_can_have_expression_arguments(self):
        expressioin = "sin(3 * 0)"
        res = self.calculator.calculate(expressioin)
        expression2 = "sin( sin( 0 ) )"
        res2 = self.calculator.calculate(expression2)
        
        self.assertEqual(res, 0)
        self.assertEqual(res2, 0)

    def test_can_handle_constants(self):
        expression = "pi + e"
        res = self.calculator.calculate(expression)
        self.assertGreater(res, 5)
        self.assertLess(res, 6)

        expression2 = "sin(pi)"
        res2 = self.calculator.calculate(expression2)
        self.assertAlmostEqual(res2, 0)

    def test_illegal_token_error(self):
        exp = "2p+7"
        self.calculator.calculate(exp)
        self.assertRaises(ValueError)

    def test_can_handle_default_variables(self):
        exp = "2*x"
        res = self.calculator.calculate(exp)
        self.assertEqual(0, res)

    def test_variable_is_numeric(self):
        self.assertTrue(Validator.is_numeric("x"))
    
    def test_variable_is_legal(self):
        self.assertTrue(Validator.is_legal("x"))    

    def test_variables_put_into_rpn(self):
        exp = "2*x+1"
        self.assertEqual(self.calculator.to_rpn(exp), ["2", "x", "*", "1", "+"])

    def test_variables_are_handled(self):
        exp = "2*x + 7"
        res = self.calculator.calculate(exp, 1)
        self.assertEqual(res, 9)

    def test_variables_no_multiplication_operator_handles(self):
        exp1 = "2x"
        exp2 = "xx"
        exp3 = "2xx"
        exp4 = "2x2x"
        res1 = self.calculator.calculate(exp1, 1)
        res2 = self.calculator.calculate(exp2, 2)
        res3 = self.calculator.calculate(exp3, 2)
        res4 = self.calculator.calculate(exp4, 2)
        self.assertEqual(res1, 2)
        self.assertEqual(res2, 4)
        self.assertEqual(res3, 8)
        self.assertEqual(res4, 16)

