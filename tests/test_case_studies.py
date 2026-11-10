import unittest
from src.balanced_parentheses import is_balanced_parentheses
from src.arithmetic_parser import is_valid_expression
from src.palindrome_pda import is_palindrome_pda

class TestBalancedParentheses(unittest.TestCase):
    def test_accept(self):
        for s in ["", "()", "(())", "()()", "(()())", "((()()))"]:
            self.assertTrue(is_balanced_parentheses(s),s)
    def test_reject(self):
        for s in [")(", "(", ")", "(()", "())", "(a)", "(()))"]:
            self.assertFalse(is_balanced_parentheses(s),s)

class TestArithmeticGrammar(unittest.TestCase):
    def test_accept(self):
        for s in ["x", "42", "x+y", "a+b*c", "(a+b)*c", "x / (y-2)", "alpha_1 + 12.5"]:
            self.assertTrue(is_valid_expression(s),s)
    def test_reject(self):
        for s in ["", "+a", "a+", "a**b", "(a+b", "a+b)", "a b", "a @ b"]:
            self.assertFalse(is_valid_expression(s),s)

class TestPalindromePDA(unittest.TestCase):
    def test_accept(self):
        for s in ["", "a", "b", "aa", "aba", "abba", "baab", "aabbaa"]:
            self.assertTrue(is_palindrome_pda(s),s)
    def test_reject(self):
        for s in ["ab", "aab", "abb", "abab", "ba", "abc"]:
            self.assertFalse(is_palindrome_pda(s),s)

if __name__=="__main__": unittest.main()
