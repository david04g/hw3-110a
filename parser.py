from scanner import Lexeme, Token, Scanner
from typing import List, Optional

class SymbolTableException(Exception):
    def __init__(self, lineno: int, ID: str) -> None:
        message = f"Symbol table error on line: {lineno}\nUndeclared ID: {ID}"
        super().__init__(message)

class SymbolTable:
    def __init__(self) -> None:
        self.scopes = [{}]

    def insert(self, ID: str, info=None) -> None:
        if ID in self.scopes[-1]:
            raise SymbolTableException(-1, ID)
        self.scopes[-1][ID] = info

    def lookup(self, ID: str):
        for scope in reversed(self.scopes):
            if ID in scope:
                return scope[ID]
        raise SymbolTableException(-1, ID)

    def push_scope(self) -> None:
        self.scopes.append({})

    def pop_scope(self) -> None:
        self.scopes.pop()

class ParserException(Exception):
    def __init__(self, lineno: int, lexeme: Lexeme, tokens: List[Token]) -> None:
        message = f"Parser error on line: {lineno}\nExpected one of: {tokens}\nGot: {lexeme}"
        super().__init__(message)

class Parser:
    def __init__(self, scanner: Scanner, use_symbol_table: bool) -> None:
        self.scanner = scanner
        self.use_symbol_table = use_symbol_table
        self.lookahead = self.scanner.token()
        if use_symbol_table:
            self.symbol_table = SymbolTable()

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
            Token.INT, Token.ID, Token.IF, Token.FOR, Token.LBRACE, Token.SEMI
        }:
            self._stmt()

    def _stmt(self):
        if self.lookahead.token == Token.INT:
            self._decl()
        elif self.lookahead.token == Token.ID:
            temp = self.lookahead
            self._match(Token.ID)
            if self.lookahead and self.lookahead.token == Token.ASSIGN:
                if self.use_symbol_table:
                    self.symbol_table.lookup(temp.value)
                self._match(Token.ASSIGN)
                self._expr()
                self._match(Token.SEMI)
            else:
                raise ParserException(
                    self.scanner.get_lineno(),
                    self.lookahead,
                    [Token.ASSIGN]
                )
        elif self.lookahead.token == Token.IF:
            self._if_stmt()
        elif self.lookahead.token == Token.FOR:
            self._for_stmt()
        elif self.lookahead.token == Token.LBRACE:
            self._block()
        elif self.lookahead.token == Token.SEMI:
            self._match(Token.SEMI)
        else:
            raise ParserException(
                self.scanner.get_lineno(),
                self.lookahead,
                [Token.INT, Token.ID, Token.IF, Token.FOR, Token.LBRACE, Token.SEMI]
            )

    def _decl(self):
        self._match(Token.INT)
        var_name = self.lookahead.value
        self._match(Token.ID)
        if self.use_symbol_table:
            self.symbol_table.insert(var_name)
        self._match(Token.SEMI)

    def _assign_expr(self):
        var_name = self.lookahead.value
        if self.use_symbol_table:
            self.symbol_table.lookup(var_name)
        self._match(Token.ID)
        self._match(Token.ASSIGN)
        self._expr()

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
        self._assign_expr()
        self._match(Token.SEMI)
        self._expr()
        self._match(Token.SEMI)
        self._assign_expr()
        self._match(Token.RPAR)
        self._stmt()

    def _block(self):
        self._match(Token.LBRACE)
        if self.use_symbol_table:
            self.symbol_table.push_scope()
        self._stmt_list()
        if self.use_symbol_table:
            self.symbol_table.pop_scope()
        self._match(Token.RBRACE)

    def _expr(self):
        self._simple_expr()
        if self.lookahead and self.lookahead.token in {Token.EQ, Token.LT, Token.GT}:
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
        elif self.lookahead.token == Token.ID:
            if self.use_symbol_table:
                self.symbol_table.lookup(self.lookahead.value)
            self._match(Token.ID)
        elif self.lookahead.token == Token.NUM:
            self._match(Token.NUM)
        else:
            raise ParserException(
                self.scanner.get_lineno(),
                self.lookahead,
                [Token.NUM, Token.ID, Token.LPAR]
            )

