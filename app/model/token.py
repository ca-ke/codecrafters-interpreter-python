from typing import Optional
from app.model.token_type import TokenType


class Token:
    def __init__(
        self,
        token_type: TokenType,
        lexeme: str,
        literal: Optional[object],
        line: int,
    ) -> None:
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.token_type.name} {self.lexeme} {"null" if self.literal is None else self.literal}"
