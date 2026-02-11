"""Tests for plugins module."""

from __future__ import annotations

from plugins import configure_backups, configure_login


class TestConfigureBackups:
    """Tests for configure_backups function."""

    def test_defaults(self) -> None:
        """Test that defaults are returned when no args provided."""
        result = configure_backups()
        assert result == {
            "path": "~/backups",
            "prefix": "copy_",
            "extension": ".txt",
        }

    def test_override_all(self) -> None:
        """Test overriding all parameters."""
        result = configure_backups(
            ("path", "~/custom"),
            ("prefix", "bk_"),
            ("extension", ".md"),
        )
        assert result == {
            "path": "~/custom",
            "prefix": "bk_",
            "extension": ".md",
        }

    def test_override_partial(self) -> None:
        """Test overriding a single parameter keeps other defaults."""
        result = configure_backups(("path", "/custom"))
        assert result == {
            "path": "/custom",
            "prefix": "copy_",
            "extension": ".txt",
        }


class TestConfigureLogin:
    """Tests for configure_login function."""

    def test_defaults(self) -> None:
        """Test that defaults are all None."""
        result = configure_login()
        assert result == {
            "user": None,
            "password": None,
            "token": None,
        }

    def test_override_all(self) -> None:
        """Test overriding all parameters."""
        result = configure_login(
            ("user", "admin"),
            ("password", "secret"),
            ("token", "abc123"),
        )
        assert result == {
            "user": "admin",
            "password": "secret",
            "token": "abc123",
        }

    def test_override_partial(self) -> None:
        """Test overriding some parameters keeps other defaults."""
        result = configure_login(("token", "mytoken"))
        assert result == {
            "user": None,
            "password": None,
            "token": "mytoken",
        }

    def test_user_and_password_without_token(self) -> None:
        """Test setting user and password without token."""
        result = configure_login(("user", "john"), ("password", "pass123"))
        assert result == {
            "user": "john",
            "password": "pass123",
            "token": None,
        }
