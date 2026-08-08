#!/usr/bin/env python3
"""Save lecture-note Markdown beside a source PDF."""

from __future__ import annotations

import argparse
from pathlib import Path


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    index = 2
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write a Markdown lecture explanation next to the source PDF."
    )
    parser.add_argument("--pdf", required=True, help="Path to the source PDF.")
    parser.add_argument(
        "--content-file",
        required=True,
        help="Path to a UTF-8 Markdown file containing the lecture notes.",
    )
    parser.add_argument(
        "--output-name",
        help="Optional Markdown filename. Defaults to '<pdf-stem>_讲解笔记.md'.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the target file if it already exists.",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).expanduser().resolve()
    content_path = Path(args.content_file).expanduser().resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Source file is not a PDF: {pdf_path}")
    if not content_path.exists():
        raise FileNotFoundError(f"Content file not found: {content_path}")

    output_name = args.output_name or f"{pdf_path.stem}_\u8bb2\u89e3\u7b14\u8bb0.md"
    output_path = pdf_path.parent / output_name
    if output_path.suffix.lower() != ".md":
        output_path = output_path.with_suffix(".md")
    if not args.overwrite:
        output_path = unique_path(output_path)

    content = content_path.read_text(encoding="utf-8")
    output_path.write_text(content, encoding="utf-8", newline="\n")
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
