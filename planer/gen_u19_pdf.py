#!/usr/bin/env python3
"""Generate a training-plan PDF from Markdown using local Chrome."""

from __future__ import annotations

import html
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


PLAN = Path(__file__).with_name("treningsplan-u19.md")
OUTPUT = PLAN.with_suffix(".pdf")
CHROME_MACOS = Path(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)


def inline_markup(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<!_)_([^_]+?)_(?!_)", r"<em>\1</em>", text)
    return text


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(lines: list[str]) -> str:
    rows = [table_cells(line) for line in lines]
    if len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", cell) for cell in rows[1]):
        rows.pop(1)

    header = rows[0]
    if header and header[0].casefold() == "sone":
        table_class = "zone-table"
    elif len(header) == 4:
        table_class = "summary-table"
    else:
        table_class = "week-table"

    head = "".join(f"<th>{inline_markup(cell)}</th>" for cell in header)
    body = "".join(
        "<tr>" + "".join(f"<td>{inline_markup(cell)}</td>" for cell in row) + "</tr>"
        for row in rows[1:]
    )
    return (
        f'<table class="{table_class}"><thead><tr>{head}</tr></thead>'
        f"<tbody>{body}</tbody></table>"
    )


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    blocks: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue

        if line.startswith("|"):
            table_lines = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            table = render_table(table_lines)
            total_index = index
            while total_index < len(lines) and not lines[total_index].strip():
                total_index += 1
            if (
                total_index < len(lines)
                and lines[total_index].strip().startswith("**Totalbelastning:**")
            ):
                total = inline_markup(lines[total_index].strip())
                blocks.append(
                    f'<div class="table-total">{table}<p>{total}</p></div>'
                )
                index = total_index + 1
            else:
                blocks.append(table)
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        if heading:
            level = len(heading.group(1))
            blocks.append(
                f"<h{level}>{inline_markup(heading.group(2))}</h{level}>"
            )
            index += 1
            continue

        if re.fullmatch(r"(?:-{3,}|\*{3,}|_{3,})", line):
            blocks.append('<hr class="section-rule">')
            index += 1
            continue

        if re.match(r"^\d+\.\s+", line):
            items = []
            while index < len(lines):
                item = re.match(r"^\s*\d+\.\s+(.+)$", lines[index])
                if not item:
                    if (
                        not lines[index].strip()
                        and index + 1 < len(lines)
                        and re.match(r"^\s*\d+\.\s+", lines[index + 1])
                    ):
                        index += 1
                        continue
                    break
                item_text = item.group(1).strip()
                index += 1
                while index < len(lines) and re.match(r"^\s{2,}\S", lines[index]):
                    item_text += " " + lines[index].strip()
                    index += 1
                items.append(f"<li>{inline_markup(item_text)}</li>")
            blocks.append("<ol>" + "".join(items) + "</ol>")
            continue

        paragraph = [lines[index]]
        index += 1
        while index < len(lines):
            next_line = lines[index].strip()
            if (
                not next_line
                or next_line.startswith("|")
                or re.match(r"^#{1,3}\s+", next_line)
                or re.fullmatch(r"(?:-{3,}|\*{3,}|_{3,})", next_line)
                or re.match(r"^\d+\.\s+", next_line)
            ):
                break
            paragraph.append(lines[index])
            index += 1
        rendered_lines = []
        for line_index, raw_line in enumerate(paragraph):
            rendered_lines.append(inline_markup(raw_line.rstrip()))
            if line_index + 1 < len(paragraph):
                rendered_lines.append("<br>" if raw_line.endswith("  ") else " ")
        blocks.append("<p>" + "".join(rendered_lines) + "</p>")

    return "\n".join(blocks)


def find_chrome() -> str:
    configured = os.environ.get("CHROME_BIN")
    if configured:
        return configured
    for candidate in ("google-chrome", "chrome", "chromium", "chromium-browser"):
        executable = shutil.which(candidate)
        if executable:
            return executable
    if CHROME_MACOS.is_file():
        return str(CHROME_MACOS)
    raise FileNotFoundError(
        "Chrome/Chromium was not found. Set CHROME_BIN to its executable path."
    )


def stop_chrome(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def is_complete_pdf(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size == 0:
        return False
    with path.open("rb") as pdf:
        start = pdf.read(5)
        pdf.seek(max(0, path.stat().st_size - 1024))
        end = pdf.read()
    return start == b"%PDF-" and b"%%EOF" in end


def generate_pdf(
    plan: Path = PLAN,
    output: Path = OUTPUT,
    footer_label: str = "TVK U19",
) -> None:
    markdown = plan.read_text(encoding="utf-8")
    title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    title = title_match.group(1) if title_match else "TVK U19 treningsplan"
    year_match = re.search(r"sesongen\s+(\d{4})", title, re.IGNORECASE)
    year = year_match.group(1) if year_match else ""
    body = render_markdown(markdown)
    document = f"""<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
  @page {{
    size: A4;
    margin: 17mm 16mm 18mm;
    @bottom-right {{
      content: "{html.escape(footer_label)} · {year} · " counter(page);
      color: #194794;
      font: 8pt Arial, sans-serif;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    color: #20242b;
    font: 9pt/1.38 Arial, "Helvetica Neue", sans-serif;
  }}
  h1 {{
    color: #194794;
    font-size: 19pt;
    line-height: 1.15;
    text-align: center;
    margin: 0 0 16pt;
  }}
  h2 {{
    color: #194794;
    font-size: 14pt;
    margin: 18pt 0 6pt;
    break-after: avoid-page;
  }}
  h3 {{
    color: #e2071d;
    font-size: 11pt;
    margin: 12pt 0 5pt;
    break-after: avoid-page;
  }}
  p {{ margin: 0 0 7pt; }}
  strong {{ color: #194794; }}
  em {{ color: #555; }}
  hr.section-rule {{
    border: 0;
    border-top: 1px solid #194794;
    margin: 12pt 0 5pt;
  }}
  table {{
    border-collapse: collapse;
    table-layout: fixed;
    width: 100%;
    margin: 4pt 0 6pt;
    font-size: 8.3pt;
    line-height: 1.25;
    break-inside: avoid-page;
  }}
  .table-total {{
    break-before: avoid-page;
    break-inside: avoid-page;
  }}
  thead {{ display: table-header-group; }}
  th {{
    background: #194794;
    color: white;
    font-weight: bold;
    text-align: left;
  }}
  th, td {{
    border: 0.5pt solid #c9cdd5;
    padding: 4pt 5pt;
    vertical-align: top;
    overflow-wrap: anywhere;
  }}
  tbody tr:nth-child(even) {{ background: #e8ecf5; }}
  .week-table th:first-child, .week-table td:first-child {{ width: 15%; }}
  .week-table th:last-child, .week-table td:last-child {{ width: 15%; }}
  .summary-table th:first-child, .summary-table td:first-child {{ width: 18%; }}
  .summary-table th:last-child, .summary-table td:last-child {{ width: 20%; }}
  .zone-table th:first-child, .zone-table td:first-child {{ width: 11%; }}
  .zone-table th:nth-child(2), .zone-table td:nth-child(2) {{ width: 24%; }}
  tr {{ break-inside: avoid; }}
  ol {{ margin: 2pt 0 8pt; padding-left: 22pt; break-inside: avoid-page; }}
  li {{ margin: 0 0 3pt; }}
  @media print {{
    h2, h3 {{ break-after: avoid; }}
    table {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
<main>{body}</main>
</body>
</html>"""

    chrome = find_chrome()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"{output.stem}-pdf-") as temp_dir:
        temp_path = Path(temp_dir)
        html_path = temp_path / "plan.html"
        candidate_pdf = temp_path / "plan.pdf"
        stderr_path = temp_path / "chrome-stderr.log"
        html_path.write_text(document, encoding="utf-8")
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--no-first-run",
            "--no-default-browser-check",
            "--no-pdf-header-footer",
            f"--user-data-dir={temp_path / 'chrome-profile'}",
            f"--print-to-pdf={candidate_pdf}",
            html_path.resolve().as_uri(),
        ]
        with stderr_path.open("w", encoding="utf-8") as stderr:
            process = subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=stderr,
            )
            deadline = time.monotonic() + 120
            previous_size = -1
            stable_checks = 0
            finished_writing = False

            while time.monotonic() < deadline:
                if process.poll() is not None:
                    break
                size = (
                    candidate_pdf.stat().st_size
                    if candidate_pdf.is_file()
                    else -1
                )
                if size > 0 and size == previous_size:
                    stable_checks += 1
                    if stable_checks >= 4:
                        # Chrome on macOS can stay alive after finishing the PDF.
                        finished_writing = True
                        stop_chrome(process)
                        break
                else:
                    stable_checks = 0
                previous_size = size
                time.sleep(0.5)
            else:
                stop_chrome(process)
                raise TimeoutError("Chrome did not finish rendering the PDF.")

            if process.poll() is not None and process.returncode == 0:
                finished_writing = True
            if not finished_writing or not is_complete_pdf(candidate_pdf):
                details = stderr_path.read_text(encoding="utf-8").strip()
                raise RuntimeError(
                    "Chrome failed to create a complete PDF."
                    + (f"\nChrome output: {details}" if details else "")
                )

        with tempfile.NamedTemporaryFile(
            dir=output.parent,
            prefix=f".{output.stem}-",
            suffix=".pdf",
            delete=False,
        ) as staged_file:
            staged_path = Path(staged_file.name)
        try:
            shutil.copy2(candidate_pdf, staged_path)
            if not is_complete_pdf(staged_path):
                raise RuntimeError("The staged PDF is incomplete.")
            staged_path.replace(output)
        finally:
            staged_path.unlink(missing_ok=True)

    print(f"PDF generated from {plan.name}: {output}")


def main() -> None:
    generate_pdf()


if __name__ == "__main__":
    main()
