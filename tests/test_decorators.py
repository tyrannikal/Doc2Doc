"""Tests for decorators module."""

from __future__ import annotations

from decorators import configure_plugin_decorator


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
