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
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case '"':
                self.extract_string()
            case _:
                if c.isnumeric():
                    self.extract_number()
                    return
                elif self.is_alpha(c):
                    self.extract_identifier()
                    return
                # Delegate it
                self.had_error = True
                sys.stderr.write(
                    f"[line {self.line}] Error: Unexpected character: {c}\n"
                )

    def extract_number(self) -> None:
        while self.peek().isnumeric():
            self.advance()

        if self.peek() == "." and self.peek_next().isnumeric():
            self.advance()
            while self.peek().isnumeric():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def extract_identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        lexeme = self.source[self.start : self.current]
        token_type = next(
            token_type for token_type in TokenType.values() if token_type == lexeme
        )
        if token_type is None:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)

    def is_alpha_numeric(self, c: str) -> bool:
        return c.isnumeric() or self.is_alpha(c)

    def is_alpha(self, c: str) -> bool:
        return (c >= "a" and c <= "z") or (c >= "A" and c <= "Z") or c == "_"

    def extract_string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.had_error = True
            sys.stderr.write(f"[line {self.line}] Error: Unterminated string.\n")
            return

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

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
