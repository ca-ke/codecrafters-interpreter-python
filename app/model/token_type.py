from enum import Enum, auto
from typing import List


class TokenType(Enum):
    # Single-character tokens (not reserved)
    LEFT_PAREN = (auto(), False)
    RIGHT_PAREN = (auto(), False)
    LEFT_BRACE = (auto(), False)
    RIGHT_BRACE = (auto(), False)
    COMMA = (auto(), False)
    DOT = (auto(), False)
    MINUS = (auto(), False)
    PLUS = (auto(), False)
    SEMICOLON = (auto(), False)
    SLASH = (auto(), False)
    STAR = (auto(), False)

    # One or two character tokens (not reserved)
    BANG = (auto(), False)
    BANG_EQUAL = (auto(), False)
    EQUAL = (auto(), False)
    EQUAL_EQUAL = (auto(), False)
    GREATER = (auto(), False)
    GREATER_EQUAL = (auto(), False)
    LESS = (auto(), False)
    LESS_EQUAL = (auto(), False)

    # Literals (not reserved)
    IDENTIFIER = (auto(), False)
    STRING = (auto(), False)
    NUMBER = (auto(), False)

    # Reserved Keywords (marked as reserved=True)
    AND = (auto(), True)
    CLASS = (auto(), True)
    ELSE = (auto(), True)
    FALSE = (auto(), True)
    FUN = (auto(), True)
    FOR = (auto(), True)
    IF = (auto(), True)
    NIL = (auto(), True)
    OR = (auto(), True)
    PRINT = (auto(), True)
    RETURN = (auto(), True)
    SUPER = (auto(), True)
    THIS = (auto(), True)
    TRUE = (auto(), True)
    VAR = (auto(), True)
    WHILE = (auto(), True)

    EOF = (auto(), False)

    def __init__(self, value, reserved):
        self._value_ = value
        self.reserved = reserved

    @staticmethod
    def reserved_keywords() -> List:
        return [token for token in TokenType if token.reserved]
