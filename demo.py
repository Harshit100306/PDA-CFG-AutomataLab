from src.balanced_parentheses import is_balanced_parentheses, trace_parentheses
from src.arithmetic_parser import is_valid_expression, explain_parse
from src.palindrome_pda import is_palindrome_pda, midpoint_traces

def show(title, rows, fn):
    print("\n"+title)
    for value in rows:
        print(f"{value!r:18} -> {'ACCEPT' if fn(value) else 'REJECT'}")

if __name__=="__main__":
    show("BALANCED PARENTHESES", ["(())","(()","()()","())"], is_balanced_parentheses)
    print("\nStack trace for (()):")
    for item in trace_parentheses("(())"): print(" ",item)
    show("ARITHMETIC EXPRESSIONS", ["a+b*c","(a+b)*c","a+*b","(a+b"], is_valid_expression)
    print("\nParse explanation:", explain_parse("a+b*c"))
    show("PALINDROMES OVER {a,b}", ["abba","aba","aab","abab"], is_palindrome_pda)
    print("\nPDA branch trace for abba:")
    for item in midpoint_traces("abba"): print(" ",item)
