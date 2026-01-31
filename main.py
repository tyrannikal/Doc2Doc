def stylize_title(document: str) -> str:
    return document.replace(document, add_border(center_title(document)))


# Don't touch below this line


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
