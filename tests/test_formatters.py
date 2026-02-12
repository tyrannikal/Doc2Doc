"""Tests for formatters module."""

from __future__ import annotations

from formatters import concat, format_as_essay


class TestConcat:
    """Tests for concat function."""

    def test_strips_markdown_from_both_args(self) -> None:
        """Test that markdown headers are stripped from both arguments."""
        result = concat("# First doc", "## Second doc")
        expected = "  First: First doc\n  Second: Second doc"
        assert result == expected

    def test_plain_text_unchanged(self) -> None:
        """Test that plain text passes through without modification."""
        result = concat("Hello", "World")
        expected = "  First: Hello\n  Second: World"
        assert result == expected

    def test_multiline_markdown(self) -> None:
        """Test concat with multi-line markdown arguments."""
        result = concat("# Title\nBody", "## Header\nContent")
        expected = "  First: Title\nBody\n  Second: Header\nContent"
        assert result == expected


class TestFormatAsEssay:
    """Tests for format_as_essay function."""

    def test_all_plain_text(self) -> None:
        """Test formatting with plain text arguments."""
        result = format_as_essay("My Title", "Some body", "The end")
        expected = "  Title: My Title\n  Body: Some body\n  Conclusion: The end"
        assert result == expected

    def test_strips_markdown_headers(self) -> None:
        """Test that markdown headers are stripped from all arguments."""
        result = format_as_essay("# My Title", "## Body text", "### Conclusion text")
        expected = "  Title: My Title\n  Body: Body text\n  Conclusion: Conclusion text"
        assert result == expected

    def test_keyword_arguments(self) -> None:
        """Test formatting with keyword arguments."""
        result = format_as_essay(
            title="Why Python is Great",
            body="Maybe it isn't",
            conclusion="## That's why Python is great!",
        )
        expected = (
            "  Title: Why Python is Great\n"
            "  Body: Maybe it isn't\n"
            "  Conclusion: That's why Python is great!"
        )
        assert result == expected

    def test_mixed_positional_and_keyword(self) -> None:
        """Test formatting with positional args and keyword conclusion."""
        result = format_as_essay(
            "# Boots' grocery list",
            "Salmon, gems, arcanum crystals",
            conclusion="## Don't forget!",
        )
        expected = (
            "  Title: Boots' grocery list\n"
            "  Body: Salmon, gems, arcanum crystals\n"
            "  Conclusion: Don't forget!"
        )
        assert result == expected
