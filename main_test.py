import ast
import inspect
import textwrap
from typing import Callable

from main import choose_parser

run_cases: list[tuple[str, str]] = [
    ("md", "markdown"),
    ("txt", "plaintext"),
]

submit_cases: list[tuple[str, str]] = run_cases + [
    ("markdown", "markdown"),
    ("MD", "markdown"),
    ("docx", "plaintext"),
]


def get_ast(fn: Callable) -> ast.Module:
    src: str = textwrap.dedent(inspect.getsource(fn))
    return ast.parse(src)


def uses_ternary(fn: Callable) -> bool:
    tree = get_ast(fn)
    fn_def = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))

    has_ifexp = any(isinstance(n, ast.IfExp) for n in ast.walk(fn_def))
    has_if_stmt = any(isinstance(n, ast.If) for n in ast.walk(fn_def))

    return has_ifexp and not has_if_stmt


def test(input: str, expected: str) -> bool:
    print("---------------------------------")
    print(f"File extension: {input}")
    print(f"Expected parser: {expected}")
    result = choose_parser(input)
    print(f"Chosen parser: {result}")
    if result == expected:
        print("Pass")
        return True
    print("Fail")
    return False


def main() -> None:
    if not uses_ternary(choose_parser):
        print("Please use a ternary expression!")
        print("============= FAIL ==============")
        return

    print("Ternary expression detected!")

    passed = 0
    failed = 0
    skipped = len(submit_cases) - len(test_cases)

    for test_case in test_cases:
        correct = test(*test_case)
        if correct:
            passed += 1
        else:
            failed += 1

    if failed == 0:
        print("============= PASS ==============")
    else:
        print("============= FAIL ==============")

    if skipped > 0:
        print(f"{passed} passed, {failed} failed, {skipped} skipped")
    else:
        print(f"{passed} passed, {failed} failed")


test_cases = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()
