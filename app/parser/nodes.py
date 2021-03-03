from ..lexer.tokens import TokenType
from ..lexer.units import UnitFlag

class NumberNode:
    def __init__(self, numberToken, unitToken=None):
        self.numberToken = numberToken
        self.unitToken = unitToken

    def __repr__(self):
        if self.unitToken is None: return f'{self.numberToken}'
        else: return f'{self.numberToken.value}{self.unitToken.value}'

    def simplify(self):
        '''Converts to metric and removes prefix'''
        if self.unitToken is not None:
            unit = self.unitToken.value
            if not unit.type.isDefault():
                # Convert number
                conv = unit.type.conv()
                self.numberToken.value = (self.numberToken.value + conv[1]) * conv[0]
                # Change unit
                self.unitToken.value.type = unit.type.getDefault()
            # Remove prefix
            if unit.prefix is not None:
                self.numberToken.value *= unit.prefix.mult()
                self.unitToken.value.prefix = None

class UnaryNode:
    def __init__(self, op, node):
        self.op = op
        self.node = node

    def __repr__(self):
        return f'<{self.op}, {self.node}>'

    def simplify(self):
        self.node.simplify()

class BinaryNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    
    def __repr__(self):
        return f'({self.left}, {self.op}, {self.right})'

    def simplify(self):
        if self.left: self.left.simplify()
        if self.right: self.right.simplify()