from ..parser.nodes import NumberNode, UnaryNode, BinaryNode
from ..lexer.tokens import TokenType
from ..lexer.units import UnitPrefix

class Number:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        if self.unit is not None: return f'{self.value} {self.unit.short_name()}'
        else: return f'{self.value}'

    def simplify(self):
        # Cannot simplify without units
        if self.unit is None: 
            return
        # Abort if already simplified
        if abs(self.value) > 0.001 and abs(self.value) < 1500.0:
            return
        # Try simplifying
        prefix = self.unit.prefix if self.unit.prefix else UnitPrefix.Zetta
        value = self.value
        while True:
            # Check value
            value = self.value / prefix.mult()
            if abs(value) > 0.1 and abs(value) < 1500.0: break
            # Grab smaller prefix
            next_prefix = prefix.smaller()
            if next_prefix is None: break
            prefix = next_prefix
        # Update value and prefix
        self.value = value
        self.unit.prefix = prefix

    def _unit(self, other):
        if self.unit is None: return other.unit
        if other.unit is None: return self.unit
        if self.unit.type is other.unit.type: return self.unit
        print(f'UNIT MISMATCH: {self.unit} != {other.unit}')
        return None

    def negated(self):
        return Number(-self.value, self.unit)

    def add(self, other):
        return Number(self.value + other.value, self._unit(other))

    def subtract(self, other):
        return Number(self.value - other.value, self._unit(other))

    def multiply(self, other):
        return Number(self.value * other.value, self._unit(other))

    def divide(self, other):
        return Number(self.value / other.value, self._unit(other))

class Interpreter:
    def __init__(self):
        pass

    def visit(self, node):
        if isinstance(node, NumberNode): return self.visit_number(node)
        elif isinstance(node, UnaryNode): return self.visit_unary(node)
        elif isinstance(node, BinaryNode): return self.visit_binary(node)
        else: print(f'Unknown Node: {type(node).__name__}')
        return None

    def visit_number(self, numberNode) -> Number:
        if numberNode.unitToken is None: return Number(numberNode.numberToken.value, None)
        else: return Number(numberNode.numberToken.value, numberNode.unitToken.value)

    def visit_unary(self, unaryNode):
        number = self.visit(unaryNode.node)
        op_type = unaryNode.op.type

        if op_type is TokenType.Minus: return number.negated()
        elif op_type is TokenType.Plus: return number
        else: return None

    def visit_binary(self, binaryNode):
        left = self.visit(binaryNode.left)
        right = self.visit(binaryNode.right)
        op_type = binaryNode.op.type

        if op_type is TokenType.Plus: return left.add(right)
        elif op_type is TokenType.Minus: return left.subtract(right)
        elif op_type is TokenType.Multiply: return left.multiply(right)
        elif op_type is TokenType.Divide: return left.divide(right)
        else: return None