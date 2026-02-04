"""Tests for main module."""

import pytest

from main import (
    add_border,
    add_format,
    add_prefix,
    center_title,
    change_bullet_style,
    choose_parser,
    convert_case,
    convert_file_format,
    convert_line,
    file_to_prompt,
    file_type_getter,
    format_line,
    get_median_font_size,
    hex_to_rgb,
    is_hexadecimal,
    join,
    join_first_sentences,
    pair_document_with_format,
    remove_emphasis,
    remove_format,
    remove_invalid_lines,
    remove_line_emphasis,
    remove_word_emphasis,
    restore_documents,
    stylize_title,
    word_count,
    word_count_memo,
)


class TestCenterTitle:
    """Tests for center_title function."""

    def test_centers_short_title(self) -> None:
        """Test centering a short title within 40 char width."""
        doc = "Hello\nBody text"
        result = center_title(doc)
        assert "Hello" not in result or result.split("\n", maxsplit=1)[
            0
        ] == "Hello".center(40)

    def test_centers_title_preserves_body(self) -> None:
        """Test that body text is preserved."""
        doc = "Title\nBody line 1\nBody line 2"
        result = center_title(doc)
        assert "Body line 1" in result
        assert "Body line 2" in result


class TestAddBorder:
    """Tests for add_border function."""

    def test_adds_asterisk_border(self) -> None:
        """Test that asterisks are added below title."""
        doc = "Hello\nBody"
        result = add_border(doc)
        lines = result.split("\n")
        assert lines[1] == "*" * len("Hello")

    def test_border_matches_title_length(self) -> None:
        """Test border length matches title length."""
        doc = "A longer title here\nBody"
        result = add_border(doc)
        lines = result.split("\n")
        assert len(lines[1]) == len("A longer title here")


class TestStylizeTitle:
    """Tests for stylize_title function."""

    def test_stylizes_document(self) -> None:
        """Test that document gets centered and bordered title."""
        doc = "Title\nBody"
        result = stylize_title(doc)
        assert "*" in result


class TestAddPrefix:
    """Tests for add_prefix function."""

    def test_adds_numbered_prefix(self) -> None:
        """Test that document gets numbered prefix based on tuple length."""
        docs: tuple[str, ...] = ("first",)
        result = add_prefix("second", docs)
        assert result[-1] == "1. second"

    def test_empty_tuple_prefix(self) -> None:
        """Test prefix with empty tuple."""
        docs: tuple[str, ...] = ()
        result = add_prefix("first", docs)
        assert result == ("0. first",)

    def test_returns_extended_tuple(self) -> None:
        """Test that original documents are preserved."""
        docs: tuple[str, ...] = ("a", "b")
        result = add_prefix("c", docs)
        assert len(result) == 3
        assert result[0] == "a"
        assert result[1] == "b"


class TestGetMedianFontSize:
    """Tests for get_median_font_size function."""

    def test_empty_list_returns_none(self) -> None:
        """Test empty list returns None."""
        assert get_median_font_size([]) is None

    def test_single_element(self) -> None:
        """Test single element list."""
        assert get_median_font_size([12]) == 12

    def test_odd_number_of_elements(self) -> None:
        """Test median of odd-length list."""
        assert get_median_font_size([10, 12, 14]) == 12

    def test_even_number_of_elements(self) -> None:
        """Test median of even-length list (returns lower median)."""
        assert get_median_font_size([10, 12, 14, 16]) == 12

    def test_unsorted_list(self) -> None:
        """Test that unsorted list is handled correctly."""
        assert get_median_font_size([14, 10, 12]) == 12


class TestFormatLine:
    """Tests for format_line function."""

    def test_removes_periods_from_input(self) -> None:
        """Test that periods from input are removed."""
        result = format_line("hello.world")
        assert result == "HELLOWORLD..."

    def test_uppercases(self) -> None:
        """Test that output is uppercase."""
        result = format_line("hello")
        assert result == "HELLO..."

    def test_strips_whitespace(self) -> None:
        """Test that whitespace is stripped."""
        result = format_line("  hello  ")
        assert result == "HELLO..."

    def test_adds_ellipsis(self) -> None:
        """Test that ellipsis is added."""
        result = format_line("test")
        assert result.endswith("...")


class TestChooseParser:
    """Tests for choose_parser function."""

    def test_markdown_extension(self) -> None:
        """Test markdown extension returns markdown parser."""
        assert choose_parser("md") == "markdown"
        assert choose_parser("markdown") == "markdown"

    def test_case_insensitive(self) -> None:
        """Test case insensitivity."""
        assert choose_parser("MD") == "markdown"
        assert choose_parser("Markdown") == "markdown"

    def test_other_extensions(self) -> None:
        """Test non-markdown returns plaintext."""
        assert choose_parser("txt") == "plaintext"
        assert choose_parser("py") == "plaintext"
        assert choose_parser("html") == "plaintext"


class TestIsHexadecimal:
    """Tests for is_hexadecimal function."""

    def test_valid_hex(self) -> None:
        """Test valid hexadecimal strings."""
        assert is_hexadecimal("ff00ff") is True
        assert is_hexadecimal("123abc") is True
        assert is_hexadecimal("AABBCC") is True

    def test_invalid_hex(self) -> None:
        """Test invalid hexadecimal strings."""
        assert is_hexadecimal("gggggg") is False
        assert is_hexadecimal("hello") is False

    def test_empty_string(self) -> None:
        """Test empty string."""
        assert is_hexadecimal("") is False


class TestHexToRgb:
    """Tests for hex_to_rgb function."""

    def test_valid_hex_color(self) -> None:
        """Test valid hex color conversion."""
        assert hex_to_rgb("ff0000") == (255, 0, 0)
        assert hex_to_rgb("00ff00") == (0, 255, 0)
        assert hex_to_rgb("0000ff") == (0, 0, 255)

    def test_mixed_case(self) -> None:
        """Test mixed case hex."""
        assert hex_to_rgb("FF00FF") == (255, 0, 255)

    def test_invalid_length_raises(self) -> None:
        """Test that wrong length raises TypeError."""
        with pytest.raises(TypeError, match="not a hex color string"):
            hex_to_rgb("fff")

    def test_invalid_hex_raises(self) -> None:
        """Test that invalid hex raises TypeError."""
        with pytest.raises(TypeError, match="not a hex color string"):
            hex_to_rgb("gggggg")


class TestFileToPrompt:
    """Tests for file_to_prompt function."""

    def test_wraps_in_code_block(self) -> None:
        """Test that output is wrapped in code block."""
        file_data = {"name": "test.txt", "content": "hello"}

        def to_str(f: dict[str, str]) -> str:
            return f["content"]

        result = file_to_prompt(file_data, to_str)
        assert result.startswith("```\n")
        assert result.endswith("\n```")

    def test_uses_to_string_function(self) -> None:
        """Test that to_string function is applied."""
        file_data = {"key": "value"}

        def custom_to_str(f: dict[str, str]) -> str:
            return f"Key is {f['key']}"

        result = file_to_prompt(file_data, custom_to_str)
        assert "Key is value" in result


class TestFileTypeGetter:
    """Tests for file_type_getter function."""

    def test_returns_callable(self) -> None:
        """Test that function returns a callable."""
        getter = file_type_getter([("Document", ["doc", "pdf"])])
        assert callable(getter)

    def test_finds_extension_type(self) -> None:
        """Test basic extension lookup."""
        getter = file_type_getter([("Document", ["doc", "docx", "pdf"])])
        assert getter("pdf") == "Document"
        assert getter("doc") == "Document"

    def test_multiple_file_types(self) -> None:
        """Test lookup across multiple file types."""
        getter = file_type_getter(
            [
                ("Document", ["doc", "docx", "pdf"]),
                ("Image", ["png", "jpg", "gif"]),
                ("Code", ["py", "js", "ts"]),
            ]
        )
        assert getter("pdf") == "Document"
        assert getter("jpg") == "Image"
        assert getter("py") == "Code"

    def test_unknown_extension_returns_unknown(self) -> None:
        """Test that unknown extension returns 'Unknown'."""
        getter = file_type_getter([("Document", ["doc", "pdf"])])
        assert getter("xyz") == "Unknown"
        assert getter("") == "Unknown"

    def test_empty_list_returns_unknown(self) -> None:
        """Test empty extension list returns 'Unknown' for any lookup."""
        getter = file_type_getter([])
        assert getter("pdf") == "Unknown"
        assert getter("any") == "Unknown"

    def test_case_sensitive(self) -> None:
        """Test that extension matching is case-sensitive."""
        getter = file_type_getter([("Image", ["PNG", "JPG"])])
        assert getter("PNG") == "Image"
        assert getter("png") == "Unknown"

    def test_first_and_last_extensions(self) -> None:
        """Test first and last extensions in list are found."""
        getter = file_type_getter([("Spreadsheet", ["xls", "xlsx", "csv"])])
        assert getter("xls") == "Spreadsheet"
        assert getter("csv") == "Spreadsheet"


class TestConvertLine:
    """Tests for convert_line function."""

    def test_converts_dash_to_asterisk(self) -> None:
        """Test that dash bullet is converted to asterisk."""
        assert convert_line("- item") == "* item"

    def test_preserves_non_bullet_lines(self) -> None:
        """Test that non-bullet lines are unchanged."""
        assert convert_line("regular line") == "regular line"
        assert convert_line("* already asterisk") == "* already asterisk"

    def test_empty_line(self) -> None:
        """Test that empty line is unchanged."""
        assert convert_line("") == ""

    def test_dash_not_at_start(self) -> None:
        """Test that dash not at start is unchanged."""
        assert convert_line("text - with dash") == "text - with dash"


class TestChangeBulletStyle:
    """Tests for change_bullet_style function."""

    def test_converts_all_dash_bullets(self) -> None:
        """Test that all dash bullets are converted."""
        doc = "- item 1\n- item 2\n- item 3"
        expected = "* item 1\n* item 2\n* item 3"
        assert change_bullet_style(doc) == expected

    def test_preserves_non_bullet_lines(self) -> None:
        """Test mixed content with non-bullet lines."""
        doc = "Title\n- item 1\nParagraph\n- item 2"
        expected = "Title\n* item 1\nParagraph\n* item 2"
        assert change_bullet_style(doc) == expected

    def test_empty_document(self) -> None:
        """Test empty document."""
        assert change_bullet_style("") == ""

    def test_no_bullets(self) -> None:
        """Test document with no bullets."""
        doc = "Line 1\nLine 2"
        assert change_bullet_style(doc) == doc


class TestRemoveInvalidLines:
    """Tests for remove_invalid_lines function."""

    def test_removes_lines_starting_with_dash(self) -> None:
        """Test that lines starting with dash are removed."""
        doc = "valid line\n- invalid line\nanother valid"
        expected = "valid line\nanother valid"
        assert remove_invalid_lines(doc) == expected

    def test_preserves_valid_lines(self) -> None:
        """Test that non-dash lines are preserved."""
        doc = "* bullet\nregular text\n  indented"
        assert remove_invalid_lines(doc) == doc

    def test_empty_document(self) -> None:
        """Test empty document."""
        assert remove_invalid_lines("") == ""

    def test_all_invalid_lines(self) -> None:
        """Test document with all invalid lines."""
        doc = "- line 1\n- line 2\n- line 3"
        assert remove_invalid_lines(doc) == ""

    def test_dash_in_middle_of_line(self) -> None:
        """Test that dash in middle of line doesn't remove it."""
        doc = "text - with dash\nanother - line"
        assert remove_invalid_lines(doc) == doc

    def test_mixed_valid_and_invalid(self) -> None:
        """Test mixed document with multiple invalid lines."""
        doc = "\n* We are the music makers\n- And we are the dreamers\n* Come with me\n"
        expected = "\n* We are the music makers\n* Come with me\n"
        assert remove_invalid_lines(doc) == expected


class TestJoin:
    """Tests for join function."""

    def test_joins_two_strings(self) -> None:
        """Test that two strings are joined with period and space."""
        assert join("Hello", "World") == "Hello. World"

    def test_joins_with_existing_content(self) -> None:
        """Test joining to existing multi-sentence content."""
        assert join("First. Second", "Third") == "First. Second. Third"

    def test_empty_first_string(self) -> None:
        """Test joining with empty first string."""
        assert join("", "Second") == ". Second"

    def test_empty_second_string(self) -> None:
        """Test joining with empty second string."""
        assert join("First", "") == "First. "


class TestJoinFirstSentences:
    """Tests for join_first_sentences function."""

    def test_joins_first_n_sentences(self) -> None:
        """Test joining first n sentences from list."""
        sentences = ["First", "Second", "Third", "Fourth"]
        assert join_first_sentences(sentences, 2) == "First. Second."

    def test_n_equals_zero_returns_empty(self) -> None:
        """Test that n=0 returns empty string."""
        sentences = ["First", "Second"]
        assert join_first_sentences(sentences, 0) == ""

    def test_single_sentence(self) -> None:
        """Test with n=1."""
        sentences = ["Only one", "Not included"]
        assert join_first_sentences(sentences, 1) == "Only one."

    def test_all_sentences(self) -> None:
        """Test joining all sentences."""
        sentences = ["A", "B", "C"]
        assert join_first_sentences(sentences, 3) == "A. B. C."

    def test_n_greater_than_list_length(self) -> None:
        """Test when n exceeds list length."""
        sentences = ["One", "Two"]
        assert join_first_sentences(sentences, 5) == "One. Two."


class TestPairDocumentWithFormat:
    """Tests for pair_document_with_format function."""

    def test_pairs_valid_formats(self) -> None:
        """Test pairing documents with valid formats."""
        names = ["doc1", "doc2", "doc3"]
        formats = ["pdf", "docx", "txt"]
        result = pair_document_with_format(names, formats)
        assert result == [("doc1", "pdf"), ("doc2", "docx"), ("doc3", "txt")]

    def test_filters_invalid_formats(self) -> None:
        """Test that invalid formats are filtered out."""
        names = ["doc1", "doc2", "doc3"]
        formats = ["pdf", "xyz", "txt"]
        result = pair_document_with_format(names, formats)
        assert result == [("doc1", "pdf"), ("doc3", "txt")]

    def test_all_invalid_formats(self) -> None:
        """Test with all invalid formats returns empty list."""
        names = ["doc1", "doc2"]
        formats = ["invalid", "unknown"]
        result = pair_document_with_format(names, formats)
        assert not result

    def test_empty_lists(self) -> None:
        """Test with empty input lists."""
        result = pair_document_with_format([], [])
        assert not result

    def test_all_valid_format_types(self) -> None:
        """Test all valid format types are accepted."""
        names = ["a", "b", "c", "d", "e", "f"]
        formats = ["docx", "pdf", "txt", "pptx", "ppt", "md"]
        result = pair_document_with_format(names, formats)
        assert len(result) == 6


class TestRestoreDocuments:
    """Tests for restore_documents function."""

    def test_combines_and_uppercases(self) -> None:
        """Test that originals and backups are combined and uppercased."""
        originals = ("doc1", "doc2")
        backups = ("doc3",)
        result = restore_documents(originals, backups)
        assert result == {"DOC1", "DOC2", "DOC3"}

    def test_filters_digit_only_strings(self) -> None:
        """Test that digit-only strings are filtered out."""
        originals = ("doc1", "123", "456")
        backups = ("doc2", "789")
        result = restore_documents(originals, backups)
        assert result == {"DOC1", "DOC2"}

    def test_empty_tuples(self) -> None:
        """Test with empty input tuples."""
        result = restore_documents((), ())
        assert not result

    def test_returns_set_no_duplicates(self) -> None:
        """Test that duplicates are removed (set behavior)."""
        originals = ("doc", "DOC")
        backups = ("Doc",)
        result = restore_documents(originals, backups)
        assert result == {"DOC"}

    def test_mixed_alphanumeric_preserved(self) -> None:
        """Test that strings with mixed alphanumeric are preserved."""
        originals = ("file1", "2file", "f1l3")
        backups = ("123",)
        result = restore_documents(originals, backups)
        assert result == {"FILE1", "2FILE", "F1L3"}


class TestConvertFileFormat:
    """Tests for convert_file_format function."""

    def test_docx_to_pdf(self) -> None:
        """Test converting docx to pdf."""
        assert convert_file_format("document.docx", "pdf") == "document.pdf"

    def test_docx_to_txt(self) -> None:
        """Test converting docx to txt."""
        assert convert_file_format("file.docx", "txt") == "file.txt"

    def test_docx_to_md(self) -> None:
        """Test converting docx to md."""
        assert convert_file_format("file.docx", "md") == "file.md"

    def test_pdf_conversions(self) -> None:
        """Test valid pdf conversions."""
        assert convert_file_format("file.pdf", "docx") == "file.docx"
        assert convert_file_format("file.pdf", "txt") == "file.txt"
        assert convert_file_format("file.pdf", "md") == "file.md"

    def test_txt_conversions(self) -> None:
        """Test valid txt conversions."""
        assert convert_file_format("file.txt", "docx") == "file.docx"
        assert convert_file_format("file.txt", "pdf") == "file.pdf"
        assert convert_file_format("file.txt", "md") == "file.md"

    def test_pptx_conversions(self) -> None:
        """Test valid pptx conversions."""
        assert convert_file_format("slides.pptx", "ppt") == "slides.ppt"
        assert convert_file_format("slides.pptx", "pdf") == "slides.pdf"

    def test_ppt_conversions(self) -> None:
        """Test valid ppt conversions."""
        assert convert_file_format("slides.ppt", "pptx") == "slides.pptx"
        assert convert_file_format("slides.ppt", "pdf") == "slides.pdf"

    def test_md_conversions(self) -> None:
        """Test valid md conversions."""
        assert convert_file_format("readme.md", "docx") == "readme.docx"
        assert convert_file_format("readme.md", "pdf") == "readme.pdf"
        assert convert_file_format("readme.md", "txt") == "readme.txt"

    def test_invalid_source_format(self) -> None:
        """Test with invalid source format returns None."""
        assert convert_file_format("file.xyz", "pdf") is None
        assert convert_file_format("file.jpg", "docx") is None

    def test_invalid_target_format(self) -> None:
        """Test with invalid target format returns None."""
        assert convert_file_format("file.docx", "pptx") is None
        assert convert_file_format("file.pptx", "docx") is None

    def test_same_format_returns_none(self) -> None:
        """Test converting to same format returns None."""
        assert convert_file_format("file.pdf", "pdf") is None


class TestAddFormat:
    """Tests for add_format function."""

    def test_adds_new_format(self) -> None:
        """Test adding a new format to existing dict."""
        formats = {"docx": True, "pdf": True}
        result = add_format(formats, "txt")
        assert result == {"docx": True, "pdf": True, "txt": True}

    def test_overwrites_existing_false_value(self) -> None:
        """Test adding a format that exists with False sets it to True."""
        formats = {"docx": False, "pdf": True}
        result = add_format(formats, "docx")
        assert result == {"docx": True, "pdf": True}

    def test_adds_to_empty_dict(self) -> None:
        """Test adding format to empty dict."""
        result = add_format({}, "docx")
        assert result == {"docx": True}

    def test_does_not_mutate_original(self) -> None:
        """Test that original dict is not modified."""
        formats = {"docx": True, "pdf": False}
        original_copy = formats.copy()
        add_format(formats, "txt")
        assert formats == original_copy

    def test_existing_true_value_unchanged(self) -> None:
        """Test adding a format that already exists with True."""
        formats = {"docx": True, "pdf": True}
        result = add_format(formats, "docx")
        assert result == {"docx": True, "pdf": True}


class TestRemoveFormat:
    """Tests for remove_format function."""

    def test_removes_existing_format(self) -> None:
        """Test removing an existing format sets it to False."""
        formats = {"docx": True, "pdf": True}
        result = remove_format(formats, "pdf")
        assert result == {"docx": True, "pdf": False}

    def test_removes_already_false_format(self) -> None:
        """Test removing a format that is already False."""
        formats = {"docx": True, "pdf": False}
        result = remove_format(formats, "pdf")
        assert result == {"docx": True, "pdf": False}

    def test_removes_nonexistent_format(self) -> None:
        """Test removing a format that doesn't exist creates it as False."""
        formats = {"docx": True}
        result = remove_format(formats, "pdf")
        assert result == {"docx": True, "pdf": False}

    def test_does_not_mutate_original(self) -> None:
        """Test that original dict is not modified."""
        formats = {"docx": True, "pdf": True}
        original_copy = formats.copy()
        remove_format(formats, "pdf")
        assert formats == original_copy

    def test_removes_from_empty_dict(self) -> None:
        """Test removing from empty dict creates entry with False."""
        result = remove_format({}, "docx")
        assert result == {"docx": False}


class TestConvertCase:
    """Tests for convert_case function."""

    def test_converts_to_uppercase(self) -> None:
        """Test converting text to uppercase."""
        assert convert_case("hello world", "uppercase") == "HELLO WORLD"

    def test_converts_to_lowercase(self) -> None:
        """Test converting text to lowercase."""
        assert convert_case("HELLO WORLD", "lowercase") == "hello world"

    def test_converts_to_titlecase(self) -> None:
        """Test converting text to titlecase."""
        assert convert_case("hello world", "titlecase") == "Hello World"

    def test_empty_text_raises_error(self) -> None:
        """Test that empty text raises ValueError."""
        with pytest.raises(ValueError, match="no text or target format provided"):
            convert_case("", "uppercase")

    def test_empty_format_raises_error(self) -> None:
        """Test that empty format raises ValueError."""
        with pytest.raises(ValueError, match="no text or target format provided"):
            convert_case("hello", "")

    def test_unsupported_format_raises_error(self) -> None:
        """Test that unsupported format raises ValueError."""
        with pytest.raises(ValueError, match="unsupported format"):
            convert_case("hello", "snakecase")

    def test_mixed_case_input(self) -> None:
        """Test converting mixed case input."""
        assert convert_case("HeLLo WoRLd", "lowercase") == "hello world"
        assert convert_case("HeLLo WoRLd", "uppercase") == "HELLO WORLD"
        assert convert_case("hELLO wORLD", "titlecase") == "Hello World"


class TestRemoveWordEmphasis:
    """Tests for remove_word_emphasis function."""

    def test_removes_leading_asterisks(self) -> None:
        """Test removing leading asterisks."""
        assert remove_word_emphasis("*hello") == "hello"
        assert remove_word_emphasis("**hello") == "hello"

    def test_removes_trailing_asterisks(self) -> None:
        """Test removing trailing asterisks."""
        assert remove_word_emphasis("hello*") == "hello"
        assert remove_word_emphasis("hello**") == "hello"

    def test_removes_surrounding_asterisks(self) -> None:
        """Test removing asterisks from both ends."""
        assert remove_word_emphasis("*hello*") == "hello"
        assert remove_word_emphasis("**hello**") == "hello"

    def test_preserves_word_without_asterisks(self) -> None:
        """Test word without asterisks is unchanged."""
        assert remove_word_emphasis("hello") == "hello"

    def test_empty_string(self) -> None:
        """Test empty string returns empty string."""
        assert remove_word_emphasis("") == ""

    def test_only_asterisks(self) -> None:
        """Test string of only asterisks returns empty string."""
        assert remove_word_emphasis("***") == ""


class TestRemoveLineEmphasis:
    """Tests for remove_line_emphasis function."""

    def test_removes_emphasis_from_words(self) -> None:
        """Test removing emphasis from multiple words."""
        assert remove_line_emphasis("*hello* *world*") == "hello world"

    def test_mixed_emphasis_and_plain(self) -> None:
        """Test line with mix of emphasized and plain words."""
        assert remove_line_emphasis("*bold* plain **strong**") == "bold plain strong"

    def test_empty_line(self) -> None:
        """Test empty line returns empty string."""
        assert remove_line_emphasis("") == ""

    def test_no_emphasis(self) -> None:
        """Test line without emphasis is unchanged."""
        assert remove_line_emphasis("hello world") == "hello world"


class TestRemoveEmphasis:
    """Tests for remove_emphasis function."""

    def test_removes_emphasis_from_document(self) -> None:
        """Test removing emphasis from multi-line document."""
        doc = "*hello* world\n**bold** text"
        expected = "hello world\nbold text"
        assert remove_emphasis(doc) == expected

    def test_empty_document(self) -> None:
        """Test empty document returns empty string."""
        assert remove_emphasis("") == ""

    def test_single_line(self) -> None:
        """Test single line document."""
        assert remove_emphasis("*emphasized*") == "emphasized"

    def test_no_emphasis(self) -> None:
        """Test document without emphasis is unchanged."""
        doc = "plain text\nanother line"
        assert remove_emphasis(doc) == doc

    def test_multiple_lines_with_mixed_content(self) -> None:
        """Test multiple lines with various emphasis patterns."""
        doc = "Title\n*italic* and **bold**\nplain line"
        expected = "Title\nitalic and bold\nplain line"
        assert remove_emphasis(doc) == expected


class TestWordCount:
    """Tests for word_count function."""

    def test_counts_words(self) -> None:
        """Test counting words in a simple sentence."""
        assert word_count("hello world") == 2

    def test_empty_string(self) -> None:
        """Test empty string returns zero."""
        assert word_count("") == 0

    def test_single_word(self) -> None:
        """Test single word returns one."""
        assert word_count("hello") == 1

    def test_multiple_spaces(self) -> None:
        """Test multiple spaces between words."""
        assert word_count("hello    world") == 2

    def test_newlines_and_tabs(self) -> None:
        """Test words separated by various whitespace."""
        assert word_count("hello\nworld\tthere") == 3


class TestWordCountMemo:
    """Tests for word_count_memo function."""

    def test_counts_and_memoizes_new_document(self) -> None:
        """Test counting a new document adds it to memos."""
        memos: dict[str, int] = {}
        count, new_memos = word_count_memo("hello world", memos)
        assert count == 2
        assert new_memos == {"hello world": 2}

    def test_returns_cached_count(self) -> None:
        """Test that cached document returns memoized count."""
        memos = {"hello world": 2}
        count, new_memos = word_count_memo("hello world", memos)
        assert count == 2
        assert new_memos == {"hello world": 2}

    def test_does_not_mutate_original_memos(self) -> None:
        """Test that original memos dict is not modified."""
        memos: dict[str, int] = {}
        original_copy = memos.copy()
        word_count_memo("hello world", memos)
        assert memos == original_copy

    def test_preserves_existing_memos(self) -> None:
        """Test that existing memos are preserved when adding new."""
        memos = {"existing doc": 5}
        count, new_memos = word_count_memo("hello world", memos)
        assert count == 2
        assert new_memos == {"existing doc": 5, "hello world": 2}

    def test_empty_document(self) -> None:
        """Test counting empty document."""
        memos: dict[str, int] = {}
        count, new_memos = word_count_memo("", memos)
        assert count == 0
        assert new_memos == {"": 0}
