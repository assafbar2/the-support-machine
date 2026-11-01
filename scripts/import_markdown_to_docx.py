"""Import a complete Markdown revision into the canonical formatted manuscript."""
import argparse
import re
from pathlib import Path
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from manuscript_format import blocks, spans, slugify, bookmark, plain

def xml(tag, **attrs):
    node = OxmlElement(tag)
    for key, value in attrs.items():
        node.set(qn("w:" + key), str(value))
    return node

def add_inline(paragraph, text):
    for kind, value, target in spans(text):
        if kind == "link":
            link = xml("w:hyperlink")
            if target.startswith("#"):
                link.set(qn("w:anchor"), bookmark(target[1:]))
            else:
                link.set(qn("r:id"), paragraph.part.relate_to(target, RT.HYPERLINK, is_external=True))
            run, props = xml("w:r"), xml("w:rPr")
            props.append(xml("w:rStyle", val="Hyperlink"))
            run.append(props)
            t = xml("w:t")
            t.text = value
            run.append(t)
            link.append(run)
            paragraph._p.append(link)
        else:
            run = paragraph.add_run(value)
            if kind == "bold":
                run.bold = True
            elif kind == "italic":
                run.italic = True
            elif kind == "code":
                run.font.name, run.font.size = "Consolas", Pt(10)

def set_numbering(doc, paragraph, number, num_id=None):
    numbering = doc.part.numbering_part.element
    if num_id is None:
        aid = max([int(x.get(qn("w:abstractNumId"))) for x in numbering.findall(qn("w:abstractNum"))], default=-1) + 1
        abstract, level = xml("w:abstractNum", abstractNumId=aid), xml("w:lvl", ilvl=0)
        for item in [xml("w:start", val=number), xml("w:numFmt", val="decimal"), xml("w:lvlText", val="%1."), xml("w:lvlJc", val="left")]:
            level.append(item)
        props = xml("w:pPr")
        props.append(xml("w:ind", left=360, hanging=240))
        level.append(props)
        abstract.append(level)
        numbering.append(abstract)
        num_id = max([int(x.get(qn("w:numId"))) for x in numbering.findall(qn("w:num"))], default=0) + 1
        num = xml("w:num", numId=num_id)
        num.append(xml("w:abstractNumId", val=aid))
        numbering.append(num)
    numpr = xml("w:numPr")
    numpr.append(xml("w:ilvl", val=0))
    numpr.append(xml("w:numId", val=num_id))
    paragraph._p.get_or_add_pPr().append(numpr)
    return num_id

def format_document(doc):
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin = section.bottom_margin = Inches(.78)
    section.left_margin = section.right_margin = Inches(.85)
    section.header_distance = section.footer_distance = Inches(.35)
    section.different_first_page_header_footer = True
    styles = doc.styles
    for name in ("Normal", "Body Text"):
        styles[name].font.name, styles[name].font.size = "Georgia", Pt(11)
        styles[name].font.color.rgb = RGBColor(0,0,0)
        styles[name].paragraph_format.line_spacing = 1.1
        styles[name].paragraph_format.space_after = Pt(6)
        styles[name].paragraph_format.widow_control = True
    for name, size in [("Title",36),("Subtitle",18),("Heading 1",22),("Heading 2",14),("Heading 3",12)]:
        style = styles[name]
        style.font.name, style.font.size = "Calibri", Pt(size)
        style.font.color.rgb = RGBColor(0,0,0)
        style.paragraph_format.keep_with_next = True
        style.paragraph_format.space_before, style.paragraph_format.space_after = Pt(15), Pt(9)
    styles["Title"].paragraph_format.space_before = Pt(105)
    for border in list(styles.element.xpath(".//w:pBdr")):
        border.getparent().remove(border)
    for name in ("List Bullet","List Number","Quote"):
        styles[name].font.name, styles[name].font.size = "Georgia", Pt(11)
        styles[name].font.color.rgb = RGBColor(0,0,0)
        styles[name].paragraph_format.space_after = Pt(6)
        styles[name].paragraph_format.line_spacing = 1.13
    styles['Quote'].font.italic = False
    for name in ("Cell Body","Code"):
        if name not in styles:
            styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    styles["Cell Body"].base_style = styles["Normal"]
    styles["Cell Body"].font.size = Pt(9.5)
    styles["Cell Body"].paragraph_format.space_after = Pt(3)
    styles["Cell Body"].paragraph_format.space_before = Pt(3)
    styles["Cell Body"].paragraph_format.line_spacing = 1.05
    styles["Code"].font.name, styles["Code"].font.size = "Consolas", Pt(9)
    if "Hyperlink" not in styles:
        styles.add_style("Hyperlink", WD_STYLE_TYPE.CHARACTER)
    styles["Hyperlink"].font.color.rgb = RGBColor.from_string("772817")
    styles["Hyperlink"].font.underline = True
    header = section.header.paragraphs[0]
    run = header.add_run("THE SUPPORT MACHINE  ·  v0.3")
    run.font.name, run.font.size = "Calibri", Pt(8)
    run.font.color.rgb = RGBColor(0,0,0)
    footer = section.footer.paragraphs[0]
    footer.alignment = 2
    field = xml("w:fldSimple", instr="PAGE")
    field.append(xml("w:r"))
    footer._p.append(field)

def add_table(doc, rows):
    width = len(rows[0])
    table = doc.add_table(rows=1, cols=width)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fractions = {2:[.30,.70],3:[.24,.38,.38],4:[.20,.29,.25,.26]}.get(width,[1/width]*width)
    for col, fraction in zip(table.columns, fractions):
        col.width = Inches(6.8*fraction)
    borders = xml("w:tblBorders")
    for edge in ("top","left","bottom","right","insideH","insideV"):
        borders.append(xml("w:"+edge,val="single",sz=4,color="D9D9D9"))
    table._tbl.tblPr.append(borders)
    for index, values in enumerate(rows):
        row = table.rows[0] if index == 0 else table.add_row()
        trpr = row._tr.get_or_add_trPr()
        trpr.append(xml("w:cantSplit"))
        if index == 0:
            trpr.append(xml("w:tblHeader"))
        for cell, value, fraction in zip(row.cells,values,fractions):
            cell.width = Inches(6.8*fraction)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            p = cell.paragraphs[0]
            p.style = "Cell Body"
            add_inline(p,value)
            if index == 0:
                cell._tc.get_or_add_tcPr().append(xml("w:shd",fill="F2F2F2"))
                for run in p.runs:
                    run.bold = True
                    run.font.color.rgb = RGBColor(0,0,0)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(2)
    spacer.paragraph_format.line_spacing = Pt(2)
    spacer.add_run().font.size = Pt(2)

def create(source, destination):
    doc = Document()
    format_document(doc)
    doc.core_properties.title = "The Support Machine"
    doc.core_properties.author = "Assaf Barnir"
    doc.core_properties.subject = "How to Deploy AI in Customer Support Without Breaking Trust"
    doc.core_properties.keywords = "v0.3, support, AI, evaluation, operating model"
    doc.core_properties.comments = ""
    seen, cover, count, in_contents = {}, True, 0, False
    list_id, expected_number = None, None
    for kind, content, extra in blocks(source.read_text()):
        if kind != "number":
            list_id, expected_number = None, None
        if kind == "heading":
            level = extra
            if level == 2:
                in_contents = content == "Contents"
            p = doc.add_paragraph(style="Title" if level == 1 else "Heading "+str(level-1))
            add_inline(p,content)
            anchor = slugify(plain(content))
            seen[anchor] = seen.get(anchor,0)+1
            if seen[anchor] > 1:
                anchor += "-"+str(seen[anchor])
            count += 1
            p._p.insert(1,xml("w:bookmarkStart",id=count,name=bookmark(anchor)))
            p._p.append(xml("w:bookmarkEnd",id=count))
            if level == 2:
                if cover or content in {"Reader's Note", "The Operating Map"} or re.match(r"^(Part [IVX]+:|[0-9]+\.|Appendix |Contents$|Introduction:)",content):
                    p.paragraph_format.page_break_before = True
                cover = False
        elif kind == "table":
            add_table(doc,content)
        else:
            style = {"bullet":"List Bullet","number":"List Number","quote":"Quote","code":"Code"}.get(kind,"Normal")
            if cover and kind == "paragraph":
                style = "Subtitle" if content.startswith("How to Deploy") else "Normal"
            p = doc.add_paragraph(style=style)
            add_inline(p,content)
            if kind == 'paragraph' and re.fullmatch(r'\*\*[^*]+\*\*',content):
                p.paragraph_format.keep_with_next = True
            if kind == 'quote':
                p.paragraph_format.keep_together = True
            if in_contents:
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.space_after = Pt(2)
                if kind == "paragraph":
                    p.paragraph_format.space_before = Pt(6)
                    p.paragraph_format.keep_with_next = True
                # Hyperlink text inherits the paragraph style; set its runs too.
                for element in p._p.xpath(".//w:r"):
                    props = element.find(qn("w:rPr"))
                    if props is None:
                        props = xml("w:rPr")
                        element.insert(0,props)
                    props.append(xml("w:sz",val=21))
            if plain(content).startswith("Field note:"):
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.keep_together = True
                if len(doc.paragraphs) > 1:
                    doc.paragraphs[-2].paragraph_format.keep_with_next = True
                for run in p.runs:
                    run.italic = True
                    run.font.size = Pt(10.5)
            if kind == "number":
                if extra != expected_number:
                    list_id = None
                list_id = set_numbering(doc,p,extra,list_id)
                expected_number = extra+1
    if doc.paragraphs:
        doc.paragraphs[-1].paragraph_format.keep_together = True
    # These short chapters otherwise leave only their closing lines on a new
    # page. Tighten paragraph spacing without shrinking the body type.
    active_chapter = None
    active_section = None
    for paragraph in doc.paragraphs:
        if paragraph.style.name == 'Heading 1':
            active_section = paragraph.text
            match = re.match(r'^(\d+)\.', paragraph.text)
            active_chapter = int(match.group(1)) if match else None
        if active_chapter in {19,20,23,25}:
            compact = active_chapter in {20,23}
            if paragraph.style.name in {'Normal','List Number'}:
                paragraph.paragraph_format.space_after = Pt(2 if compact else 4)
                paragraph.paragraph_format.line_spacing = 1.03 if compact else 1.05
            elif paragraph.style.name == 'Heading 2':
                paragraph.paragraph_format.space_before = Pt(10 if compact else 12)
                paragraph.paragraph_format.space_after = Pt(6 if compact else 7)
            elif paragraph.style.name == 'Heading 1' and compact:
                paragraph.paragraph_format.space_before = Pt(10)
                paragraph.paragraph_format.space_after = Pt(7)
        if active_section in {'Notes for the New Version: v0.3', 'Appendix H: Sources and Further Reading'}:
            if paragraph.style.name in {'Normal', 'List Bullet'}:
                paragraph.paragraph_format.space_after = Pt(4)
                paragraph.paragraph_format.line_spacing = 1.05
            elif paragraph.style.name == 'Heading 2':
                paragraph.paragraph_format.space_before = Pt(12)
                paragraph.paragraph_format.space_after = Pt(6)
    destination.parent.mkdir(parents=True,exist_ok=True)
    doc.save(destination)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source",type=Path)
    parser.add_argument("destination",type=Path)
    args = parser.parse_args()
    create(args.source,args.destination)
