from main import *

run_cases = [
    (
        "Through the darkness of future past",
        "uppercase",
        "THROUGH THE DARKNESS OF FUTURE PAST",
    ),
    ("The magician longs to see", "lowercase", "the magician longs to see"),
]

submit_cases = run_cases + [
    (
        "One chants out between two worlds",
        "titlecase",
        "One Chants Out Between Two Worlds",
    ),
    ("Fire walk with me", "garbagecase", "unsupported format: garbagecase"),
]


def test(input1, input2, expected_output):
    print("---------------------------------")
    print(f"Input:")
    print(f'"{input1}", {input2}')
    print(f"Expected:")
    print(f'"{expected_output}"')
    try:
        result = convert_case(input1, input2)
    except Exception as e:
        result = str(e)
    print(f"Actual:")
    print(f'"{result}"')
    if result == expected_output:
        print("Pass")
        return True
    print("Fail")
    return False


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
