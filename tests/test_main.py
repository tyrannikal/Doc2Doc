"""Tests for main module."""

from main import main


def test_main(capsys) -> None:
    """Test main function prints hello world."""
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
