"""Tests for main module."""

import pytest

from main import (
    add_border,
    add_prefix,
    center_title,
    choose_parser,
    file_to_prompt,
    format_line,
    get_median_font_size,
    hex_to_rgb,
    is_hexadecimal,
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
