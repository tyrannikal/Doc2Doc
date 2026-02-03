from main import *

run_cases = [
    (
        ["I don't feel safe", "Are you cussing with me"],
        2,
        "I don't feel safe. Are you cussing with me.",
    ),
    (
        ["You're fantastic", "He's just another rat", "Where'd the food come from"],
        2,
        "You're fantastic. He's just another rat.",
    ),
]

submit_cases = run_cases + [
    (["I'm not different"], 0, ""),
    (
        [
            "You wrote a bad song",
            "This is a good idea",
            "Just buy the tree",
            "It's going to flood",
            "Tell us what to do",
            "Here comes the train",
            "Are you cussing with me?",
            "This is just cider",
            "Get me a bandit hat",
        ],
        3,
        "You wrote a bad song. This is a good idea. Just buy the tree.",
    ),
]


def test(input_sentences, input_n, expected_output):
    print("---------------------------------")
    print("Inputs:")
    print(f" * sentences: {input_sentences}")
    print(f" * n: {input_n}")
    print("Expected:")
    print(f" * {expected_output}")
    result = join_first_sentences(input_sentences, input_n)
    print("Actual:")
    print(f" * {result}")
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

