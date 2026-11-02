"""Export the canonical DOCX, preserving inline links, emphasis and lists."""
import sys
import re
from pathlib import Path
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run
from manuscript_format import slugify, TICK

def embedded_images(run, directory, used_names):
    """Export embedded drawing bytes and their authored alternative text."""
    results=[]
    for drawing in run._r.xpath('.//wp:inline'):
        props=drawing.find(qn('wp:docPr'))
        blips=drawing.xpath('.//a:blip')
        if len(blips)!=1 or not blips[0].get(qn('r:embed')):
            raise ValueError('A book illustration must contain one embedded image')
        part=run.part.related_parts[blips[0].get(qn('r:embed'))]
        stem=re.sub(r'[^a-zA-Z0-9_-]+','-',Path(props.get('name','illustration')).stem).strip('-') or 'illustration'
        filename=stem+Path(str(part.partname)).suffix
        if filename in used_names and used_names[filename]!=part.blob:
            raise ValueError('Different illustrations use the same name: '+filename)
        used_names[filename]=part.blob
        directory.mkdir(parents=True,exist_ok=True)
        (directory/filename).write_bytes(part.blob)
        alt=props.get('descr') or props.get('title') or stem.replace('-',' ')
        alt=' '.join(alt.split()).replace('\\','\\\\').replace('[',r'\[').replace(']',r'\]')
        results.append(f'![{alt}](illustrations/{filename})')
    return results

def paragraph_markdown(p,anchors,image_directory=None,used_names=None):
    parts = []
    for element in p._p:
        if element.tag == qn("w:r"):
            run = Run(element,p)
            if image_directory is not None:
                parts.extend(embedded_images(run,image_directory,used_names))
            value = run.text
            if not value:
                continue
            if run.font.name == "Consolas" and p.style.name != "Code":
                value = TICK+value+TICK
            elif run.bold:
                value = "**"+value+"**"
            elif run.italic:
                value = "_"+value+"_"
            parts.append(value)
        elif element.tag == qn("w:hyperlink"):
            value = "".join(t.text or "" for t in element.iter(qn("w:t")))
            rel, anchor = element.get(qn("r:id")), element.get(qn("w:anchor"))
            if rel:
                target = p.part.rels[rel].target_ref
            elif anchor:
                if anchor not in anchors:
                    raise ValueError("Unresolved internal bookmark: "+anchor)
                target = "#"+anchors[anchor]
            else:
                target = ""
            parts.append(f"[{value}]({target})" if target else value)
    return "".join(parts).replace("\xa0"," ").strip()

def numbering_starts(doc):
    root = doc.part.numbering_part.element
    abstract, starts = {}, {}
    for node in root.findall(qn("w:abstractNum")):
        level = node.find(qn("w:lvl"))
        start = level.find(qn("w:start")) if level is not None else None
        abstract[node.get(qn("w:abstractNumId"))] = int(start.get(qn("w:val"))) if start is not None else 1
    for node in root.findall(qn("w:num")):
        ref = node.find(qn("w:abstractNumId"))
        starts[node.get(qn("w:numId"))] = abstract.get(ref.get(qn("w:val")),1)
    return starts

def export_docx(src,dst):
    doc = Document(src)
    anchors, seen = {}, {}
    for p in doc.paragraphs:
        if p.style.name == "Title" or p.style.name.startswith("Heading"):
            anchor = slugify(p.text)
            seen[anchor] = seen.get(anchor,0)+1
            if seen[anchor] > 1:
                anchor += "-"+str(seen[anchor])
            for start in p._p.findall(qn("w:bookmarkStart")):
                anchors[start.get(qn("w:name"))] = anchor
    lines, counts, starts = [], {}, numbering_starts(doc)
    image_directory, used_names=dst.parent/'illustrations',{}
    for child in doc.element.body:
        if child.tag == qn("w:p"):
            p = Paragraph(child,doc)
            text = paragraph_markdown(p,anchors,image_directory,used_names)
            if not text:
                continue
            style = p.style.name
            if style == "Title":
                lines += ["# "+text,"",f"> Markdown export of the manuscript. The canonical formatted source is maintained in {TICK}manuscript/{TICK}.",""]
            elif style.startswith("Heading "):
                lines += ["#"*(int(style.split()[-1])+1)+" "+text,""]
            elif style == "List Bullet":
                lines += ["- "+text,""]
            elif style == "List Number":
                num = p._p.find("./"+qn("w:pPr")+"/"+qn("w:numPr")+"/"+qn("w:numId"))
                nid = num.get(qn("w:val")) if num is not None else "default"
                number = counts.get(nid,starts.get(nid,1))
                counts[nid] = number+1
                lines += [f"{number}. {text}",""]
            elif style == "Quote":
                lines += ["> "+text,""]
            elif style == "Code":
                lines += [TICK*3,text,TICK*3,""]
            else:
                lines += [text,""]
        elif child.tag == qn("w:tbl"):
            rows = []
            for row in Table(child,doc).rows:
                rows.append([" ".join(paragraph_markdown(p,anchors,image_directory,used_names) for p in c.paragraphs).replace("|",r"\|") for c in row.cells])
            lines += ["| "+" | ".join(rows[0])+" |","| "+" | ".join(["---"]*len(rows[0]))+" |"]
            lines += ["| "+" | ".join(row)+" |" for row in rows[1:]]
            lines += [""]
    if not any(line.startswith("# ") for line in lines):
        lines = ["# The Support Machine",""]+lines
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_text("\n".join(lines).rstrip()+"\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: export_docx_to_markdown.py input.docx output.md")
    export_docx(Path(sys.argv[1]),Path(sys.argv[2]))
