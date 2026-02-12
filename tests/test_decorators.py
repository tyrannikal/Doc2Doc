"""Tests for decorators module."""

from __future__ import annotations

from decorators import (
    configure_plugin_decorator,
    convert_md_to_txt,
    markdown_to_text_decorator,
)


class TestConfigurePluginDecorator:
    """Tests for configure_plugin_decorator."""

    def test_returns_callable(self) -> None:
        """Test that the decorator returns a callable."""

        @configure_plugin_decorator
        def dummy(key: str = "default") -> dict[str, str | None]:
            return {"key": key}

        assert callable(dummy)

    def test_converts_tuple_args_to_kwargs(self) -> None:
        """Test that tuple positional args are passed as kwargs."""

        @configure_plugin_decorator
        def dummy(a: str = "", b: str = "") -> dict[str, str | None]:
            return {"a": a, "b": b}

        result = dummy(("a", "hello"), ("b", "world"))
        assert result == {"a": "hello", "b": "world"}

    def test_no_args_uses_defaults(self) -> None:
        """Test that calling with no args uses function defaults."""

        @configure_plugin_decorator
        def dummy(x: str = "default") -> dict[str, str | None]:
            return {"x": x}

        result = dummy()
        assert result == {"x": "default"}

    def test_partial_override(self) -> None:
        """Test that only specified args override defaults."""

        @configure_plugin_decorator
        def dummy(a: str = "1", b: str = "2") -> dict[str, str | None]:
            return {"a": a, "b": b}

        result = dummy(("a", "override"))
        assert result == {"a": "override", "b": "2"}

    def test_preserves_function_return_value(self) -> None:
        """Test that the decorated function's return value is passed through."""

        @configure_plugin_decorator
        def dummy(name: str = "test") -> dict[str, str | None]:
            return {"name": name, "extra": "added"}

        result = dummy(("name", "custom"))
        assert result == {"name": "custom", "extra": "added"}


class TestConvertMdToTxt:
    """Tests for convert_md_to_txt."""

    def test_strips_h1_header(self) -> None:
        """Test that h1 markdown header is stripped."""
        assert convert_md_to_txt("# Title") == "Title"

    def test_strips_h2_header(self) -> None:
        """Test that h2 markdown header is stripped."""
        assert convert_md_to_txt("## Subtitle") == "Subtitle"

    def test_plain_text_unchanged(self) -> None:
        """Test that plain text without headers is unchanged."""
        assert convert_md_to_txt("Hello world") == "Hello world"

    def test_multiline_with_mixed_headers(self) -> None:
        """Test multi-line doc with headers and plain text."""
        doc = "# Title\nBody text\n## Section"
        result = convert_md_to_txt(doc)
        assert result == "Title\nBody text\nSection"

    def test_empty_string(self) -> None:
        """Test that empty string returns empty string."""
        assert convert_md_to_txt("") == ""


class TestMarkdownToTextDecorator:
    """Tests for markdown_to_text_decorator."""

    def test_returns_callable(self) -> None:
        """Test that the decorator returns a callable."""

        @markdown_to_text_decorator
        def dummy(text: str) -> str:
            return text

        assert callable(dummy)

    def test_converts_positional_args(self) -> None:
        """Test that positional args are converted from markdown."""

        @markdown_to_text_decorator
        def dummy(a: str, b: str) -> str:
            return f"{a}|{b}"

        result = dummy("# Hello", "## World")
        assert result == "Hello|World"

    def test_converts_keyword_args(self) -> None:
        """Test that keyword args are converted from markdown."""

        @markdown_to_text_decorator
        def dummy(title: str = "", body: str = "") -> str:
            return f"{title}|{body}"

        result = dummy(title="# Header", body="## Sub")
        assert result == "Header|Sub"

    def test_converts_mixed_positional_and_keyword(self) -> None:
        """Test that both positional and keyword args are converted."""

        @markdown_to_text_decorator
        def dummy(a: str, b: str = "") -> str:
            return f"{a}|{b}"

        result = dummy("# Pos", b="## Kw")
        assert result == "Pos|Kw"

    def test_plain_text_passes_through(self) -> None:
        """Test that plain text args pass through unchanged."""

        @markdown_to_text_decorator
        def dummy(text: str) -> str:
            return text

        assert dummy("no markdown here") == "no markdown here"
