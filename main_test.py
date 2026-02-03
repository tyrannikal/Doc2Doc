from main import *

run_cases = [
    (
        (
            ("Mortgage", "Marriage Certificate", "Boot.dev Certificate"),
            ("VEHICLE TITLE", "MORTGAGE"),
        ),
        {"MORTGAGE", "MARRIAGE CERTIFICATE", "BOOT.DEV CERTIFICATE", "VEHICLE TITLE"},
    ),
    (
        (
            ("ANNUITY", "WATER BILL"),
            ("Photo Album", "1235023451345", "Year Book"),
        ),
        {"ANNUITY", "WATER BILL", "PHOTO ALBUM", "YEAR BOOK"},
    ),
]

submit_cases = run_cases + [
    (((), ()), set()),
    (
        (
            ("RECEIPT FOR 1st AND LAST RENT", "School Loan"),
            ("SCOOTER REGISTRATION", "314159", "ENGLISH MAJOR DEGREE"),
        ),
        {
            "RECEIPT FOR 1ST AND LAST RENT",
            "SCHOOL LOAN",
            "SCOOTER REGISTRATION",
            "ENGLISH MAJOR DEGREE",
        },
    ),
]


def test(input1, expected_output):
    print("---------------------------------")
    print(f"Inputs:")
    print(f" * damaged documents: {input1[0]}")
    print(f" * back-up documents: {input1[1]}")
    print(f"Expected: {expected_output}")
    try:
        result = restore_documents(*input1)
    except Exception as e:
        result = f"Error: {e}"
    print(f"Actual:   {result}")
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
