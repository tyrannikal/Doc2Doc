
from main import *

run_cases = [
    (
        "\n* We are the music makers\n- And we are the dreamers of dreams\n* Come with me and you'll be\n",
        "\n* We are the music makers\n* Come with me and you'll be\n",
    ),
    (
        "\n* In a world of pure imagination\n- There is no life I know\n* Living there - you'll be free\n",
        "\n* In a world of pure imagination\n* Living there - you'll be free\n",
    ),
]

submit_cases = run_cases + [
    (
        "\n* If you want to view paradise\n- Simply look around and view it\n* Anything you want to, do it\n* There is no life I know\n- To compare with pure imagination\n* Living there, you'll be free\n",
        "\n* If you want to view paradise\n* Anything you want to, do it\n* There is no life I know\n* Living there, you'll be free\n",
    ),
]


def test(input_document, expected_output):
    print("---------------------------------")
    print("Input document:")
    print('"' + input_document + '"')
    print("Expected output:")
    print('"' + expected_output + '"')
    result = remove_invalid_lines(input_document)
    print("Actual output:")
    print('"' + str(result) + '"')
    if result == expected_output:
        print("Pass")
        return True

    if expected_output.endswith("\n") and not str(result).endswith("\n"):
        print("Fail")
        print("Reason: expected newline at the end of the output")
        return False

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
