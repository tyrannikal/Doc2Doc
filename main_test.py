from main import remove_emphasis

TestCase = tuple[str, str]

run_cases: list[TestCase] = [
    ("*Don't* panic.\n", "Don't panic.\n"),
    (
        "The **answer to the ultimate question** of life, the universe and everything is *42*\n",
        "The answer to the ultimate question of life, the universe and everything is 42\n",
    ),
    (
        "For a moment, *nothing* happened.\nThen, after a second or so, nothing **continued** to happen.\n",
        "For a moment, nothing happened.\nThen, after a second or so, nothing continued to happen.\n",
    ),
]

submit_cases: list[TestCase] = run_cases + [
    ("", ""),
    (
        "The Hitchhiker's Guide is a d*mn **useful** book.\n",
        "The Hitchhiker's Guide is a d*mn useful book.\n",
    ),
    (
        "In the beginning the *universe* was created.\nThis has made a lot of people very *angry* and been widely regarded as a bad move.\n",
        "In the beginning the universe was created.\nThis has made a lot of people very angry and been widely regarded as a bad move.\n",
    ),
    (
        "Ford, you're turning into a *penguin*\n",
        "Ford, you're turning into a penguin\n",
    ),
    (
        "*Space* is big.\nYou just won't **believe** how vastly, hugely, mind-bogglingly big it is.\n",
        "Space is big.\nYou just won't believe how vastly, hugely, mind-bogglingly big it is.\n",
    ),
    (
        "***Life before death, journey before destination.***\n",
        "Life before death, journey before destination.\n",
    ),
]


def test(input_doc: str, expected_output: str) -> bool:
    print("---------------------------------")
    print(f"Input document:\n{input_doc}")
    print(f"Expected output:\n{expected_output}")
    try:
        result = remove_emphasis(input_doc)
    except Exception as e:
        print(f"Exception raised: {e}")
        print("Fail")
        return False
    print(f"Actual output:\n{result}")
    if result == expected_output:
        print("Pass")
        return True
    print("Fail")
    return False


def main() -> None:
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


test_cases: list[TestCase] = submit_cases
if "__RUN__" in globals():
    test_cases = run_cases

main()
