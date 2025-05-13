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
    ASSIGN = "="
    EQ     = "=="
    GT     = ">"     # Added greater-than
    LT     = "<"
    PLUS   = "+"
    MINUS  = "-"
    MUL    = "*"
    SEMI   = ";"
    IGNORE = "IGNORE"
    IF     = "if"
    ELSE   = "else"
    FOR    = "for"
    INT    = "int"

class Lexeme:
    def __init__(self, token: Token, value: str) -> None:
        self.token = token
        self.value = value

    def __str__(self) -> str:
        return f"({self.token}, \"{self.value}\")"

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
        while self.istring and self.istring[0] in [' ', '\t', '\n']:
            if self.istring[0] == '\n':
                self.lineno += 1
            self.istring = self.istring[1:]

        if not self.istring:
            return None

        for token_type, regex, action in self.tokens:
            match = re.match(regex, self.istring)
            if match:
                matched_text = match.group(0)
                self.istring = self.istring[len(matched_text):]

                if token_type == Token.IGNORE:
                    self.lineno += matched_text.count('\n')
                    return self.token()

                lexeme = Lexeme(token_type, matched_text)
                return action(lexeme)

        raise ScannerException(self.lineno)

# Default identity token action
def idy(l: Lexeme) -> Lexeme:
    return l

tokens = [
    (Token.IGNORE, r"[ \t\n]+", idy),
    (Token.IGNORE, r"//.*", idy),
    (Token.EQ, r"==", idy),
    (Token.GT, r">", idy),           # Added token
    (Token.LT, r"<", idy),
    (Token.LPAR, r"\(", idy),
    (Token.RPAR, r"\)", idy),
    (Token.LBRACE, r"\{", idy),
    (Token.RBRACE, r"\}", idy),
    (Token.SEMI, r";", idy),
    (Token.ASSIGN, r"=", idy),
    (Token.PLUS, r"\+", idy),
    (Token.MINUS, r"-", idy),
    (Token.MUL, r"\*", idy),
    (Token.NUM, r"\d+(\.\d+)?", idy),
    (Token.IF, r"\bif\b", idy),
    (Token.ELSE, r"\belse\b", idy),
    (Token.FOR, r"\bfor\b", idy),
    (Token.INT, r"\bint\b", idy),
    (Token.ID, r"[a-zA-Z_][a-zA-Z0-9_]*", idy),
]

