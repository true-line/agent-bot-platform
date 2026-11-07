#!/usr/bin/env python3
"""pdf2md.py - Extract PDF text to Markdown with page markers.

Usage:
  python3 -I pdf2md.py <input.pdf> <output.md> "<Document title>"
"""
import sys

from pypdf import PdfReader


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(2)
    src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
    reader = PdfReader(src)
    parts = [
        "# %s\n" % title,
        "",
        "> Converted from `%s` (%d pages) with scripts/pdf2md.py — "
        "PDF text extraction is best-effort; curate before treating as "
        "normative. The original PDF is authoritative." % (src, len(reader.pages)),
        "",
    ]
    for i, page in enumerate(reader.pages, 1):
        parts.append("\n<!-- page %d -->\n" % i)
        parts.append(page.extract_text() or "")
        parts.append("\n")
    md = "\n".join(parts)
    md = "\n".join(line.rstrip() for line in md.split("\n"))
    with open(dst, "w", encoding="utf-8") as f:
        f.write(md.strip() + "\n")
    print("wrote %s (%d pages, %d bytes)" % (dst, len(reader.pages), len(md)))


if __name__ == "__main__":
    main()
