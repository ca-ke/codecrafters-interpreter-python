from typing import Any
from app.model.token import Token


class Expr:
    def accept(self, visitor) -> Any:
        raise NotImplementedError("You shall not pass! Subclass must implement it")


class Binary(Expr):
    def __init__(self, left: "Expr", operator: Token, right: "Expr") -> None:
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> Any:
        return visitor.visit_binary_expr(self)


class Grouping(Expr):
    def __init__(self, expression: "Expr") -> None:
        self.expression = expression

    def accept(self, visitor) -> Any:
        return visitor.visit_grouping_expr(self)


class Literal(Expr):
    def __init__(self, value: object) -> None:
        self.value = value

    def accept(self, visitor) -> Any:
        return visitor.visit_literal_expr(self)

    def __str__(self) -> str:
        return f"{self.value}"


class Unary(Expr):
    def __init__(self, operator: Token, right: "Expr") -> None:
        self.operator = operator
        self.right = right

    def accept(self, visitor) -> Any:
        return visitor.visit_unary_expr(self)
