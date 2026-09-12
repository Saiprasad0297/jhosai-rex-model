"""
JHOSAI REX V2 - Calculator Tool

Provides safe mathematical expression evaluation
without using Python eval().
"""

import ast
import operator


class Calculator:
    """
    Safe calculator for JHOSAI REX.

    Supported:
    +   Addition
    -   Subtraction
    *   Multiplication
    /   Division
    %   Modulo
    **  Power
    ()  Parentheses
    """

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(self, expression: str):
        """Safely calculate a mathematical expression."""

        expression = expression.strip()

        if not expression:
            raise ValueError("Expression cannot be empty.")

        try:
            tree = ast.parse(expression, mode="eval")
            return self._evaluate(tree.body)

        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero.")

        except (SyntaxError, ValueError):
            raise ValueError("Invalid mathematical expression.")

    def _evaluate(self, node):
        """Recursively evaluate the AST."""

        # Numbers
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Invalid number.")

        # Unary operators: -10, +10
        if isinstance(node, ast.UnaryOp):
            operator_func = self.OPERATORS.get(type(node.op))

            if operator_func is None:
                raise ValueError("Unsupported operator.")

            operand = self._evaluate(node.operand)

            return operator_func(operand)

        # Binary operators: 10 + 5, 10 * 5, etc.
        if isinstance(node, ast.BinOp):
            operator_func = self.OPERATORS.get(type(node.op))

            if operator_func is None:
                raise ValueError("Unsupported operator.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operator_func(left, right)

        raise ValueError("Invalid mathematical expression.")


if __name__ == "__main__":
    calculator = Calculator()

    print("JHOSAI REX Calculator")
    print("----------------------")

    tests = [
        "25 * 4 + 10",
        "(100 - 20) / 4",
        "10 + 5 * 2",
        "2 ** 5",
        "100 % 30",
        "-25 + 10",
    ]

    for expression in tests:
        try:
            result = calculator.calculate(expression)
            print(f"{expression} = {result}")
        except ValueError as error:
            print(f"{expression} -> Error: {error}")