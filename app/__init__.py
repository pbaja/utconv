from .lexer import Lexer
def run_lexer(text):
    lexer = Lexer(text)
    return lexer.solve()
    
from .parser import Parser
def run_parser(tokens):
    return Parser(tokens).expr()

from .interpreter import Interpreter
def run_interpreter(root):
    return Interpreter().visit(root)