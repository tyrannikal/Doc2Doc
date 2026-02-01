from collections.abc import Callable

HEX_COLOR_LENGTH = 6


def stylize_title(document: str) -> str:
    return document.replace(document, add_border(center_title(document)))


def center_title(document: str) -> str:
    width: int = 40
    title: str = document.split("\n")[0]
    centered_title: str = title.center(width)
    return document.replace(title, centered_title)


def add_border(document: str) -> str:
    title: str = document.split("\n")[0]
    border: str = "*" * len(title)
    return document.replace(title, title + "\n" + border)


def add_prefix(document: str, documents: tuple[str, ...]) -> tuple[str, ...]:
    prefix: str = f"{len(documents)}. "
    new_doc: str = prefix + document
    documents = (
        *documents,
        new_doc,
    )
    return documents


def get_median_font_size(font_sizes: list[int]) -> int | None:
    if not font_sizes:
        return None
    return sorted(font_sizes)[(len(font_sizes) - 1) // 2]


def format_line(line: str) -> str:
    return f"{line.replace('.', '').upper().strip()}..."


def choose_parser(file_extension: str) -> str:
    return "markdown" if file_extension.lower() in ("markdown", "md") else "plaintext"


def hex_to_rgb(hex_color: str) -> tuple[int, ...]:
    if not is_hexadecimal(hex_color) or len(hex_color) != HEX_COLOR_LENGTH:
        raise TypeError("not a hex color string")

    r = int(hex_color[:2], base=16)
    g = int(hex_color[2:4], base=16)
    b = int(hex_color[4:], base=16)
    return r, g, b


def is_hexadecimal(hex_string: str) -> bool:
    try:
        int(hex_string, 16)
        return True
    except ValueError:
        return False


def file_to_prompt(
    file: dict[str, str], to_string: Callable[[dict[str, str]], str]
) -> str:
    return f"```\n{to_string(file)}\n```"
