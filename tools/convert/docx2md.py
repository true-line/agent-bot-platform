#!/usr/bin/env python3
"""docx2md.py - Convert textutil HTML output (from .docx) to Markdown.

Usage:
  textutil -convert html -output /tmp/out.html "input.docx"
  python3 -I docx2md.py /tmp/out.html output.md

Handles headings, paragraphs, bold/italic/code, links, nested lists,
simple tables, blockquotes and pre blocks. Best-effort first pass;
curate the result afterwards.
"""
import html as html_mod
import re
import sys
from html.parser import HTMLParser

SKIP_TAGS = {"style", "script", "head", "title"}


class MD(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.list_stack = []          # [tag, counter]
        self.in_pre = False
        self.skip = 0
        self.a_stack = []             # start indices of open links
        self.cur_href = None
        self.in_table = False
        self.rows = []
        self.cur_row = None
        self.cur_cell = None
        self.in_cell_head = False

    # ---- output helpers -------------------------------------------------
    def emit(self, s):
        if s:
            self.out.append(s)

    def text_since(self, start):
        return "".join(self.out[start:])

    # ---- tag handlers ----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n%s " % ("#" * int(tag[1])))
        elif tag == "p":
            self.emit("\n\n")
        elif tag == "br":
            self.emit("\n" if not self.in_pre else "\n")
        elif tag == "hr":
            self.emit("\n\n---\n\n")
        elif tag in ("ul", "ol"):
            self.list_stack.append([tag, 0])
        elif tag == "li":
            depth = max(len(self.list_stack) - 1, 0)
            marker = "-"
            if self.list_stack and self.list_stack[-1][0] == "ol":
                self.list_stack[-1][1] += 1
                marker = "%d." % self.list_stack[-1][1]
            self.emit("\n" + "  " * depth + marker + " ")
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code":
            self.emit("`")
        elif tag == "pre":
            self.in_pre = True
            self.emit("\n\n```\n")
        elif tag == "a":
            self.a_stack.append(len(self.out))
            self.cur_href = dict(attrs).get("href") or ""
        elif tag == "blockquote":
            self.emit("\n\n> ")
        elif tag == "table":
            self.in_table = True
            self.rows = []
        elif tag == "tr":
            self.cur_row = []
        elif tag in ("td", "th"):
            self.cur_cell = []
            self.in_cell_head = tag == "th"

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n")
        elif tag == "p":
            self.emit("\n")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
        elif tag in ("strong", "b"):
            self.emit("**")
        elif tag in ("em", "i"):
            self.emit("*")
        elif tag == "code":
            self.emit("`")
        elif tag == "pre":
            self.in_pre = False
            self.emit("\n```\n\n")
        elif tag == "a":
            if self.a_stack:
                start = self.a_stack.pop()
                text = self.text_since(start).strip()
                del self.out[start:]
                if text:
                    self.emit("[%s](%s)" % (text, self.cur_href))
                elif self.cur_href:
                    self.emit("<%s>" % self.cur_href)
            self.cur_href = None
        elif tag == "blockquote":
            self.emit("\n")
        elif tag in ("td", "th"):
            if self.cur_row is not None and self.cur_cell is not None:
                self.cur_row.append(("".join(self.cur_cell)).strip())
            self.cur_cell = None
        elif tag == "tr":
            if self.cur_row:
                self.rows.append(self.cur_row)
            self.cur_row = None
        elif tag == "table":
            self.in_table = False
            self.flush_table()

    # ---- data / tables ----------------------------------------------------
    def handle_data(self, data):
        if self.skip:
            return
        if self.in_pre:
            self.emit(data)
            return
        text = re.sub(r"\s+", " ", data)
        if not text.strip():
            return
        if self.cur_cell is not None:
            self.cur_cell.append(text)
            return
        self.emit(text)

    def flush_table(self):
        rows = [r for r in self.rows if r]
        if not rows:
            return
        width = max(len(r) for r in rows)
        cells = []
        for r in rows:
            r = r + [""] * (width - len(r))
            cells.append([c.replace("|", "\\|").replace("\n", " ") for c in r])
        self.emit("\n\n")
        self.emit("| " + " | ".join(cells[0]) + " |\n")
        self.emit("|" + "|".join([" --- "] * width) + "|\n")
        for r in cells[1:]:
            self.emit("| " + " | ".join(r) + " |\n")
        self.emit("\n")
        self.rows = []

    # ---- final cleanup ----------------------------------------------------
    def result(self):
        md = "".join(self.out)
        # stray empty emphasis from adjacent bold/italic tags
        md = md.replace("****", "").replace("** **", " ")
        # collapse 3+ blank lines to 2
        md = re.sub(r"\n{3,}", "\n\n", md)
        # no trailing spaces
        md = "\n".join(line.rstrip() for line in md.split("\n"))
        return md.strip() + "\n"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    parser = MD()
    parser.feed(raw)
    parser.close()
    md = "# %(title)s\n\n> Converted from `%(src)s` with scripts/docx2md.py — best-effort; curate before treating as normative.\n\n" % {
        "title": "",
        "src": src,
    } + parser.result()
    # drop the empty leading heading if the document already starts with one
    if md.startswith("# \n\n#"):
        md = md[5:]
    with open(dst, "w", encoding="utf-8") as f:
        f.write(md)
    print("wrote %s (%d bytes)" % (dst, len(md)))


if __name__ == "__main__":
    main()
