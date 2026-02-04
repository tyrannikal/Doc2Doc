from main import *


run_cases = [
    (
        ("add_format", add_format),
        default_formats,
        [("rtf",), ("csv",)],
        ["txt", "md", "html", "rtf", "csv"],
    ),
    (
        ("save_document", save_document),
        saved_documents,
        [
            ("My_Princess_Diaries.txt", "I can't be a princess!"),
            (
                "The_Devil_Wears_Boots.md",
                "Please, bore someone else with your questions.",
            ),
        ],
        {
            "My_Princess_Diaries.txt": "I can't be a princess!",
            "The_Devil_Wears_Boots.md": "Please, bore someone else with your questions.",
        },
    ),
    (
        ("add_line_break", add_line_break),
        "It's not you, it's me.",
        [()],
        "It's not you, it's me.\n\n",
    ),
]


submit_cases = run_cases + [
    (
        ("add_format", add_format),
        default_formats,
        [
            ("doc",),
            ("docx",),
            ("pdf",),
        ],
        ["txt", "md", "html", "doc", "docx", "pdf"],
    ),
    (
        ("save_document", save_document),
        saved_documents,
        [
            ("Function_Club.txt", "The types you own end up owning you"),
            ("Shrek.doc", "Functions are like onions."),
        ],
        {
            "Function_Club.txt": "The types you own end up owning you",
            "Shrek.doc": "Functions are like onions.",
        },
    ),
    (
        ("add_line_break", add_line_break),
        "Go be free.",
        [()],
        "Go be free.\n\n",
    ),
]


def test(input1, input2, input3, expected_output):
    print("---------------------------------")
    print(f"Inputs:")
    print(f" * new command: {input1[0]}")
    print(f" * starting input: {input2}")
    result = input2
    commands = default_commands
    input2_length = len(input2)
    default_commands_length = len(default_commands)

    # add and test new command
    commands = add_custom_command(commands, *input1)
    for item in input3:
        if len(item) > 0:
            print(f" * input: {item}")
        result = commands[input1[0]](result, *item)

    # check result
    print(f"Expected: '{expected_output}'")
    print(f"Actual:   '{result}'")
    if result == expected_output:
        # check inputs not mutated
        if len(input2) == input2_length:
            if len(default_commands) == default_commands_length:
                print("Pass")
                return True
            else:
                print("default_commands modified")
        else:
            print("Starting input modified")
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
