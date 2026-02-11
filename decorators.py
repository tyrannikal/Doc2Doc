from collections.abc import Callable


def configure_plugin_decorator(
    func: Callable[..., dict[str, str | None]],
) -> Callable[..., dict[str, str | None]]:
    def wrapper(*args: tuple[str, str | None]) -> dict[str, str | None]:
        return func(**dict(args))

    return wrapper
