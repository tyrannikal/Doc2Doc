from main import *


run_cases = [
    (
        "00FFFF",
        (0, 255, 255),
    ),
    (
        "FFFF00",
        (255, 255, 0),
    ),
    (
        "Hello!",
        None,
        "not a hex color string",
    ),
    (
        "42",
        None,
        "not a hex color string",
    ),
    (
        1_000_000,
        None,
        "not a hex color string",
    ),
]

submit_cases = run_cases + [
    (
        "",
        None,
        "not a hex color string",
    ),
    (
        "FF00FF",
        (255, 0, 255),
    ),
    (
        "000000",
        (0, 0, 0),
    ),
    (
        "FFFFFF",
        (255, 255, 255),
    ),
]


def test(input, expected_output, expected_err=None):
    print("---------------------------------")
    print(f"  Inputs: '{input}'")
    try:
        result = hex_to_rgb(input)
    except Exception as e:
        print(f"Expected Error: {expected_err}")
        print(f"  Actual Error: {str(e)}")
        if str(e) != expected_err:
            print("Fail")
            return False
        print("Pass")
        return True

    if expected_err is not None:
        print(f"Expected Error: {expected_err}")
        print(f"        Actual: {result} (no error thrown)")
        print("Fail")
        return False

    print(f"Expected: {expected_output}")
    print(f"  Actual: {result}")
    if result != expected_output:
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
