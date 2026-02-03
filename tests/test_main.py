"""Tests for main module."""

import pytest

from main import (
    add_border,
    add_prefix,
    center_title,
    change_bullet_style,
    choose_parser,
    convert_line,
    file_to_prompt,
    file_type_getter,
    format_line,
    get_median_font_size,
    hex_to_rgb,
    is_hexadecimal,
    remove_invalid_lines,
    stylize_title,
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
