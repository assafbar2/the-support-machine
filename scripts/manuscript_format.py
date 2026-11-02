"""Explicit Markdown subset shared by the book import and website."""
import re
import hashlib

TICK = chr(96)
INLINE = re.compile(r"(\[[^\]]+\]\([^)]+\)|\*\*[^*]+\*\*|" + TICK + "[^" + TICK + "]+" + TICK + r"|_[^_\n]+_)")

def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "section"

def bookmark(anchor):
    return "book_" + hashlib.sha256(anchor.encode()).hexdigest()[:24]

def spans(text):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("[") and re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", part):
            m = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", part)
            yield "link", m[1], m[2]
        elif part.startswith("**"):
            yield "bold", part[2:-2], None
        elif part.startswith(TICK):
            yield "code", part[1:-1], None
        elif part.startswith("_"):
            yield "italic", part[1:-1], None
        else:
            yield "text", part, None

def plain(text):
    return "".join(value for _, value, _ in spans(text))

def blocks(markdown):
    lines, i = markdown.splitlines(), 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        image=re.fullmatch(r'!\[((?:\\.|[^\]\\])*)\]\(([^)]+)\)',line)
        if image:
            yield 'image',re.sub(r'\\([\\\[\]])',r'\1',image[1]),image[2]
            i+=1
            continue
        if line.startswith(TICK*3):
            content = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith(TICK*3):
                content.append(lines[i])
                i += 1
            if i == len(lines):
                raise ValueError("unclosed code fence")
            yield "code", "\n".join(content), None
            i += 1
            continue
        heading = re.fullmatch(r"(#{1,4})\s+(.+)", line)
        if heading:
            yield "heading", heading[2], len(heading[1])
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", lines[i].strip().strip("|"))])
                i += 1
            if len(rows) < 2 or not all(re.fullmatch(r":?-+:?", c.replace(" ", "")) for c in rows[1]):
                raise ValueError("table needs a delimiter row")
            if any(len(r) != len(rows[0]) for r in rows):
                raise ValueError("table rows have inconsistent width")
            yield "table", [rows[0]] + rows[2:], None
            continue
        numbered = re.match(r"^(\d+)\.\s+(.+)$", line)
        if line.startswith("- "):
            yield "bullet", line[2:], None
            i += 1
            continue
        if numbered:
            yield "number", numbered[2], int(numbered[1])
            i += 1
            continue
        if line.startswith("> "):
            yield "quote", line[2:], None
            i += 1
            continue
        parts = [line]
        i += 1
        while i < len(lines) and lines[i].strip():
            following = lines[i].strip()
            if re.match(r"^(#{1,4} |[-|>] |\d+\. |\||!\[)", following) or following.startswith(TICK*3):
                break
            parts.append(following)
            i += 1
        yield "paragraph", " ".join(parts), None
