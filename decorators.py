from collections.abc import Callable


def configure_plugin_decorator(
    func: Callable[..., dict[str, str | None]],
) -> Callable[..., dict[str, str | None]]:
    def wrapper(*args: tuple[str, str | None]) -> dict[str, str | None]:
        return func(**dict(args))

    return wrapper


def markdown_to_text_decorator(
    func: Callable[..., str],
) -> Callable[..., str]:
    def wrapper(*args: str, **kwargs: str) -> str:
        new_list = list(map(convert_md_to_txt, args))
        new_dict = {key: convert_md_to_txt(value) for key, value in kwargs.items()}
        return func(*new_list, **new_dict)

    return wrapper


def convert_md_to_txt(doc: str) -> str:
    lines = doc.split("\n")
    for i, line in enumerate(lines):
        lines[i] = line.lstrip("# ")
    return "\n".join(lines)
