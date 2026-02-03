import main as main_

run_cases = [
    ("Proposal.docx", "pdf", "Proposal.pdf"),
    ("Invoice.txt", "md", "Invoice.md"),
]

submit_cases = run_cases + [
    ("Presentation.ppt", "pptx", "Presentation.pptx"),
    ("Intro.pptx", "jpeg", None),
    ("Summary.md", "txt", "Summary.txt"),
    ("Contract.pdf", "pdoof", None),
]


def mutate_globals():
    main_.valid_extensions = ["docx", "txt", "pptx", "ppt", "md"]
    main_.valid_conversions = {
        "docx": ["jpeg"],
        "pdf": ["docx", "txt", "md"],
        "txt": ["docx"],
        "ppt": ["pptx", "jpeg"],
        "md": ["png"],
        "jpeg": ["png"],
    }


def test(input1, input2, expected_output):
    print("---------------------------------")
    print(f"Inputs:")
    print(f" * filename: {input1}")
    print(f" * target_format: {input2}")
    print(f"Expected: {expected_output}")
    result = main_.convert_file_format(input1, input2)
    print(f"Actual:   {result}")
    if result == expected_output:
        print("Pass")
        return True
    print("Fail")
    return False


def main():
    passed = 0
    failed = 0
    mutate_globals()
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
