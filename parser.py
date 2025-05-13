from scanner import Lexeme, Token, Scanner
from typing import List, Optional

# Symbol Table exception, for Part 2
class SymbolTableException(Exception):
    def __init__(self, lineno: int, ID: str) -> None:
        message = f"Symbol table error on line: {lineno}\nUndeclared ID: {ID}"
        super().__init__(message)

# Symbol Table skeleton (to be filled in for Part 2)
class SymbolTable:
    def __init__(self) -> None:
        pass

    def insert(self, ID: str, info) -> None:
        pass

    def lookup(self, ID: str):
        pass

    def push_scope(self) -> None:
        pass

    def pop_scope(self) -> None:
        pass

# Parser error exception for syntax errors
class ParserException(Exception):
    def __init__(self, lineno: int, lexeme: Lexeme, tokens: List[Token]) -> None:
        message = f"Parser error on line: {lineno}\nExpected one of: {tokens}\nGot: {lexeme}"
        super().__init__(message)

class Parser:
    def __init__(self, scanner: Scanner, use_symbol_table: bool) -> None:
        self.scanner = scanner
        self.use_symbol_table = use_symbol_table
        self.lookahead = self.scanner.token()

    def _match(self, expected_token: Token):
        if self.lookahead and self.lookahead.token == expected_token:
            self.lookahead = self.scanner.token()
        else:
            raise ParserException(
                self.scanner.get_lineno(),
                self.lookahead if self.lookahead else Lexeme(Token.ID, "EOF"),
                [expected_token]
            )

    def parse(self, s: str):
        self._program()

    def _program(self):
        self._stmt_list()

    def _stmt_list(self):
        while self.lookahead and self.lookahead.token in {
            Token.INT, Token.ID, Token.IF, Token.FOR, Token.LBRACE
        }:
            self._stmt()

    def _stmt(self):
        if self.lookahead.token == Token.INT:
            self._decl()
        elif self.lookahead.token == Token.ID:
            self._assign()
        elif self.lookahead.token == Token.IF:
            self._if_stmt()
        elif self.lookahead.token == Token.FOR:
            self._for_stmt()
        elif self.lookahead.token == Token.LBRACE:
            self._block()
        else:
            raise ParserException(
                self.scanner.get_lineno(),
                self.lookahead,
                [Token.INT, Token.ID, Token.IF, Token.FOR, Token.LBRACE]
            )

    def _decl(self):
        self._match(Token.INT)
        self._match(Token.ID)
        self._match(Token.SEMI)

    def _assign(self):
        self._match(Token.ID)
        self._match(Token.ASSIGN)
        self._expr()
        self._match(Token.SEMI)

    def _if_stmt(self):
        self._match(Token.IF)
        self._match(Token.LPAR)
        self._expr()
        self._match(Token.RPAR)
        self._stmt()
        if self.lookahead and self.lookahead.token == Token.ELSE:
            self._match(Token.ELSE)
            self._stmt()

    def _for_stmt(self):
        self._match(Token.FOR)
        self._match(Token.LPAR)
        self._assign()
        self._match(Token.SEMI)
        self._expr()
        self._match(Token.SEMI)
        self._assign()
        self._match(Token.RPAR)
        self._stmt()

    def _block(self):
        self._match(Token.LBRACE)
        self._stmt_list()
        self._match(Token.RBRACE)

    def _expr(self):
        self._simple_expr()
        if self.lookahead and self.lookahead.token in {Token.EQ, Token.LT}:
            self._match(self.lookahead.token)
            self._simple_expr()

    def _simple_expr(self):
        self._term()
        while self.lookahead and self.lookahead.token in {Token.PLUS, Token.MINUS}:
            self._match(self.lookahead.token)
            self._term()

    def _term(self):
        self._factor()
        while self.lookahead and self.lookahead.token == Token.MUL:
            self._match(Token.MUL)
            self._factor()

    def _factor(self):
        if self.lookahead.token == Token.LPAR:
            self._match(Token.LPAR)
            self._expr()
            self._match(Token.RPAR)
        elif self.lookahead.token in {Token.NUM, Token.ID}:
            self._match(self.lookahead.token)
        else:
            raise ParserException(
                self.scanner.get_lineno(),
                self.lookahead,
                [Token.NUM, Token.ID, Token.LPAR]
            )

