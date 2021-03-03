from ..lexer.tokens import TokenType
from .nodes import NumberNode, BinaryNode, UnaryNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.token = None
        self._next()

    def _next(self):
        self.pos += 1
        if self.pos < len(self.tokens): self.token = self.tokens[self.pos]
        else: self.token = None

    def _rollback(self, amount):
        self.pos -= amount
        if self.pos < 0: self.pos = 0

    def factor(self):
        # Check for parenthesis
        if self.token.type is TokenType.LeftParen:
            self._next()
            expr = self.expr()
            if self.token is None: return None
            if self.token.type is TokenType.RightParen:
                self._next()
                return expr
        # Check for sign
        sign = None
        if self.token is None: return None
        if self.token.type in (TokenType.Minus, TokenType.Plus):
            sign = self.token
            self._next()
        # Check for number (having a number is acutally pretty important)
        number = None
        if self.token is None: return None
        if self.token.type in (TokenType.Int, TokenType.Float):
            number = self.token
            self._next()
        # Check for unit
        unit = None
        if self.token is not None and self.token.type is TokenType.Unit: 
            unit = self.token
            self._next()
        # Construct node
        node = NumberNode(number, unit)
        if sign is not None: 
            return UnaryNode(sign, node)  
        return node

    def term(self):
        return self.bin_op(self.factor, (TokenType.Multiply, TokenType.Divide))

    def expr(self):
        return self.bin_op(self.term, (TokenType.Plus, TokenType.Minus))

    def bin_op(self, wrap_func, types):
        left = wrap_func()
        while self.token is not None and self.token.type in types:
            op = self.token
            self._next()
            right = wrap_func()
            left = BinaryNode(left, op, right)
        return left