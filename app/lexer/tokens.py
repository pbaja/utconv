from enum import IntEnum, auto

class TokenType(IntEnum):
    Invalid = auto()
    # Types
    Int = auto()
    Float = auto()
    Unit = auto()
    # Operators
    Plus = auto()
    Minus = auto()
    Multiply = auto()
    Divide = auto()
    LeftParen = auto()
    RightParen = auto()

    def __str__(self):
        return self.name

class Token:
    def __init__(self, tokenType:TokenType, tokenValue=None):
        self.type = tokenType
        self.value = tokenValue
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        else: return f'{self.type}'
