"""Check edition completeness, canonical export, local site links and preserved files."""
from __future__ import annotations
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit, unquote
from zipfile import ZipFile
from docx import Document
from pypdf import PdfReader
from export_docx_to_markdown import export_docx

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for key in ("href","src"):
            if key in attrs:
                self.links.append(attrs[key])

def verify():
    meta=json.loads((ROOT/"edition.json").read_text())
    version=meta["version"]
    book=ROOT/"skills/the-support-machine/references/book.md"
    text=book.read_text()
    numbers=[int(n) for n in re.findall(r"^## (\d+)\.",text,re.M)]
    assert numbers==list(range(1,meta["chapters"]+1)),numbers
    assert len(re.findall(r"^## Appendix [A-E]:",text,re.M))==meta["appendices"]
    assert len(re.findall(r"^## Part [IVX]+:",text,re.M))==5
    assert not re.search(r"\?\?\?|<[-—]AI|AI-generated phrasing|AI number",text)
    source=ROOT/f"manuscript/The Support Machine - manuscript {version}.docx"
    with TemporaryDirectory() as temp:
        regenerated=Path(temp)/"book.md"
        export_docx(source,regenerated)
        assert regenerated.read_bytes()==book.read_bytes(),"canonical export is stale"
    manifest=json.loads((ROOT/f"release-notes/{version}-checksums.json").read_text())
    for rel,expected in manifest["files"].items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==expected,rel
    preserved=json.loads((ROOT/f'docs/editions/{meta["previous"]}/checksums.json').read_text())
    for rel,expected in preserved.items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==expected,"archive changed: "+rel
    assert (ROOT/f"docs/downloads/the-support-machine-{version}.docx").read_bytes()==source.read_bytes()
    assert (ROOT/f"docs/downloads/the-support-machine-{version}.md").read_bytes()==book.read_bytes()
    doc=Document(source)
    assert not doc.styles.element.xpath(".//w:pBdr"),"unexpected paragraph border"
    pdf=PdfReader(ROOT/f"docs/the-support-machine-{version}.pdf")
    combined="\n".join(page.extract_text() or "" for page in pdf.pages)
    for marker in ("AI NIMBYs","Build vs. Buy","When the Customer Is a Bot","Did the Action Actually Happen","When the Agent Gets It Wrong","The Work Is Never Done","Appendix E"):
        assert marker in combined,"missing PDF section: "+marker
    for i,page in enumerate(pdf.pages):
        assert len((page.extract_text() or "").strip())>30,f"empty PDF page {i+1}"
    pages={}
    for path in (ROOT/"docs").rglob("*.html"):
        parser=Page()
        parser.feed(path.read_text())
        pages[path.resolve()]=parser
        if "editions" not in path.parts:
            assert len(parser.ids)==len(set(parser.ids)),"duplicate HTML anchor: "+str(path)
    broken=[]
    for path,page in pages.items():
        for link in page.links:
            url=urlsplit(link)
            if url.scheme or url.netloc:
                continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target=target/"index.html"
            if not target.exists():
                broken.append((str(path.relative_to(ROOT)),link))
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                broken.append((str(path.relative_to(ROOT)),link))
    assert not broken,broken
    for skill in ("the-support-machine","support-ai-evals"):
        with ZipFile(ROOT/f"docs/downloads/{skill}.skill") as package:
            assert f"{skill}/SKILL.md" in package.namelist()
            assert not any("__pycache__" in name for name in package.namelist())
    print(f"Verified {meta['chapters']} chapters, {meta['appendices']} appendices, {len(pdf.pages)} PDF pages, {len(pages)} HTML pages, all local site links, canonical export, downloads, and v0.2 checksums.")
    return len(pdf.pages)

if __name__=="__main__":
    verify()
