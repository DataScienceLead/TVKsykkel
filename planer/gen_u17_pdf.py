#!/usr/bin/env python3
"""Generate the U17 PDF from its Markdown source."""

from pathlib import Path

from gen_u19_pdf import generate_pdf


PLAN = Path(__file__).with_name("treningsplan-u17.md")
OUTPUT = PLAN.with_suffix(".pdf")


def main() -> None:
    generate_pdf(PLAN, OUTPUT, footer_label="TVK U17")


if __name__ == "__main__":
    main()
