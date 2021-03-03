import string
from typing import List
from .tokens import Token, TokenType
from .units import Unit

class Lexer:
    def __init__(self, text:str):
        self.text = text
        self.pos = -1
        self.char = ''
        self._next()
        self.tokens = []

    def _next(self):
        self.pos += 1
        if self.pos < len(self.text): self.char = self.text[self.pos]
        else: self.char = None

    def _rollback(self, amount:int):
        self.pos -= amount
        if self.pos < 0: self.pos = 0

    def _solve_number(self) -> Token:
        # Grab all number characters
        number = ''
        while self.char is not None and self.char in string.digits+'.':
            number += self.char
            self._next()
        # Try parsing the number
        try:
            if '.' in number: return Token(TokenType.Float, float(number))
            else: return Token(TokenType.Int, int(number))
        except ValueError:
            return Token(TokenType.Invalid, number)

    def _solve_string(self) -> Token:
        # Grab all characters until unit unit is encountered
        unitText = ''
        foundUnits = []
        fails = 0
        while self.char is not None and self.char in string.ascii_letters:
            # Try parsing unit from string
            unitText += self.char
            units = Unit.fromText(unitText)

            # We found unit, add to list
            if len(units) > 0: 
                foundUnits += units
                fails = 0
            # Allow up to 3 consecutive fails before giving up
            elif fails > 3: break
            # Failed to find unit
            else: fails += 1

            # Advance
            self._next()

        # Finished string
        if len(foundUnits) == 0:
            self._rollback(fails)
            return Token(TokenType.Invalid, unitText)
        else:
            bestUnits = sorted(foundUnits, key=lambda x: len(x.text))
            #print(bestUnits)
            return Token(TokenType.Unit, bestUnits[-1])

    def solve(self) -> List[Token]:
        self.tokens.clear()
        advance = True
        while self.char is not None:
            # Ignore whitespace
            if len(self.char.strip()) == 0:
                pass
            # Operators
            elif self.char == '+': 
                self.tokens.append(Token(TokenType.Plus))
            elif self.char == '-':
                self.tokens.append(Token(TokenType.Minus))
            elif self.char == '*':
                self.tokens.append(Token(TokenType.Multiply))
            elif self.char == '/':
                self.tokens.append(Token(TokenType.Divide))
            elif self.char == '(':
                self.tokens.append(Token(TokenType.LeftParen))
            elif self.char == ')':
                self.tokens.append(Token(TokenType.RightParen))
            # Numbers
            elif self.char in string.digits:
                self.tokens.append(self._solve_number())
                advance = False
            # Units
            elif self.char in string.ascii_letters:
                self.tokens.append(self._solve_string())
                advance = False
            else:
                self.tokens.append(Token(TokenType.Invalid, self.char))

            # Advance to next character
            if advance: self._next()
            advance = True
            
        return self.tokens