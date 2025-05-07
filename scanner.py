from enum import Enum
from typing import Callable,List,Tuple,Optional

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
        pass

def idy(l:Lexeme) -> Lexeme:
    return l

# Finish providing tokens (including token actions) for the C-simple
# language
tokens = [(Token.LPAR, "\(", idy),
          (Token.RPAR, "\)", idy)]
