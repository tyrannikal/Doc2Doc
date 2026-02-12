"""Tests for main module."""

# pylint: disable=too-many-lines

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from main import (
    NestedDocument,
    add_border,
    add_custom_command,
    add_format,
    add_line_break,
    add_prefix,
    capitalize_content,
    center_title,
    change_bullet_style,
    choose_parser,
    colon_delimit,
    convert_case,
    convert_file_format,
    convert_line,
    converted_font_size,
    count_nested_levels,
    create_markdown_image,
    css_styles,
    dash_delimit,
    doc_format_checker_and_converter,
    factorial_r,
    file_to_prompt,
    file_type_aggregator,
    file_type_getter,
    find_longest_word,
    fix_ellipsis,
    format_date,
    format_line,
    get_filter_cmd,
    get_logger,
    get_median_font_size,
    hex_to_rgb,
    is_hexadecimal,
    is_palindrome,
    join,
    join_first_sentences,
    lines_with_sequence,
    list_files,
    new_collection,
    new_resizer,
    pair_document_with_format,
    process_doc,
    remove_emphasis,
    remove_format,
    remove_invalid_lines,
    remove_line_emphasis,
    remove_word_emphasis,
    replace_bad,
    replace_ellipsis,
    restore_documents,
    reverse_content,
    save_document,
    sort_dates,
    stylize_title,
    sum_nested_list,
    word_count,
    word_count_aggregator,
    word_count_memo,
    zipmap,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any


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

    def test_adds_format_to_list(self) -> None:
        """Test adding a format to existing list."""
        formats = ["docx", "pdf"]
        result = add_format(formats, "txt")
        assert result == ["docx", "pdf", "txt"]

    def test_adds_to_empty_list(self) -> None:
        """Test adding format to empty list."""
        result = add_format([], "docx")
        assert result == ["docx"]

    def test_does_not_mutate_original(self) -> None:
        """Test that original list is not modified."""
        formats = ["docx", "pdf"]
        original_copy = formats.copy()
        add_format(formats, "txt")
        assert formats == original_copy

    def test_allows_duplicate_formats(self) -> None:
        """Test that duplicate formats can be added."""
        formats = ["docx", "pdf"]
        result = add_format(formats, "docx")
        assert result == ["docx", "pdf", "docx"]


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


class TestAddCustomCommand:
    """Tests for add_custom_command function."""

    def test_adds_command_to_dict(self) -> None:
        """Test adding a new command to existing dict."""

        def sample_func() -> str:
            return "hello"

        commands: dict[str, Callable[..., Any]] = {"existing": lambda: None}
        result = add_custom_command(commands, "new_cmd", sample_func)
        assert "new_cmd" in result
        assert result["new_cmd"] is sample_func

    def test_adds_to_empty_dict(self) -> None:
        """Test adding command to empty dict."""

        def sample_func() -> str:
            return "hello"

        commands: dict[str, Callable[..., Any]] = {}
        result = add_custom_command(commands, "cmd", sample_func)
        assert "cmd" in result
        assert result["cmd"] is sample_func

    def test_does_not_mutate_original(self) -> None:
        """Test that original dict is not modified."""

        def sample_func() -> str:
            return "hello"

        commands: dict[str, Callable[..., Any]] = {"existing": lambda: None}
        original_keys = set(commands.keys())
        add_custom_command(commands, "new_cmd", sample_func)
        assert set(commands.keys()) == original_keys

    def test_overwrites_existing_command(self) -> None:
        """Test that adding a command with existing name overwrites it."""

        def func1() -> str:
            return "first"

        def func2() -> str:
            return "second"

        commands: dict[str, Callable[..., Any]] = {"cmd": func1}
        result = add_custom_command(commands, "cmd", func2)
        assert result["cmd"] is func2


class TestSaveDocument:
    """Tests for save_document function."""

    def test_saves_document_to_dict(self) -> None:
        """Test saving a new document."""
        docs: dict[str, str] = {}
        result = save_document(docs, "file.txt", "content")
        assert result == {"file.txt": "content"}

    def test_preserves_existing_documents(self) -> None:
        """Test that existing documents are preserved."""
        docs = {"existing.txt": "old content"}
        result = save_document(docs, "new.txt", "new content")
        assert result == {"existing.txt": "old content", "new.txt": "new content"}

    def test_does_not_mutate_original(self) -> None:
        """Test that original dict is not modified."""
        docs: dict[str, str] = {"file.txt": "content"}
        original_copy = docs.copy()
        save_document(docs, "new.txt", "new content")
        assert docs == original_copy

    def test_overwrites_existing_document(self) -> None:
        """Test that saving with existing filename overwrites."""
        docs = {"file.txt": "old content"}
        result = save_document(docs, "file.txt", "new content")
        assert result == {"file.txt": "new content"}


class TestAddLineBreak:
    """Tests for add_line_break function."""

    def test_adds_double_newline(self) -> None:
        """Test that double newline is added to line."""
        assert add_line_break("hello") == "hello\n\n"

    def test_empty_string(self) -> None:
        """Test adding line break to empty string."""
        assert add_line_break("") == "\n\n"

    def test_line_with_existing_newline(self) -> None:
        """Test adding line break to line that already has newline."""
        assert add_line_break("hello\n") == "hello\n\n\n"


class TestFormatDate:
    """Tests for format_date function."""

    def test_converts_to_sortable_format(self) -> None:
        """Test converting MM-DD-YYYY to YYYY-MM-DD."""
        assert format_date("01-15-2024") == "2024-01-15"

    def test_different_date(self) -> None:
        """Test with different date values."""
        assert format_date("12-31-1999") == "1999-12-31"

    def test_zeroed_date(self) -> None:
        """Test with zeroed date format."""
        assert format_date("00-00-0000") == "0000-00-00"


class TestSortDates:
    """Tests for sort_dates function."""

    def test_sorts_dates_chronologically(self) -> None:
        """Test that dates are sorted in chronological order."""
        dates = ["12-31-2024", "01-01-2020", "06-15-2022"]
        result = sort_dates(dates)
        assert result == ["01-01-2020", "06-15-2022", "12-31-2024"]

    def test_empty_list(self) -> None:
        """Test sorting empty list."""
        assert sort_dates([]) == []

    def test_single_date(self) -> None:
        """Test sorting single date."""
        assert sort_dates(["05-20-2023"]) == ["05-20-2023"]

    def test_already_sorted(self) -> None:
        """Test list that is already sorted."""
        dates = ["01-01-2020", "01-01-2021", "01-01-2022"]
        assert sort_dates(dates) == dates

    def test_does_not_mutate_original(self) -> None:
        """Test that original list is not modified."""
        dates = ["12-31-2024", "01-01-2020"]
        original_copy = dates.copy()
        sort_dates(dates)
        assert dates == original_copy


class TestFactorialR:
    """Tests for factorial_r function."""

    def test_factorial_of_zero(self) -> None:
        """Test that factorial of 0 is 1."""
        assert factorial_r(0) == 1

    def test_factorial_of_one(self) -> None:
        """Test that factorial of 1 is 1."""
        assert factorial_r(1) == 1

    def test_factorial_of_five(self) -> None:
        """Test that factorial of 5 is 120."""
        assert factorial_r(5) == 120

    def test_factorial_of_ten(self) -> None:
        """Test that factorial of 10 is 3628800."""
        assert factorial_r(10) == 3628800

    def test_factorial_of_small_numbers(self) -> None:
        """Test factorial of small numbers 2, 3, 4."""
        assert factorial_r(2) == 2
        assert factorial_r(3) == 6
        assert factorial_r(4) == 24


class TestZipmap:
    """Tests for zipmap function."""

    def test_zips_equal_length_lists(self) -> None:
        """Test zipping two lists of equal length."""
        keys = ["a", "b", "c"]
        values = [1, 2, 3]
        result = zipmap(keys, values)
        assert result == {"a": 1, "b": 2, "c": 3}

    def test_empty_keys_list(self) -> None:
        """Test with empty keys list returns empty dict."""
        assert zipmap([], [1, 2, 3]) == {}

    def test_empty_values_list(self) -> None:
        """Test with empty values list returns empty dict."""
        assert zipmap(["a", "b"], []) == {}

    def test_both_empty_lists(self) -> None:
        """Test with both empty lists returns empty dict."""
        assert zipmap([], []) == {}

    def test_single_element_lists(self) -> None:
        """Test zipping single element lists."""
        assert zipmap(["key"], ["value"]) == {"key": "value"}

    def test_more_keys_than_values(self) -> None:
        """Test when keys list is longer than values list."""
        keys = ["a", "b", "c", "d"]
        values = [1, 2, 3]
        result = zipmap(keys, values)
        assert result == {"a": 1, "b": 2, "c": 3}

    def test_more_values_than_keys(self) -> None:
        """Test when values list is longer than keys list."""
        keys = ["a", "b"]
        values = [1, 2, 3, 4]
        result = zipmap(keys, values)
        assert result == {"a": 1, "b": 2}

    def test_mixed_types(self) -> None:
        """Test zipping lists with mixed types."""
        keys = ["name", "age", "active"]
        values = ["Alice", 30, True]
        result = zipmap(keys, values)
        assert result == {"name": "Alice", "age": 30, "active": True}


class TestSumNestedList:
    """Tests for sum_nested_list function."""

    def test_flat_list(self) -> None:
        """Test summing a flat list of integers."""
        assert sum_nested_list([1, 2, 3]) == 6

    def test_empty_list(self) -> None:
        """Test that empty list returns zero."""
        assert sum_nested_list([]) == 0

    def test_single_int(self) -> None:
        """Test list with a single integer."""
        assert sum_nested_list([5]) == 5

    def test_one_level_nesting(self) -> None:
        """Test list with one level of nesting."""
        assert sum_nested_list([1, [2, 3]]) == 6

    def test_deep_nesting(self) -> None:
        """Test deeply nested list."""
        assert sum_nested_list([1, [2, [3, [4]]]]) == 10

    def test_all_nested(self) -> None:
        """Test list where all elements are nested lists."""
        assert sum_nested_list([[1, 2], [3, 4]]) == 10

    def test_nested_empty_lists(self) -> None:
        """Test list containing empty nested lists."""
        assert sum_nested_list([1, [], [2, []], 3]) == 6


class TestListFiles:
    """Tests for list_files function."""

    def test_empty_directory(self) -> None:
        """Test that empty directory returns empty list."""
        assert not list_files({})

    def test_single_file(self) -> None:
        """Test directory with a single file."""
        assert list_files({"file.txt": None}) == ["/file.txt"]

    def test_multiple_files(self) -> None:
        """Test directory with multiple files."""
        result = list_files({"a.txt": None, "b.txt": None})
        assert "/a.txt" in result
        assert "/b.txt" in result
        assert len(result) == 2

    def test_nested_directory(self) -> None:
        """Test file inside a subdirectory."""
        assert list_files({"dir": {"file.txt": None}}) == ["/dir/file.txt"]

    def test_deep_nesting(self) -> None:
        """Test deeply nested directory structure."""
        tree: dict[str, Any] = {"a": {"b": {"c.txt": None}}}
        assert list_files(tree) == ["/a/b/c.txt"]

    def test_mixed_files_and_directories(self) -> None:
        """Test directory with both files and subdirectories."""
        tree: dict[str, Any] = {
            "readme.md": None,
            "src": {"main.py": None},
        }
        result = list_files(tree)
        assert "/readme.md" in result
        assert "/src/main.py" in result
        assert len(result) == 2

    def test_custom_filepath_prefix(self) -> None:
        """Test with a custom starting filepath."""
        result = list_files({"file.txt": None}, "/home")
        assert result == ["/home/file.txt"]

    def test_empty_subdirectory(self) -> None:
        """Test directory containing an empty subdirectory."""
        tree: dict[str, Any] = {"file.txt": None, "empty_dir": {}}
        assert list_files(tree) == ["/file.txt"]


class TestFindLongestWord:
    """Tests for find_longest_word function."""

    def test_single_word(self) -> None:
        """Test document with a single word."""
        assert find_longest_word("hello") == "hello"

    def test_multiple_words(self) -> None:
        """Test document with multiple words of different lengths."""
        assert find_longest_word("I am extraordinary") == "extraordinary"

    def test_empty_string(self) -> None:
        """Test that empty string returns empty string."""
        assert find_longest_word("") == ""

    def test_whitespace_only(self) -> None:
        """Test that whitespace-only string returns empty string."""
        assert find_longest_word("   ") == ""

    def test_equal_length_words(self) -> None:
        """Test that first longest word is returned when tied."""
        assert find_longest_word("cat dog bat") == "cat"

    def test_longest_word_at_end(self) -> None:
        """Test when the longest word is at the end."""
        assert find_longest_word("a bb ccc") == "ccc"

    def test_longest_word_at_start(self) -> None:
        """Test when the longest word is at the start."""
        assert find_longest_word("longest ab c") == "longest"


class TestCountNestedLevels:
    """Tests for count_nested_levels function."""

    def test_finds_key_at_top_level(self) -> None:
        """Test finding a key at the top level returns 1."""
        tree: NestedDocument = {1: {2: {}}, 3: {}}
        assert count_nested_levels(tree, 1) == 1

    def test_finds_key_at_second_level(self) -> None:
        """Test finding a key at the second level returns 2."""
        tree: NestedDocument = {1: {2: {3: {}}, 4: {5: {}}}, 6: {}}
        assert count_nested_levels(tree, 2) == 2

    def test_finds_key_at_deep_level(self) -> None:
        """Test finding a key deeply nested."""
        tree: NestedDocument = {
            1: {2: {3: {}, 4: {5: {}}}, 6: {}, 7: {8: {9: {10: {}}}}}
        }
        assert count_nested_levels(tree, 9) == 4

    def test_key_not_found_returns_negative_one(self) -> None:
        """Test that a missing key returns -1."""
        tree: NestedDocument = {1: {2: {3: {}}}}
        assert count_nested_levels(tree, 99) == -1

    def test_empty_dict_returns_negative_one(self) -> None:
        """Test that empty dict returns -1."""
        empty: NestedDocument = {}
        assert count_nested_levels(empty, 1) == -1

    def test_finds_leaf_key(self) -> None:
        """Test finding a key with an empty dict value."""
        tree: NestedDocument = {1: {2: {3: {}}}}
        assert count_nested_levels(tree, 3) == 3

    def test_finds_key_in_sibling_branch(self) -> None:
        """Test finding a key in a sibling branch."""
        tree: NestedDocument = {
            1: {2: {3: {}, 4: {5: {}}}, 6: {}, 7: {8: {9: {10: {}}}}}
        }
        assert count_nested_levels(tree, 5) == 4

    def test_skips_none_value_and_continues_search(self) -> None:
        """Test that a None value is skipped without recursion."""
        tree: dict[int, Any] = {1: None, 2: {3: {}}}
        assert count_nested_levels(tree, 3) == 2


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_callable(self) -> None:
        """Test that get_logger returns a callable."""
        logger = get_logger(colon_delimit)
        assert callable(logger)

    def test_logs_formatted_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that the logger prints the formatted output."""
        logger = get_logger(colon_delimit)
        logger("ERROR", "something broke")
        captured = capsys.readouterr()
        assert captured.out.strip().endswith("ERROR: something broke")

    def test_uses_custom_formatter(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that the logger uses the provided formatter."""
        logger = get_logger(dash_delimit)
        logger("WARN", "low disk")
        captured = capsys.readouterr()
        assert "WARN - low disk" in captured.out


class TestColonDelimit:
    """Tests for colon_delimit function."""

    def test_joins_with_colon(self) -> None:
        """Test that two strings are joined with colon and space."""
        assert colon_delimit("key", "value") == "key: value"

    def test_empty_strings(self) -> None:
        """Test with empty strings."""
        assert colon_delimit("", "") == ": "

    def test_first_empty(self) -> None:
        """Test with empty first string."""
        assert colon_delimit("", "value") == ": value"

    def test_second_empty(self) -> None:
        """Test with empty second string."""
        assert colon_delimit("key", "") == "key: "


class TestDashDelimit:
    """Tests for dash_delimit function."""

    def test_joins_with_dash(self) -> None:
        """Test that two strings are joined with dash."""
        assert dash_delimit("left", "right") == "left - right"

    def test_empty_strings(self) -> None:
        """Test with empty strings."""
        assert dash_delimit("", "") == " - "

    def test_first_empty(self) -> None:
        """Test with empty first string."""
        assert dash_delimit("", "right") == " - right"

    def test_second_empty(self) -> None:
        """Test with empty second string."""
        assert dash_delimit("left", "") == "left - "


class TestDocFormatCheckerAndConverter:
    """Tests for doc_format_checker_and_converter function."""

    def test_returns_callable(self) -> None:
        """Test that it returns a callable."""
        converter = doc_format_checker_and_converter(capitalize_content, ["txt"])
        assert callable(converter)

    def test_converts_valid_format(self) -> None:
        """Test conversion with a valid file format."""
        converter = doc_format_checker_and_converter(capitalize_content, ["txt", "md"])
        assert converter("doc.txt", "hello") == "HELLO"

    def test_raises_on_invalid_format(self) -> None:
        """Test that invalid file format raises ValueError."""
        converter = doc_format_checker_and_converter(capitalize_content, ["txt"])
        with pytest.raises(ValueError, match="invalid file format"):
            converter("doc.pdf", "hello")

    def test_uses_provided_conversion_function(self) -> None:
        """Test that the provided conversion function is applied."""
        converter = doc_format_checker_and_converter(reverse_content, ["md"])
        assert converter("file.md", "abc") == "cba"

    def test_multiple_valid_formats(self) -> None:
        """Test with multiple valid formats."""
        converter = doc_format_checker_and_converter(
            capitalize_content, ["txt", "md", "html"]
        )
        assert converter("file.md", "test") == "TEST"
        assert converter("file.html", "test") == "TEST"


class TestCapitalizeContent:
    """Tests for capitalize_content function."""

    def test_capitalizes_lowercase(self) -> None:
        """Test capitalizing lowercase text."""
        assert capitalize_content("hello world") == "HELLO WORLD"

    def test_already_uppercase(self) -> None:
        """Test that already uppercase text is unchanged."""
        assert capitalize_content("HELLO") == "HELLO"

    def test_empty_string(self) -> None:
        """Test capitalizing empty string."""
        assert capitalize_content("") == ""

    def test_mixed_case(self) -> None:
        """Test capitalizing mixed case text."""
        assert capitalize_content("HeLLo WoRLd") == "HELLO WORLD"


class TestReverseContent:
    """Tests for reverse_content function."""

    def test_reverses_string(self) -> None:
        """Test reversing a simple string."""
        assert reverse_content("hello") == "olleh"

    def test_empty_string(self) -> None:
        """Test reversing empty string."""
        assert reverse_content("") == ""

    def test_single_char(self) -> None:
        """Test reversing single character."""
        assert reverse_content("a") == "a"

    def test_palindrome(self) -> None:
        """Test reversing a palindrome."""
        assert reverse_content("racecar") == "racecar"


class TestGetFilterCmd:
    """Tests for get_filter_cmd function."""

    def test_returns_callable(self) -> None:
        """Test that it returns a callable."""
        cmd = get_filter_cmd(replace_bad, replace_ellipsis)
        assert callable(cmd)

    def test_option_one_applies_filter_one(self) -> None:
        """Test --one applies the first filter."""
        cmd = get_filter_cmd(replace_bad, replace_ellipsis)
        assert cmd("bad day", "--one") == "good day"

    def test_option_two_applies_filter_two(self) -> None:
        """Test --two applies the second filter."""
        cmd = get_filter_cmd(replace_bad, replace_ellipsis)
        assert cmd("wait..", "--two") == "wait..."

    def test_option_three_applies_both_filters(self) -> None:
        """Test --three applies filter_one then filter_two."""
        cmd = get_filter_cmd(replace_bad, fix_ellipsis)
        assert cmd("bad....", "--three") == "good..."

    def test_option_one_is_default(self) -> None:
        """Test that --one is the default option."""
        cmd = get_filter_cmd(replace_bad, replace_ellipsis)
        assert cmd("bad input", "--one") == "good input"

    def test_invalid_option_raises(self) -> None:
        """Test that invalid option raises ValueError."""
        cmd = get_filter_cmd(replace_bad, replace_ellipsis)
        with pytest.raises(ValueError, match="invalid option"):
            cmd("text", "--invalid")


class TestReplaceBad:
    """Tests for replace_bad function."""

    def test_replaces_bad_with_good(self) -> None:
        """Test replacing 'bad' with 'good'."""
        assert replace_bad("bad day") == "good day"

    def test_no_bad_present(self) -> None:
        """Test string without 'bad' is unchanged."""
        assert replace_bad("nice day") == "nice day"

    def test_multiple_occurrences(self) -> None:
        """Test replacing multiple occurrences."""
        assert replace_bad("bad bad") == "good good"

    def test_empty_string(self) -> None:
        """Test with empty string."""
        assert replace_bad("") == ""


class TestReplaceEllipsis:
    """Tests for replace_ellipsis function."""

    def test_replaces_double_dot(self) -> None:
        """Test replacing '..' with '...'."""
        assert replace_ellipsis("wait..") == "wait..."

    def test_no_double_dot(self) -> None:
        """Test string without '..' is unchanged."""
        assert replace_ellipsis("hello") == "hello"

    def test_empty_string(self) -> None:
        """Test with empty string."""
        assert replace_ellipsis("") == ""

    def test_single_dot(self) -> None:
        """Test that single dot is unchanged."""
        assert replace_ellipsis("end.") == "end."


class TestFixEllipsis:
    """Tests for fix_ellipsis function."""

    def test_fixes_four_dots(self) -> None:
        """Test replacing '....' with '...'."""
        assert fix_ellipsis("wait....") == "wait..."

    def test_no_four_dots(self) -> None:
        """Test string without '....' is unchanged."""
        assert fix_ellipsis("wait...") == "wait..."

    def test_empty_string(self) -> None:
        """Test with empty string."""
        assert fix_ellipsis("") == ""

    def test_preserves_three_dots(self) -> None:
        """Test that exactly three dots are preserved."""
        assert fix_ellipsis("ok...") == "ok..."


class TestWordCountAggregator:
    """Tests for word_count_aggregator function."""

    def test_returns_callable(self) -> None:
        """Test that it returns a callable."""
        agg = word_count_aggregator()
        assert callable(agg)

    def test_counts_single_document(self) -> None:
        """Test counting words in a single document."""
        agg = word_count_aggregator()
        assert agg("hello world") == 2

    def test_accumulates_across_calls(self) -> None:
        """Test that word count accumulates across multiple calls."""
        agg = word_count_aggregator()
        assert agg("hello world") == 2
        assert agg("one more") == 4
        assert agg("three more words") == 7

    def test_empty_string(self) -> None:
        """Test that empty string adds zero to count."""
        agg = word_count_aggregator()
        assert agg("") == 0

    def test_empty_after_nonempty(self) -> None:
        """Test that empty string does not change accumulated count."""
        agg = word_count_aggregator()
        assert agg("two words") == 2
        assert agg("") == 2

    def test_separate_aggregators_are_independent(self) -> None:
        """Test that separate aggregators have independent counts."""
        agg1 = word_count_aggregator()
        agg2 = word_count_aggregator()
        agg1("hello world")
        assert agg1("more") == 3
        assert agg2("single") == 1


class TestNewCollection:
    """Tests for new_collection function."""

    def test_returns_callable(self) -> None:
        """Test that new_collection returns a callable."""
        add_doc = new_collection([])
        assert callable(add_doc)

    def test_adds_document_to_empty_collection(self) -> None:
        """Test adding a document to an initially empty collection."""
        add_doc = new_collection([])
        result = add_doc("new doc")
        assert result == ["new doc"]

    def test_adds_document_to_existing_collection(self) -> None:
        """Test adding a document to a collection with initial docs."""
        add_doc = new_collection(["doc1", "doc2"])
        result = add_doc("doc3")
        assert result == ["doc1", "doc2", "doc3"]

    def test_accumulates_across_calls(self) -> None:
        """Test that documents accumulate across multiple add_doc calls."""
        add_doc = new_collection(["doc1"])
        add_doc("doc2")
        result = add_doc("doc3")
        assert result == ["doc1", "doc2", "doc3"]

    def test_does_not_mutate_original_list(self) -> None:
        """Test that the original list passed in is not modified."""
        initial = ["doc1", "doc2"]
        original_copy = initial.copy()
        add_doc = new_collection(initial)
        add_doc("doc3")
        assert initial == original_copy

    def test_separate_collections_are_independent(self) -> None:
        """Test that separate collections do not share state."""
        add_doc1 = new_collection(["shared"])
        add_doc2 = new_collection(["shared"])
        add_doc1("only in 1")
        result2 = add_doc2("only in 2")
        assert result2 == ["shared", "only in 2"]

    def test_multiple_adds_then_check(self) -> None:
        """Test adding several documents sequentially."""
        add_doc = new_collection([])
        add_doc("a")
        add_doc("b")
        result = add_doc("c")
        assert result == ["a", "b", "c"]


class TestCssStyles:
    """Tests for css_styles function."""

    def test_returns_callable(self) -> None:
        """Test that css_styles returns a callable."""
        add_style = css_styles({})
        assert callable(add_style)

    def test_adds_style_to_empty_styles(self) -> None:
        """Test adding a style to an initially empty styles dict."""
        add_style = css_styles({})
        result = add_style("body", "color", "red")
        assert result == {"body": {"color": "red"}}

    def test_adds_style_to_existing_selector(self) -> None:
        """Test adding a property to an existing selector."""
        add_style = css_styles({"body": {"color": "red"}})
        result = add_style("body", "font-size", "12px")
        assert result == {"body": {"color": "red", "font-size": "12px"}}

    def test_adds_new_selector(self) -> None:
        """Test adding a style to a new selector preserves existing ones."""
        add_style = css_styles({"body": {"color": "red"}})
        result = add_style("h1", "font-weight", "bold")
        assert result == {"body": {"color": "red"}, "h1": {"font-weight": "bold"}}

    def test_accumulates_across_calls(self) -> None:
        """Test that styles accumulate across multiple calls."""
        add_style = css_styles({})
        add_style("body", "color", "red")
        add_style("body", "margin", "0")
        result = add_style("h1", "font-size", "24px")
        assert result == {
            "body": {"color": "red", "margin": "0"},
            "h1": {"font-size": "24px"},
        }

    def test_does_not_mutate_original_dict(self) -> None:
        """Test that the original dict passed in is not modified."""
        initial: dict[str, dict[str, str]] = {"body": {"color": "red"}}
        add_style = css_styles(initial)
        add_style("body", "margin", "0")
        assert initial == {"body": {"color": "red"}}

    def test_overwrites_existing_property(self) -> None:
        """Test that adding a duplicate property overwrites the value."""
        add_style = css_styles({"body": {"color": "red"}})
        result = add_style("body", "color", "blue")
        assert result == {"body": {"color": "blue"}}

    def test_separate_style_instances_are_independent(self) -> None:
        """Test that separate css_styles instances do not share state."""
        add_style1 = css_styles({"body": {}})
        add_style2 = css_styles({"body": {}})
        add_style1("body", "color", "red")
        result2 = add_style2("body", "color", "blue")
        assert result2 == {"body": {"color": "blue"}}


class TestConvertedFontSize:
    """Tests for converted_font_size function."""

    def test_returns_callable(self) -> None:
        """Test that converted_font_size returns a callable."""
        converter = converted_font_size(12)
        assert callable(converter)

    def test_txt_returns_same_size(self) -> None:
        """Test that txt doc type returns the original font size."""
        converter = converted_font_size(12)
        assert converter("txt") == 12

    def test_md_returns_double_size(self) -> None:
        """Test that md doc type returns double the font size."""
        converter = converted_font_size(16)
        assert converter("md") == 32

    def test_docx_returns_triple_size(self) -> None:
        """Test that docx doc type returns triple the font size."""
        converter = converted_font_size(10)
        assert converter("docx") == 30

    def test_invalid_doc_type_raises(self) -> None:
        """Test that an invalid doc type raises ValueError."""
        converter = converted_font_size(12)
        with pytest.raises(ValueError, match="invalid doc type"):
            converter("html")

    def test_zero_font_size(self) -> None:
        """Test that zero font size returns zero for all valid types."""
        converter = converted_font_size(0)
        assert converter("txt") == 0
        assert converter("md") == 0
        assert converter("docx") == 0

    def test_separate_converters_are_independent(self) -> None:
        """Test that separate converters maintain their own font size."""
        small = converted_font_size(8)
        large = converted_font_size(24)
        assert small("md") == 16
        assert large("md") == 48


class TestLinesWithSequence:
    """Tests for lines_with_sequence function."""

    def test_returns_callable_chain(self) -> None:
        """Test that lines_with_sequence returns nested callables."""
        with_char = lines_with_sequence("#")
        assert callable(with_char)
        with_length = with_char(3)
        assert callable(with_length)

    def test_counts_lines_with_matching_sequence(self) -> None:
        """Test counting lines containing the exact sequence."""
        count = lines_with_sequence("#")(3)("###\n@##\n$$$\n###")
        assert count == 2

    def test_sequence_as_substring(self) -> None:
        """Test that sequence matches as a substring within lines."""
        count = lines_with_sequence("$")(2)("$$$\n$\n***\n@@@\n$$\n$$$")
        assert count == 3

    def test_empty_doc_returns_zero(self) -> None:
        """Test that an empty document returns zero."""
        count = lines_with_sequence("%")(1)("")
        assert count == 0

    def test_longer_doc_with_multiple_matches(self) -> None:
        """Test a longer document with multiple matching lines."""
        count = lines_with_sequence("*")(3)("***\n*\n$$$$$$\nxxx\n****\n***\n***")
        assert count == 4

    def test_no_lines_match(self) -> None:
        """Test when no lines contain the sequence."""
        count = lines_with_sequence("@")(2)("abc\ndef\nghi")
        assert count == 0

    def test_all_lines_match(self) -> None:
        """Test when all lines contain the sequence."""
        count = lines_with_sequence("x")(1)("ax\nbx\ncx")
        assert count == 3

    def test_length_one_sequence(self) -> None:
        """Test with a single character sequence."""
        count = lines_with_sequence("a")(1)("a\nb\na")
        assert count == 2


class TestCreateMarkdownImage:
    """Tests for create_markdown_image function."""

    def test_returns_callable_chain(self) -> None:
        """Test that create_markdown_image returns nested callables."""
        prep_url = create_markdown_image("alt")
        assert callable(prep_url)
        prep_title = prep_url("https://example.com/img.png")
        assert callable(prep_title)

    def test_basic_image_no_title(self) -> None:
        """Test generating a markdown image without a title."""
        result = create_markdown_image("a cat")("https://example.com/cat.png")("")
        assert result == "![a cat](https://example.com/cat.png)"

    def test_image_with_title(self) -> None:
        """Test generating a markdown image with a title."""
        result = create_markdown_image("a cat")("https://example.com/cat.png")(
            "Cat photo"
        )
        assert result == '![a cat](https://example.com/cat.png "Cat photo")'

    def test_empty_string_title(self) -> None:
        """Test that passing empty string title returns image without title."""
        result = create_markdown_image("logo")("https://example.com/logo.svg")("")
        assert result == "![logo](https://example.com/logo.svg)"

    def test_url_with_parentheses_escaped(self) -> None:
        """Test that parentheses in the URL are percent-encoded."""
        result = create_markdown_image("img")("https://example.com/image_(1).png")("")
        assert result == "![img](https://example.com/image_%281%29.png)"

    def test_url_with_parentheses_and_title(self) -> None:
        """Test URL parenthesis escaping combined with a title."""
        result = create_markdown_image("img")("https://example.com/image_(1).png")(
            "Photo"
        )
        assert result == '![img](https://example.com/image_%281%29.png "Photo")'

    def test_empty_alt_text(self) -> None:
        """Test with empty alt text."""
        result = create_markdown_image("")("https://example.com/img.png")("")
        assert result == "![](https://example.com/img.png)"

    def test_separate_instances_are_independent(self) -> None:
        """Test that separate calls produce independent closures."""
        img1 = create_markdown_image("first")("https://one.com/a.png")
        img2 = create_markdown_image("second")("https://two.com/b.png")
        assert img1("") == "![first](https://one.com/a.png)"
        assert img2("") == "![second](https://two.com/b.png)"


class TestNewResizer:
    """Tests for new_resizer function."""

    def test_returns_callable_chain(self) -> None:
        """Test that new_resizer returns nested callables."""
        get_resized = new_resizer(800, 600)
        assert callable(get_resized)
        resize = get_resized(100, 100)
        assert callable(resize)

    def test_clamps_width_to_max(self) -> None:
        """Test that width exceeding max is clamped."""
        resize = new_resizer(800, 600)(0, 0)
        assert resize(1000, 400) == (800, 400)

    def test_clamps_height_to_max(self) -> None:
        """Test that height exceeding max is clamped."""
        resize = new_resizer(800, 600)(0, 0)
        assert resize(400, 900) == (400, 600)

    def test_clamps_width_to_min(self) -> None:
        """Test that width below min is raised to min."""
        resize = new_resizer(800, 600)(200, 100)
        assert resize(50, 300) == (200, 300)

    def test_clamps_height_to_min(self) -> None:
        """Test that height below min is raised to min."""
        resize = new_resizer(800, 600)(200, 100)
        assert resize(300, 50) == (300, 100)

    def test_clamps_both_dimensions(self) -> None:
        """Test clamping both width and height simultaneously."""
        resize = new_resizer(800, 600)(200, 100)
        assert resize(1000, 50) == (800, 100)

    def test_value_within_bounds_unchanged(self) -> None:
        """Test that values within bounds are returned as-is."""
        resize = new_resizer(800, 600)(100, 100)
        assert resize(400, 300) == (400, 300)

    def test_value_at_exact_bounds(self) -> None:
        """Test that values at exactly min and max are unchanged."""
        resize = new_resizer(800, 600)(200, 100)
        assert resize(200, 100) == (200, 100)
        assert resize(800, 600) == (800, 600)

    def test_min_exceeds_max_width_raises(self) -> None:
        """Test that min_width > max_width raises ValueError."""
        with pytest.raises(ValueError, match="minimum size cannot exceed maximum size"):
            new_resizer(800, 600)(900, 0)

    def test_min_exceeds_max_height_raises(self) -> None:
        """Test that min_height > max_height raises ValueError."""
        with pytest.raises(ValueError, match="minimum size cannot exceed maximum size"):
            new_resizer(800, 600)(0, 700)

    def test_zero_min_bounds(self) -> None:
        """Test with zero minimum bounds."""
        resize = new_resizer(800, 600)(0, 0)
        assert resize(0, 0) == (0, 0)

    def test_separate_resizers_are_independent(self) -> None:
        """Test that separate resizers maintain independent bounds."""
        small = new_resizer(100, 100)(0, 0)
        large = new_resizer(2000, 2000)(0, 0)
        assert small(500, 500) == (100, 100)
        assert large(500, 500) == (500, 500)


class TestFileTypeAggregator:
    """Tests for file_type_aggregator decorator."""

    def test_returns_result_and_counts(self) -> None:
        """Test that decorated function returns result and counts dict."""

        @file_type_aggregator
        def dummy(doc: str, file_type: str) -> str:
            return f"{doc}-{file_type}"

        result, counts = dummy("hello", "txt")
        assert result == "hello-txt"
        assert counts == {"txt": 1}

    def test_accumulates_counts_per_file_type(self) -> None:
        """Test that counts accumulate per file type across calls."""

        @file_type_aggregator
        def dummy(doc: str, _file_type: str) -> str:
            return doc

        dummy("a", "txt")
        dummy("b", "txt")
        _, counts = dummy("c", "pdf")
        assert counts == {"txt": 2, "pdf": 1}

    def test_new_file_type_starts_at_one(self) -> None:
        """Test that a new file type starts with count of 1."""

        @file_type_aggregator
        def dummy(doc: str, _file_type: str) -> str:
            return doc

        _, counts = dummy("a", "md")
        assert counts["md"] == 1

    def test_preserves_decorated_function_result(self) -> None:
        """Test that the original function's return value is preserved."""

        @file_type_aggregator
        def upper_doc(doc: str, _file_type: str) -> str:
            return doc.upper()

        result, _ = upper_doc("hello", "txt")
        assert result == "HELLO"

    def test_separate_decorated_functions_have_independent_counts(self) -> None:
        """Test that separate decorated functions have independent state."""

        @file_type_aggregator
        def func_a(doc: str, _file_type: str) -> str:
            return doc

        @file_type_aggregator
        def func_b(doc: str, _file_type: str) -> str:
            return doc

        func_a("x", "txt")
        func_a("y", "txt")
        _, counts_b = func_b("z", "txt")
        assert counts_b == {"txt": 1}


class TestProcessDoc:
    """Tests for process_doc function."""

    def test_returns_formatted_string_and_counts(self) -> None:
        """Test that process_doc returns expected format and counts."""
        result, counts = process_doc("my doc", "pdf")  # pylint: disable=no-member
        assert result == "Processing doc: 'my doc'. File Type: pdf"
        assert "pdf" in counts

    def test_counts_accumulate(self) -> None:
        """Test that calling process_doc accumulates file type counts."""
        initial_result, initial_counts = process_doc("a", "txt")
        assert initial_result == "Processing doc: 'a'. File Type: txt"
        txt_count = initial_counts.get("txt", 0)  # pylint: disable=no-member
        _, updated_counts = process_doc("b", "txt")
        assert updated_counts["txt"] == txt_count + 1  # pylint: disable=invalid-sequence-index

    def test_different_file_types_tracked_separately(self) -> None:
        """Test that different file types are tracked independently."""
        _, counts = process_doc("doc", "html")
        html_count = counts["html"]  # pylint: disable=invalid-sequence-index
        _, counts = process_doc("doc", "html")
        assert counts["html"] == html_count + 1  # pylint: disable=invalid-sequence-index


class TestIsPalindrome:
    """Tests for is_palindrome function."""

    def test_simple_palindrome(self) -> None:
        """Test that a simple palindrome returns True."""
        assert is_palindrome("racecar") is True

    def test_single_character(self) -> None:
        """Test that a single character is a palindrome."""
        assert is_palindrome("a") is True

    def test_empty_string(self) -> None:
        """Test that an empty string is a palindrome."""
        assert is_palindrome("") is True

    def test_two_char_palindrome(self) -> None:
        """Test that a two character palindrome returns True."""
        assert is_palindrome("aa") is True

    def test_not_palindrome(self) -> None:
        """Test that a non-palindrome returns False."""
        assert is_palindrome("hello") is False

    def test_even_length_palindrome(self) -> None:
        """Test an even-length palindrome."""
        assert is_palindrome("abba") is True

    def test_one_char_difference(self) -> None:
        """Test that a near-palindrome returns False."""
        assert is_palindrome("racecab") is False
