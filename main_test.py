from main import *

run_cases = [
    (
        {"docx": True, "pdf": True},
        add_format,
        "txt",
        {"docx": True, "pdf": True, "txt": True},
    ),
    (
        {"md": True, "txt": False},
        add_format,
        "ppt",
        {"md": True, "txt": False, "ppt": True},
    ),
    ({"md": True, "txt": False}, remove_format, "md", {"md": False, "txt": False}),
]

submit_cases = run_cases + [
    ({}, add_format, "docx", {"docx": True}),
    (
        {"docx": True, "pdf": True, "txt": False},
        remove_format,
        "pdf",
        {"docx": True, "pdf": False, "txt": False},
    ),
    (
        {"docx": True, "pdf": True, "txt": False},
        add_format,
        "jpg",
        {"docx": True, "pdf": True, "txt": False, "jpg": True},
    ),
    (
        {"docx": False, "pdf": True, "txt": True},
        add_format,
        "docx",
        {"docx": True, "pdf": True, "txt": True},
    ),
]


def test(input1, formatter, input2, expected_output):
    print("---------------------------------")
    print(f"Inputs:")
    print(f" * default_formats: {input1}")
    print(f" * formatter: {formatter.__name__}")
    print(f" * new_format: {input2}")
    print(f"Expected: {expected_output}")
    input1_copy = input1.copy()
    result = formatter(input1, input2)
    print(f"Actual:   {result}")
    if result != expected_output:
        print("Fail")
        return False
    if input1 != input1_copy:
        print("Default_formats was mutated!")
        print("Fail")
        return False
    print("Pass")
    return True


def main():
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
