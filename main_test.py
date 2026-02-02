from main import *


def to_string(file):
    return (
        f"File: {file['filename']}\n"
        f"Author: {file['author_first_name']} {file['author_last_name']}\n"
        f"Content: {file['content']}"
    )


run_cases = [
    (
        {
            "filename": "essay.txt",
            "content": "Dear Mr. Vernon, we accept the fact that we had to sacrifice a whole Saturday in detention for whatever it was we did wrong...",
            "author_first_name": "Brian",
            "author_last_name": "Johnson",
        },
        "```\nFile: essay.txt\nAuthor: Brian Johnson\nContent: Dear Mr. Vernon, we accept the fact that we had to sacrifice a whole Saturday in detention for whatever it was we did wrong...\n```",
    ),
    (
        {
            "filename": "letter.txt",
            "content": "But we think you're crazy to make us write an essay telling you who we think we are.",
            "author_first_name": "Brian",
            "author_last_name": "Johnson",
        },
        "```\nFile: letter.txt\nAuthor: Brian Johnson\nContent: But we think you're crazy to make us write an essay telling you who we think we are.\n```",
    ),
]

submit_cases = run_cases + [
    (
        {
            "filename": "note.txt",
            "content": "Does Barry Manilow know that you raid his wardrobe?",
            "author_first_name": "John",
            "author_last_name": "Bender",
        },
        "```\nFile: note.txt\nAuthor: John Bender\nContent: Does Barry Manilow know that you raid his wardrobe?\n```",
    ),
]


def test(input1, expected_output):
    print("---------------------------------")
    print("Inputs:")
    print(f"  filename: {input1['filename']}")
    print(f"  content: {input1['content'][:30]}...")  # Truncate for display
    print(f"  author_first_name: {input1['author_first_name']}")
    print(f"  author_last_name: {input1['author_last_name']}")
    print(f"Expected:\n{expected_output}")
    result = file_to_prompt(input1, to_string)
    print(f"Actual:\n{result}")
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


# file_type_getter tests
file_type_getter_run_cases = [
    # (file_extension_tuples, extension_to_lookup, expected_type)
    (
        [("Document", ["doc", "docx", "pdf"])],
        "pdf",
        "Document",
    ),
    (
        [("Document", ["doc", "docx", "pdf"]), ("Image", ["png", "jpg", "gif"])],
        "jpg",
        "Image",
    ),
]

file_type_getter_submit_cases = file_type_getter_run_cases + [
    # Unknown extension returns "Unknown"
    (
        [("Document", ["doc", "docx"])],
        "xyz",
        "Unknown",
    ),
    # Empty list returns "Unknown" for any lookup
    (
        [],
        "pdf",
        "Unknown",
    ),
    # Multiple types with overlapping-style extensions
    (
        [
            ("Text", ["txt", "text"]),
            ("Markup", ["html", "xml", "md"]),
            ("Code", ["py", "js", "ts"]),
        ],
        "py",
        "Code",
    ),
    # First extension in a list
    (
        [("Spreadsheet", ["xls", "xlsx", "csv"])],
        "xls",
        "Spreadsheet",
    ),
    # Last extension in a list
    (
        [("Spreadsheet", ["xls", "xlsx", "csv"])],
        "csv",
        "Spreadsheet",
    ),
    # Case sensitivity check - extensions are case-sensitive
    (
        [("Image", ["PNG", "JPG"])],
        "png",
        "Unknown",
    ),
]


def test_file_type_getter(file_extension_tuples, extension, expected_type):
    print("---------------------------------")
    print("Inputs:")
    print(f"  file_extension_tuples: {file_extension_tuples}")
    print(f"  extension to lookup: {extension}")
    print(f"Expected: {expected_type}")
    getter = file_type_getter(file_extension_tuples)
    result = getter(extension)
    print(f"Actual: {result}")
    if result == expected_type:
        print("Pass")
        return True
    print("Fail")
    return False


def main_file_type_getter():
    passed = 0
    failed = 0
    cases = file_type_getter_submit_cases
    if "__RUN__" in globals():
        cases = file_type_getter_run_cases
    skipped = len(file_type_getter_submit_cases) - len(cases)
    for test_case in cases:
        correct = test_file_type_getter(*test_case)
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


print("\n\n=== file_type_getter tests ===")
main_file_type_getter()
