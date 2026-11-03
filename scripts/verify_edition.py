"""Check edition completeness, canonical export, local site links and preserved files."""
from __future__ import annotations
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
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
    assert not re.search(r'\bhorror\b|unstructured thoughts for LLM|Date the next note|Do not put the result of a future demo into the book|\[\[ASSAF',visible,re.I),"reader-facing editorial residue"
    assert not re.search(r'\b(?:Rene|Jordyn|Simon|Kegan|Lahey|Edmondson)\b',visible),"named narrative participant"
    assert len(re.findall(r'^\*\*\d{2}\. ',text,re.M))==10,"prompt appendix should print ten starter prompts"
    prompts=(ROOT/'skills/the-support-machine/references/prompts.md').read_text()
    assert len(re.findall(r'^\*\*\d{2}\. ',prompts,re.M))==80,"prompt library is incomplete"
    def prompt_items(source):
        return {number:(title,body.strip()) for number,title,body in
                re.findall(r'^\*\*(\d{2})\. ([^\n]+)\*\*\n\n(.*?)(?=^\*\*\d{2}\. |^### |^## |\Z)',source,re.M|re.S)}
    library = prompt_items(prompts)
    starters = prompt_items(text)
    assert set(library)=={f'{number:02}' for number in range(1,81)},"prompt numbers must be unique and complete"
    assert set(starters)=={'01','09','12','17','26','36','41','48','52','66'},"wrong starter prompts"
    assert all(library[number]==prompt for number,prompt in starters.items()),"printed prompt differs from the full library"
    chapters=re.findall(r'^## (\d+)\. ([^\n]+)\n(.*?)(?=^## |\Z)',text,re.M|re.S)
    chapter_notes=[]
    for number,title,body in chapters:
        notes=re.findall(r'^_Field note: (.+)_$',body,re.M)
        assert len(notes)==1,(number,notes)
        chapter_notes.append((number,notes[0]))
    index=text.split('## Appendix E: Dated Observations\n',1)[1].split('### Dated observations',1)[0]
    assert len(re.findall(r'^- \[Chapter \d+ — ',index,re.M))==meta['chapters'],"field-note index incomplete"
    assert [int(n) for n in re.findall(r'^- \[Chapter (\d+) — ',index,re.M)]==numbers,"field-note index has duplicate or missing chapters"
    assert len({note for _,note in chapter_notes})==len(chapter_notes),"duplicate field notes"
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
    for prior_path in (ROOT/'release-notes').glob('v*-checksums.json'):
        prior=json.loads(prior_path.read_text())
        if prior['version']==version:
            continue
        # Stable edition aliases intentionally change; versioned printings do not.
        immutable={rel:expected for rel,expected in prior['files'].items()
                   if re.search(re.escape(prior['version'])+r'(?=[.-])',Path(rel).name)}
        assert immutable,'prior printing manifest has no versioned files: '+str(prior_path)
        for rel,expected in immutable.items():
            assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==expected,'prior printing changed: '+rel
    assert (ROOT/f"docs/downloads/the-support-machine-{version}.docx").read_bytes()==source.read_bytes()
    assert (ROOT/f"docs/downloads/the-support-machine-{version}.md").read_bytes()==book.read_bytes()
    assert meta['name']=='Second Edition' and meta['status']=='published'
    assert 'Second Edition' in text and 'Notes for the Second Edition' in text
    assert not re.search(r'v0\.\d+|review edition|codex/support-machine',text,re.I), 'unpublished naming in book'
    for suffix in ('pdf','docx','md','markdown.zip'):
        folder=ROOT/'docs' if suffix=='pdf' else ROOT/'docs/downloads'
        joiner='-' if suffix=='markdown.zip' else '.'
        assert (folder/f"the-support-machine-{meta['slug']}{joiner}{suffix}").read_bytes()==(folder/f"the-support-machine-{version}{joiner}{suffix}").read_bytes(), 'stale edition alias: '+suffix
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
        assert bundle.read('LICENSE-MANUSCRIPT.md')==(ROOT/'licenses/MANUSCRIPT-CC-BY-4.0.md').read_bytes(),'Markdown package book license differs'
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
    cover=' '.join((pdf.pages[0].extract_text() or '').split())
    assert doc.core_properties.subject in cover,'PDF subtitle differs from the canonical manuscript'
    normalized=' '.join(combined.split())
    for marker in ('Burn the Ships. Keep a Lifeboat.','What I got wrong in the first edition'):
        assert marker in normalized,'PDF is missing revised-printing content: '+marker
    for marker in ("AI NIMBYs","Build vs. Buy","When the Customer Is a Bot","Did the Action Actually Happen","When the Agent Gets It Wrong","The Work Is Never Done","Appendix E","Repositories Behind the Book","Talk to the Book","Sources and Further Reading"):
        assert marker in combined,"missing PDF section: "+marker
    assert 'Second Edition' in (pdf.pages[0].extract_text() or ''), 'PDF cover edition label'
    assert not re.search(r'v0\.\d+|Review edition|Markdown export of the manuscript|\[\[ASSAF',combined,re.I), 'authoring residue or repository version exposed in PDF'
    assert 'SECOND EDITION' in (pdf.pages[1].extract_text() or ''), 'PDF running header edition label'
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
            if not target.is_relative_to((ROOT/'docs').resolve()) or not target.exists():
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
            overview = 'LICENSE.md' if skill == 'the-support-machine' else 'LICENSING.md'
            license_text = package.read(f'{skill}/{overview}').decode()
            for link in re.findall(r'\]\(([^)]+)\)', license_text):
                url = urlsplit(link)
                if not url.scheme and not url.netloc:
                    member = posixpath.normpath(f'{skill}/{url.path}')
                    assert member in package.namelist(),'broken packaged licensing link: '+member
            assert package.read(f'{skill}/LICENSE-MANUSCRIPT.md')==(ROOT/'licenses/MANUSCRIPT-CC-BY-4.0.md').read_bytes(),"book license missing from package"
            code_license = 'LICENSE-SKILL.md' if skill == 'the-support-machine' else 'LICENSE.md'
            assert package.read(f'{skill}/{code_license}')==(ROOT/'LICENSE').read_bytes(),"code license changed in package"
    for page_name in ('index.html','book.html','notes.html','skill.html','illustrations/index.html'):
        page_text=(ROOT/'docs'/page_name).read_text()
        # Legacy filenames are allowed as technical URLs, never as current-edition prose.
        visible_text=re.sub(r'<[^>]+>',' ',page_text)
        assert not re.search(r'v0\.\d+|review edition',visible_text,re.I), 'public edition label: '+page_name
        assert 'Second Edition' in page_text, 'missing edition label: '+page_name
    print(f"Verified {meta['chapters']} chapters, {meta['appendices']} appendices, {expected} captioned illustrations, {len(pdf.pages)} PDF pages, {len(pages)} HTML pages, all local site links, canonical export, downloads, and preserved editions/printings.")
    return len(pdf.pages)

if __name__=="__main__":
    verify()
