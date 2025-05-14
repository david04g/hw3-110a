from enum import Enum
from typing import Callable,List,Tuple,Optional
import re

class ScannerException(Exception):
    
    # this time, the scanner exception takes a line number
    def __init__(self, lineno:int) -> None:
        message = "Scanner error on line: " + str(lineno)
        super().__init__(message)

class Token(Enum):
    LPAR   = "("
    RPAR   = "("
    ID     = "ID"
    NUM    = "NUM"
    IGNORE = "IGNORE"
    MULT   = "*"
    PLUS   = "+"
    MINUS  = "-"
    DIV    = "/"
    ASSIGN = "="
    EQUAL = "=="
    LT    = "<"
    LBRACE = "{"
    RBRACE = "}"
    SEMI   = ";"
    FLOAT  = "FLOAT"
    INT    = "INT"
    FLOATTYPE = "FLOATTYPE"
    IF    = "IF"
    ELSE  = "ELSE"
    FOR   = "FOR"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"    


class Scanner:
    def __init__(self, tokens: List[Tuple[Token,str,Callable[[Lexeme],Lexeme]]]) -> None:
        self.tokens = tokens
        self.lineno = 1

    def input_string(self, input_string:str) -> None:
        self.istring = input_string

    # Get the scanner line number, needed for the parser exception
    def get_lineno(self)->int:
        return self.lineno

    # Implement me with one of your scanner implementations for part
    # 2. I suggest the SOS implementation. If you are not comfortable
    # using one of your own scanner implementations, you can use the
    # EMScanner implementation
        
    def token(self) -> Optional[Lexeme]:
        while len(self.istring) > 0:
            longest_t = None
            longest_reg = ''

            if self.istring[0].isspace():
                if self.istring[0] == '\n':
                    self.lineno += 1
                self.istring = self.istring[1:]
                continue

            for tok_type, pattern, action in self.tokens:
                match = re.match(pattern, self.istring)
                if match:
                    lexeme = match.group(0)
                    if len(lexeme) > len(longest_reg):
                        longest_reg = lexeme
                        longest_t = tok_type

            if not longest_reg:
                raise ScannerException(self.lineno)

            self.istring = self.istring[len(longest_reg):]

            if longest_t == Token.IGNORE:
                self.lineno += longest_reg.count('\n')
                continue

            if longest_t == Token.ID and longest_reg in keywords:
                return Lexeme(keywords[longest_reg], longest_reg)

            return idy(Lexeme(longest_t, longest_reg))

        return None

keywords = {
    'int': Token.INT,
    'float': Token.FLOATTYPE,
    'if': Token.IF,
    'else': Token.ELSE,
    'for': Token.FOR
}

def idy(l:Lexeme) -> Lexeme:
    return l

# Finish providing tokens (including token actions) for the C-simple
# language
tokens = [(Token.LPAR, r"\(", idy),
          (Token.RPAR, r"\)", idy),
          (Token.LT, r"<", idy),
          (Token.MULT, r"\*", idy),
          (Token.PLUS, r"\+", idy),
          (Token.MINUS, r"-", idy),
          (Token.DIV, r"/", idy),
          (Token.EQUAL, r"==", idy),
          (Token.ASSIGN, r"=", idy),
          (Token.SEMI, r";", idy),
          (Token.LBRACE, r"{", idy),
          (Token.RBRACE, r"}", idy),
          (Token.FLOAT, r'\d+\.\d+', idy),
          (Token.NUM, r'\d+', idy),
          (Token.ID, r"[a-zA-Z_][a-zA-Z0-9_]*", idy)]

