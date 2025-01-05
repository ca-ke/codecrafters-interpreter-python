import sys
from typing import List, Optional

from app.model.token import Token
from app.model.token_type import TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.had_error = False

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens

    def scan_token(self) -> None:
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL
                    if self.match(expected_char="=")
                    else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL
                    if self.match(expected_char="=")
                    else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL
                    if self.match(expected_char="=")
                    else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL
                    if self.match(expected_char="=")
                    else TokenType.GREATER
                )
            case _:
                # Delegate it
                self.had_error = True
                sys.stderr.write(
                    f"[line {self.line}] Error: Unexpected character: {c}\n"
                )

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        return char

    def match(self, expected_char: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected_char:
            return False
        self.current += 1
        return True

    def add_token(
        self,
        token_type: TokenType,
        literal: Optional[object] = None,
    ) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line))
