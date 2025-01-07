from typing import Protocol, Any

from app.model.node import Binary, Grouping, Literal, Unary


class ExprVisitor(Protocol):
    def visit_binary_expr(self, expr: Binary) -> Any:
        pass

    def visit_grouping_expr(self, expr: Grouping) -> Any:
        pass

    def visit_literal_expr(self, expr: Literal) -> Any:
        pass

    def visit_unary_expr(self, expr: Unary) -> Any:
        pass


class AstPrinter(ExprVisitor):
    def visit_binary_expr(self, expr: Binary) -> str:
        return f"({expr.operator} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return f"(group {expr.expression.accept(self)})"

    def visit_literal_expr(self, expr: Literal) -> str:
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return f"({expr.operator} {expr.right.accept(self)})"
