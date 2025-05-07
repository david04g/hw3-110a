from scanner import Lexeme,Token,Scanner
from typing import Callable,List,Tuple,Optional

# Symbol Table exception, requires a line number and ID
class SymbolTableException(Exception):
    
    def __init__(self, lineno:int, ID:str) -> None:
        message = "Symbol table error on line: " + str(lineno) + "\nUndeclared ID: " + ID
        super().__init__(message)    

#Implement all members of this class for Part 3
class SymbolTable:
    def __init__(self) -> None:
        pass

    def insert(self, ID:str, info) -> None:
        pass

    def lookup(self, ID:str):
        pass

    def push_scope(self) -> None:
        pass

    def pop_scope(self) -> None:
        pass

class ParserException(Exception):
    
    # Pass a line number, current lexeme, and what tokens are expected
    def __init__(self, lineno:int, lexeme:Lexeme, tokens:List[Token]) -> None:
        message = "Parser error on line: " + str(lineno) + "\nExpected one of: " + str(tokens) + "\nGot: " + str(lexeme)
        super().__init__(message)

class Parser:
    def __init__(self, scanner:Scanner, use_symbol_table:bool) -> None:
        self.scanner = scanner

    # Implement one function in this class for every non-terminal in
    # your grammar using the recursive descent recipe from the book
    # and the lectures for part 2

    # Implement me:
    # s is the string to parse
    def parse(self, s:str):
        pass
