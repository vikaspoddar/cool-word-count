from pathlib import Path
import click

ALIGNMENT = 8


def wc(filepath: Path) -> tuple[int, int, int]:
    content = filepath.read_bytes()
    byte_count = len(content)
    word_count = len(content.split())
    line_count = len(content.splitlines())
    return line_count, word_count, byte_count


def format_output(filepath: Path, lines: int, words: int, bytes_: int,
                  show_lines: bool, show_words: bool, show_bytes: bool) -> str:
    return (
        (f"{lines:>{ALIGNMENT}}" if show_lines else "")
        + (f"{words:>{ALIGNMENT}}" if show_words else "")
        + (f"{bytes_:>{ALIGNMENT}}" if show_bytes else "")
        + f" {filepath}"
    )


@click.command()
@click.argument("filepaths", type=Path, nargs=-1)
@click.option("-c", is_flag=True, help="Show byte count.")
@click.option("-w", is_flag=True, help="Show word count.")
@click.option("-l", is_flag=True, help="Show line count.")
def main(filepaths: tuple[Path, ...], c: bool, w: bool, l: bool) -> None:
    if {c, w, l} == {False}:
        c, w, l = True, True, True

    total_lines = total_words = total_bytes = 0

    for filepath in filepaths:
        lines, words, bytes_ = wc(filepath)

        total_lines += lines
        total_words += words
        total_bytes += bytes_

        print(format_output(filepath, lines, words, bytes_, l, w, c))

    # 🔥 New feature: total summary
    if len(filepaths) > 1:
        print(
            format_output(
                Path("total"),
                total_lines,
                total_words,
                total_bytes,
                l,
                w,
                c,
            )
        )
