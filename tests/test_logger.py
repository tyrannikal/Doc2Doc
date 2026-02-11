"""Tests for logger module."""

from __future__ import annotations

from typing import TYPE_CHECKING

from logger import args_logger

if TYPE_CHECKING:
    import pytest


class TestArgsLogger:
    """Tests for args_logger function."""

    def test_prints_numbered_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that positional args are printed with 1-based numbering."""
        args_logger("first", "second", "third")
        captured = capsys.readouterr()
        assert "1. first" in captured.out
        assert "2. second" in captured.out
        assert "3. third" in captured.out

    def test_prints_sorted_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that kwargs are printed sorted by key with asterisk prefix."""
        args_logger(z_key="z_val", a_key="a_val")
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == "* a_key: a_val"
        assert lines[1] == "* z_key: z_val"

    def test_mixed_args_and_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test output with both args and kwargs."""
        args_logger("hello", name="world", age="30")
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert lines[0] == "1. hello"
        assert lines[1] == "* age: 30"
        assert lines[2] == "* name: world"

    def test_no_args_or_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that calling with no arguments produces no output."""
        args_logger()
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_only_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test with only positional arguments."""
        args_logger("a", "b")
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        assert len(lines) == 2
        assert lines[0] == "1. a"
        assert lines[1] == "2. b"

    def test_only_kwargs(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test with only keyword arguments."""
        args_logger(key="value")
        captured = capsys.readouterr()
        assert captured.out.strip() == "* key: value"

    def test_args_with_various_types(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that args of different types are printed correctly."""
        args_logger(42, True, 3.14)
        captured = capsys.readouterr()
        assert "1. 42" in captured.out
        assert "2. True" in captured.out
        assert "3. 3.14" in captured.out

    def test_kwargs_with_various_types(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Test that kwargs with different value types are printed correctly."""
        args_logger(count=5, active=False)
        captured = capsys.readouterr()
        assert "* active: False" in captured.out
        assert "* count: 5" in captured.out
