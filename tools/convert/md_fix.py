#!/usr/bin/env python3
"""md_fix.py - Post-process docx2md.py output.

Replaces the empty first heading with a real title, promotes known
standalone section lines to ## headings, optionally promotes
question lines (ending in "?") to ### headings, and optionally drops
one exact line (e.g. the original title paragraph now duplicated as H1).

Usage:
  python3 -I md_fix.py file.md --title "T" [--sections "A|B|C"] \
      [--questions] [--drop-line "old title line"]
"""
import sys


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    path = args[0]
    title = None
    sections = []
    questions = False
    drop = None
    i = 1
    while i < len(args):
        if args[i] == "--title":
            title = args[i + 1]
            i += 2
        elif args[i] == "--sections":
            sections = [s.strip() for s in args[i + 1].split("|")]
            i += 2
        elif args[i] == "--questions":
            questions = True
            i += 1
        elif args[i] == "--drop-line":
            drop = args[i + 1]
            i += 2
        else:
            print("unknown arg: %s" % args[i])
            sys.exit(2)

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().split("\n")

    out = []
    n_secs = n_q = 0
    for idx, line in enumerate(lines):
        if idx == 0 and line == "# " and title:
            out.append("# " + title)
            continue
        if drop and line.strip() == drop:
            n_secs += 0  # counted separately
            out.append("")
            continue
        nxt = ""
        for j in range(idx + 1, len(lines)):
            if lines[j].strip():
                nxt = lines[j].strip()
                break
        prev = lines[idx - 1].strip() if idx else ""
        stripped = line.strip()
        is_section = (
            stripped in sections
            and prev == ""
            and (nxt == "" or nxt.startswith("|") or nxt[0].isupper() or nxt.startswith("**"))
        )
        is_question = (
            questions
            and stripped.endswith("?")
            and not stripped.startswith(("#", "-", "|", ">"))
            and prev == ""
            and (nxt.startswith("**Specified") or nxt.startswith("**Partly specified") or nxt.startswith("**Not specified"))
        )
        if is_section:
            out.append("## " + stripped)
            n_secs += 1
        elif is_question:
            out.append("### " + stripped)
            n_q += 1
        else:
            out.append(line)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("%s: title=%s sections=%d questions=%d" % (path, bool(title), n_secs, n_q))


if __name__ == "__main__":
    main()
