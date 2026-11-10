"""Recursive-descent recognizer for a precedence-aware arithmetic CFG."""
import re

TOKEN_RE = re.compile(r"\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(.))")

class ParseError(ValueError):
    pass

def tokenize(source: str):
    tokens=[]
    pos=0
    while pos < len(source):
        if source[pos:].isspace():
            break
        match=TOKEN_RE.match(source,pos)
        if not match:
            raise ParseError(f"Invalid token at position {pos}")
        number, ident, other = match.groups()
        if number: tokens.append(("NUMBER",number))
        elif ident: tokens.append(("ID",ident))
        elif other in "+-*/()": tokens.append((other,other))
        elif other and other.isspace(): pass
        else: raise ParseError(f"Unexpected character {other!r} at position {pos}")
        pos=match.end()
    tokens.append(("EOF",""))
    return tokens

class ArithmeticParser:
    def __init__(self, source):
        self.tokens=tokenize(source)
        self.i=0
    def current(self): return self.tokens[self.i]
    def eat(self, kind):
        if self.current()[0] != kind:
            raise ParseError(f"Expected {kind}, found {self.current()[0]}")
        value=self.current()[1]
        self.i+=1
        return value
    def parse(self):
        self.expression()
        if self.current()[0] != "EOF":
            raise ParseError(f"Unexpected token {self.current()[1]!r}")
        return True
    def expression(self):
        self.term()
        while self.current()[0] in ("+","-"):
            op=self.current()[0]; self.eat(op); self.term()
    def term(self):
        self.factor()
        while self.current()[0] in ("*","/"):
            op=self.current()[0]; self.eat(op); self.factor()
    def factor(self):
        kind,_=self.current()
        if kind in ("NUMBER","ID"):
            self.eat(kind)
        elif kind=="(":
            self.eat("("); self.expression(); self.eat(")")
        else:
            raise ParseError(f"Expected number, identifier or '(', found {kind}")

def is_valid_expression(source: str) -> bool:
    try:
        ArithmeticParser(source).parse()
        return True
    except (ParseError, IndexError):
        return False

def explain_parse(source: str) -> str:
    try:
        ArithmeticParser(source).parse()
        return "ACCEPT — token sequence conforms to the precedence-aware expression grammar."
    except (ParseError, IndexError) as exc:
        return f"REJECT — {exc}"
