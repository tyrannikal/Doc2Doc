from collections.abc import Callable
from functools import reduce

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


def file_type_getter(
    file_extension_tuples: list[tuple[str, list[str]]],
) -> Callable[[str], str]:
    ext_type_dict = {
        extension: doc_type[0]
        for doc_type in file_extension_tuples
        for extension in doc_type[1]
    }
    return lambda found_type: ext_type_dict.get(found_type, "Unknown")


def change_bullet_style(document: str) -> str:
    lines: list[str] = document.split("\n")
    return "\n".join(list(map(convert_line, lines)))


def convert_line(line: str) -> str:
    old_bullet: str = "-"
    new_bullet: str = "*"
    if len(line) > 0 and line[0] == old_bullet:
        return new_bullet + line[1:]
    return line


def remove_invalid_lines(document: str) -> str:
    lines = document.split("\n")
    return "\n".join(list(filter(lambda line: not line.startswith("-"), lines)))


def join(doc_so_far: str, sentence: str) -> str:
    return f"{doc_so_far}. {sentence}"


def join_first_sentences(sentences: list[str], n: int) -> str:
    return f"{reduce(join, sentences[:n])}." if n else ""


def pair_document_with_format(
    doc_names: list[str], doc_formats: list[str]
) -> list[tuple[str, str]]:
    valid_extensions = ["docx", "pdf", "txt", "pptx", "ppt", "md"]
    return list(
        filter(
            lambda valid_tuple: valid_tuple[1] in valid_extensions,
            list(zip(doc_names, doc_formats, strict=True)),
        )
    )


def restore_documents(originals: tuple[str, ...], backups: tuple[str, ...]) -> set[str]:
    return set(
        filter(
            lambda good_doc: not good_doc.isdigit(), map(str.upper, originals + backups)
        )
    )


def convert_file_format(filename: str, target_format: str) -> str | None:
    current_format = filename.split(".")[-1]
    valid_extensions = ["docx", "pdf", "txt", "pptx", "ppt", "md"]
    valid_conversions = {
        "docx": ["pdf", "txt", "md"],
        "pdf": ["docx", "txt", "md"],
        "txt": ["docx", "pdf", "md"],
        "pptx": ["ppt", "pdf"],
        "ppt": ["pptx", "pdf"],
        "md": ["docx", "pdf", "txt"],
    }
    if (
        current_format in valid_extensions
        and target_format in valid_conversions[current_format]
    ):
        return filename.replace(current_format, target_format)
    return None


def add_format(default_formats: dict[str, bool], new_format: str) -> dict[str, bool]:
    formats_updated = default_formats.copy()
    formats_updated[new_format] = True
    return formats_updated


def remove_format(default_formats: dict[str, bool], old_format: str) -> dict[str, bool]:
    formats_updated = default_formats.copy()
    formats_updated[old_format] = False
    return formats_updated


def convert_case(text: str, target_format: str) -> str:
    if not text or not target_format:
        raise ValueError("no text or target format provided")

    if target_format == "uppercase":
        return text.upper()
    if target_format == "lowercase":
        return text.lower()
    if target_format == "titlecase":
        return text.title()
    raise ValueError(f"unsupported format: {target_format}")


def remove_emphasis(doc: str) -> str:
    lines = doc.split("\n")
    new_lines = map(remove_line_emphasis, lines)
    return "\n".join(new_lines)


def remove_line_emphasis(line: str) -> str:
    words = line.split()
    new_words = map(remove_word_emphasis, words)
    return " ".join(new_words)


def remove_word_emphasis(word: str) -> str:
    return word.strip("*")


def word_count_memo(document: str, memos: dict[str, int]) -> tuple[int, dict[str, int]]:
    new_memos = memos.copy()
    if document in memos:
        return memos[document], new_memos
    count = word_count(document)
    new_memos[document] = count
    return count, new_memos


# Don't edit below this line


def word_count(document: str) -> int:
    count = len(document.split())
    return count
