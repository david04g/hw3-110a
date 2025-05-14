from enum import Enum
from typing import Callable, List, Tuple, Optional
import re

class ScannerException(Exception):
    def __init__(self, lineno: int) -> None:
        message = f"Scanner error on line: {lineno}"
        super().__init__(message)

class Token(Enum):
    LPAR   = "("
    RPAR   = ")"
    LBRACE = "{"
    RBRACE = "}"
    ID     = "ID"
    NUM    = "NUM"
    FLOAT  = "FLOAT"
    ASSIGN = "="
    EQUAL  = "=="
    LT     = "<"
    PLUS   = "+"
    MINUS  = "-"
    MUL    = "*"
    DIV    = "/"
    SEMI   = ";"
    IGNORE = "IGNORE"
    IF     = "if"
    ELSE   = "else"
    FOR    = "for"
    INT    = "int"
    FLOATTYPE = "float"

class Lexeme:
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return f"({self.token}, \"{self.value}\")"

keywords = {
    'int': Token.INT,
    'float': Token.FLOATTYPE,
    'if': Token.IF,
    'else': Token.ELSE,
    'for': Token.FOR
}

def idy(l: Lexeme) -> Lexeme:
    return l

tokens = [
    (Token.LPAR, r"\(", idy),
    (Token.RPAR, r"\)", idy),
    (Token.LBRACE, r"\{", idy),
    (Token.RBRACE, r"\}", idy),
    (Token.EQUAL, r"==", idy),
    (Token.ASSIGN, r"=", idy),
    (Token.LT, r"<", idy),
    (Token.PLUS, r"\+", idy),
    (Token.MINUS, r"-", idy),
    (Token.MUL, r"\*", idy),
    (Token.DIV, r"/", idy),
    (Token.SEMI, r";", idy),
    (Token.FLOAT, r"\d+\.\d+", idy),
    (Token.NUM, r"\d+", idy),
    (Token.ID, r"[a-zA-Z_][a-zA-Z0-9_]*", idy),
    (Token.IGNORE, r"[ \t\n]+", idy),
    (Token.IGNORE, r"//.*", idy),
]

class Scanner:
    def __init__(self, tokens: List[Tuple[Token, str, Callable[[Lexeme], Lexeme]]]) -> None:
        self.tokens = tokens
        self.lineno = 1
        self.istring = ""

    def input_string(self, input_string: str) -> None:
        self.istring = input_string

    def get_lineno(self) -> int:
        return self.lineno

    def token(self) -> Optional[Lexeme]:
        while self.istring:
            if self.istring[0].isspace():
                if self.istring[0] == '\n':
                    self.lineno += 1
                self.istring = self.istring[1:]
                continue

            longest_match = ""
            longest_token = None
            for token_type, regex, action in self.tokens:
                match = re.match(regex, self.istring)
                if match:
                    text = match.group(0)
                    if len(text) > len(longest_match):
                        longest_match = text
                        longest_token = token_type

            if not longest_match:
                raise ScannerException(self.lineno)

            self.istring = self.istring[len(longest_match):]

            if longest_token == Token.IGNORE:
                self.lineno += longest_match.count('\n')
                continue

            if longest_token == Token.ID and longest_match in keywords:
                return Lexeme(keywords[longest_match], longest_match)

            return idy(Lexeme(longest_token, longest_match))

        return None

