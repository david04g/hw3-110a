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
        self.symbol_table = [{}]

    def insert(self, ID:str, info) -> None:
        self.symbol_table[-1][ID] = info

    def lookup(self, ID:str):
        for scope in reversed(self.symbol_table):
            if ID in scope:
                return scope[ID]
        return None

    def push_scope(self) -> None:
        self.symbol_table.append({})

    def pop_scope(self) -> None:
        if len(self.symbol_table) > 1:
            self.symbol_table.pop()

class ParserException(Exception):
    
    # Pass a line number, current lexeme, and what tokens are expected
    def __init__(self, lineno:int, lexeme:Lexeme, tokens:List[Token]) -> None:
        message = "Parser error on line: " + str(lineno) + "\nExpected one of: " + str(tokens) + "\nGot: " + str(lexeme)
        super().__init__(message)

class Parser:
    def __init__(self, scanner:Scanner, use_symbol_table:bool) -> None:
        self.scanner = scanner
        self.use_symbol_table = use_symbol_table
        if use_symbol_table:
            self.symbol_table = SymbolTable()

    # Implement one function in this class for every non-terminal in
    # your grammar using the recursive descent recipe from the book
    # and the lectures for part 2

    # Implement me:
    # s is the string to parse
    def parse(self, s:str):
        self.scanner.input_string(s)
        self.curr_lex = self.scanner.token()
        self.program()

    def program(self):
        self.statement_list()

    def statement_list(self):
        if self.curr_lex is not None:
            if self.curr_lex.token in [Token.ID, Token.IF, Token.FOR, Token.FLOAT, Token.INT, Token.LBRACE]:
                self.statement()
                self.statement_list()

#  assignment_statement   {ID}
#           |  if_else_statement      {IF}
#           |  block_statement        {LBRACE}
#           |  for_loop_statement     {FOR}
    def statement(self):
        if self.curr_lex.token == Token.ID:
            self.assignment_statement()
        elif self.curr_lex.token == Token.IF:
            self.if_else_statement()
        elif self.curr_lex.token == Token.FOR:
            self.for_loop_statement()
        elif self.curr_lex.token == Token.FLOAT or self.curr_lex.token == Token.INT:
            self.declaration_statement()
        elif self.curr_lex.token == Token.LBRACE:
            self.block_statement()
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.ID, Token.IF, Token.FOR, Token.FLOAT, Token.INT, Token.LBRACE])

    def eat(self, expected:Token):
        if self.curr_lex.token == expected:
            self.curr_lex = self.scanner.token()
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [expected])

    def assignment_statement(self):
        val = self.curr_lex.value
        if self.use_symbol_table:
            if self.symbol_table.lookup(val) is None:
                raise SymbolTableException(self.scanner.get_lineno(), val)
        self.eat(Token.ID)
        self.eat(Token.ASSIGN)
        self.expr()
        self.eat(Token.SEMI)

    def if_else_statement(self):
        self.eat(Token.IF)
        self.eat(Token.LPAR)
        self.expr()
        self.eat(Token.RPAR)
        self.statement()
        self.eat(Token.ELSE)
        self.statement()

    def for_loop_statement(self):
        self.eat(Token.FOR)
        self.eat(Token.LPAR)
        self.eat(Token.ID)
        self.eat(Token.ASSIGN)
        self.expr()
        self.eat(Token.SEMI)
        self.expr()
        self.eat(Token.SEMI)
        self.eat(Token.ID)
        self.eat(Token.ASSIGN)
        self.expr()
        self.eat(Token.RPAR)
        self.statement()

    def declaration_statement(self):
        t = None
        if self.curr_lex.token == Token.FLOAT:
            t = Token.FLOAT
            self.eat(Token.FLOAT)
        elif self.curr_lex.token == Token.INT:
            t = Token.INT
            self.eat(Token.INT)
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.FLOAT, Token.INT])

        val = self.curr_lex.value

        if self.use_symbol_table:
            if val in self.symbol_table.scope[-1]:
                raise SymbolTableException(self.scanner.get_lineno(), val)
            self.symbol_table.insert(val, t)

        self.eat(Token.ID)
        self.eat(Token.SEMI)

    def block_statement(self):
        self.eat(Token.LBRACE)
        if self.use_symbol_table:
            self.symbol_table.push_scope()
        self.statement_list()
        if self.use_symbol_table:
            self.symbol_table.pop_scope()
        self.eat(Token.RBRACE)
    
    def expr(self):
        self.comp()
        self.expr2()
    
    def expr2(self):
        if self.curr_lex.token is not None:
            if self.curr_lex.token == Token.EQUAL:
                self.eat(Token.EQUAL)
                self.comp()
                self.expr2()
            elif self.curr_lex.token in {Token.SEMI, Token.RPAR}:
                pass
            else:
                raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.ID, Token.NUM, Token.FLOAT, Token.LPAR])
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.ID, Token.NUM, Token.FLOAT, Token.LPAR])

    def comp(self):
        self.factor()
        self.comp2()

    def comp2(self):
        if self.curr_lex.token is not None:
            if self.curr_lex.token == Token.LT:
                self.eat(Token.LT)
                self.factor()
                self.comp2()
            elif self.curr_lex.token in {Token.SEMI, Token.RPAR, Token.EQUAL}:
                pass
            else:
                raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.LT, Token.SEMI, Token.RPAR, Token.EQUAL])
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.LT, Token.SEMI, Token.RPAR, Token.EQUAL])

    def factor(self):
        self.term()
        self.factor2()

    def factor2(self):
        if self.curr_lex.token is not None:
            if self.curr_lex.token == Token.PLUS:
                self.eat(Token.PLUS)
                self.term()
                self.factor2()
            elif self.curr_lex.token == Token.MINUS:
                self.eat(Token.MINUS)
                self.term()
                self.factor2()
            elif self.curr_lex.token in {Token.SEMI, Token.RPAR, Token.EQUAL, Token.LT}:
                pass
            else:
                raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.PLUS, Token.MINUS, Token.SEMI, Token.RPAR, Token.EQUAL, Token.LT])
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.PLUS, Token.MINUS, Token.SEMI, Token.RPAR, Token.EQUAL, Token.LT])

    def term(self):
        self.unit()
        self.term2()

    def term2(self):
        if self.curr_lex.token is not None:
            if self.curr_lex.token == Token.MULT:
                self.eat(Token.MULT)
                self.unit()
                self.term2()
            elif self.curr_lex.token == Token.DIV:
                self.eat(Token.DIV)
                self.unit()
                self.term2()
            elif self.curr_lex.token in {Token.SEMI, Token.RPAR, Token.EQUAL, Token.LT, Token.PLUS, Token.MINUS}:
                pass
            else:
                raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.MULT, Token.DIV, Token.SEMI, Token.RPAR, Token.EQUAL, Token.LT, Token.PLUS, Token.MINUS])
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.MULT, Token.DIV, Token.SEMI, Token.RPAR, Token.EQUAL, Token.LT, Token.PLUS, Token.MINUS])

    def unit(self):
        if self.curr_lex.token == Token.NUM:
            self.eat(Token.NUM)
        elif self.curr_lex.token == Token.FLOAT:
            self.eat(Token.FLOAT)
        elif self.curr_lex.token == Token.ID:
            self.eat(Token.ID)
        elif self.curr_lex.token == Token.LPAR:
            self.eat(Token.LPAR)
            self.expr()
            self.eat(Token.RPAR)
        else:
            raise ParserException(self.scanner.get_lineno(), self.curr_lex, [Token.NUM, Token.FLOAT, Token.ID, Token.LPAR])
        


