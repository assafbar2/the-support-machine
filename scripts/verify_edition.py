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
    appendix_letters=re.findall(r"^## Appendix ([A-Z]):",text,re.M)
    assert appendix_letters==[chr(ord('A')+i) for i in range(meta['appendices'])],appendix_letters
    assert len(re.findall(r"^## Part [IVX]+:",text,re.M))==5
    assert not re.search(r"\?\?\?|<[-—]AI|AI-generated phrasing|AI number",text)
    visible=re.sub(r'\]\([^)]+\)',']',text)
    assert not re.search(r'\bhorror\b|unstructured thoughts for LLM|Date the next note|Do not put the result of a future demo into the book',visible,re.I),"reader-facing editorial residue"
    assert not re.search(r'\b(?:Rene|Jordyn|Simon|Kegan|Lahey|Edmondson|Kurzweil|Turing)\b|Hernán|Cortés',visible),"named narrative participant"
    assert len(re.findall(r'^\*\*\d{2}\. ',text,re.M))==80,"prompt appendix is incomplete"
    chapters=re.findall(r'^## (\d+)\. ([^\n]+)\n(.*?)(?=^## |\Z)',text,re.M|re.S)
    chapter_notes=[]
    for number,title,body in chapters:
        notes=re.findall(r'^_Field note: (.+)_$',body,re.M)
        assert len(notes)==1,(number,notes)
        chapter_notes.append((number,notes[0]))
    collected=text.split('## Appendix E: All Field Notes\n',1)[1].split('### Dated observations',1)[0]
    assert len(re.findall(r'^\*\*Chapter \d+ —',collected,re.M))==meta['chapters']
    for number,note in chapter_notes:
        assert note in collected,'missing collected field note '+number
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
    assert (ROOT/f"review/the-support-machine-{version}-reading-copy.docx").read_bytes()==source.read_bytes(),"reading copy differs from canonical manuscript"
    assert (ROOT/f"docs/downloads/the-support-machine-{version}.md").read_bytes()==book.read_bytes()
    doc=Document(source)
    assert not doc.styles.element.xpath(".//w:pBdr"),"unexpected paragraph border"
    figures=json.loads((ROOT/'docs/illustrations/manifest.json').read_text())['figures']
    expected=meta['illustrations']
    assert len(figures)==len(doc.inline_shapes)==expected,'illustration count differs'
    captions=[p.text for p in doc.paragraphs if p.style.name=='Book Figure Caption']
    assert len(captions)==expected,'illustration captions missing'
    for label,count in [('Gate',6),('Figure',4)]:
        numbers=[int(m[1]) for c in captions if (m:=re.match(label+r' (\d+) — ',c))]
        assert numbers==list(range(1,count+1)),label+' captions are out of reading order'
    assert len(re.findall(r'^!\[',text,re.M))==expected,'Markdown illustrations missing'
    shapes={s._inline.docPr.get('name'):s for s in doc.inline_shapes}
    for figure in figures:
        slug=figure['slug']
        shape=shapes[slug]
        assert shape._inline.docPr.get('descr')==figure['caption'],'missing or stale image alternative text'
        embed=shape._inline.xpath('.//a:blip')[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
        data=doc.part.related_parts[embed].blob
        for directory in (ROOT/'docs/illustrations/book',ROOT/'docs/downloads/illustrations',book.parent/'illustrations'):
            assert (directory/f'{slug}.png').read_bytes()==data,'stale illustration: '+str(directory/slug)
    with ZipFile(ROOT/f'docs/downloads/the-support-machine-{version}-markdown.zip') as bundle:
        assert bundle.read('book.md')==book.read_bytes()
        for figure in figures:
            filename=figure['slug']+'.png'
            assert bundle.read('illustrations/'+filename)==(book.parent/'illustrations'/filename).read_bytes()
    pdf=PdfReader(ROOT/f"docs/the-support-machine-{version}.pdf")
    # LibreOffice shares image resources across pages; count actual paint operations.
    drawn_images=0
    for page in pdf.pages:
        resources=page['/Resources'].get_object().get('/XObject',{})
        if hasattr(resources,'get_object'):
            resources=resources.get_object()
        for operands,operation in page.get_contents().operations:
            if operation==b'Do' and resources[operands[0]].get_object().get('/Subtype')=='/Image':
                drawn_images+=1
    assert drawn_images==expected,'rendered PDF illustrations missing'
    combined="\n".join(page.extract_text() or "" for page in pdf.pages)
    for marker in ("AI NIMBYs","Build vs. Buy","When the Customer Is a Bot","Did the Action Actually Happen","When the Agent Gets It Wrong","The Work Is Never Done","Appendix E","Repositories Behind the Book","Talk to the Book","Sources and Further Reading"):
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
        archive = ROOT/f"docs/downloads/{skill}.skill"
        assert (ROOT/f"docs/downloads/{skill}.zip").read_bytes()==archive.read_bytes(),"ZIP alias differs: "+skill
        with ZipFile(archive) as package:
            assert f"{skill}/SKILL.md" in package.namelist()
            assert not any("__pycache__" in name for name in package.namelist())
            for path in (ROOT/"skills"/skill).rglob("*"):
                if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                    member = str(path.relative_to(ROOT/"skills"))
                    assert package.read(member)==path.read_bytes(),"stale skill resource: "+member
            if skill == "the-support-machine":
                assert package.read(f"{skill}/references/book.md")==book.read_bytes(),"packaged book is stale"
    print(f"Verified {meta['chapters']} chapters, {meta['appendices']} appendices, {expected} captioned illustrations, {len(pdf.pages)} PDF pages, {len(pages)} HTML pages, all local site links, canonical export, downloads, and v0.2 checksums.")
    return len(pdf.pages)

if __name__=="__main__":
    verify()
