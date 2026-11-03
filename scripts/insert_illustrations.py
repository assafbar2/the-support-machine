"""Insert or refresh the ten book illustrations without rewriting the manuscript."""
import json
from pathlib import Path
import re
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Inches,Pt,RGBColor
from docx.text.paragraph import Paragraph

ROOT=Path(__file__).resolve().parents[1]
PLACEMENTS={
    1:(1,'We had a friction problem.'),
    2:(8,'The question is which layer benefits from being specific to your business'),
    3:(13,'Five roles. Not five models.'),
    4:(22,'The original human answer is also something to examine.'),
    5:(24,'The launch runbook and pre-mortem brought the preparation together.'),
    6:(29,'Each finding needs an owner, an action, a way to verify the repair'),
    7:(18,'That calculation works only if the populations'),
    8:(28,"The agent's report tells us what it classified as resolved."),
    9:(16,'The human handoff should include the original intent,'),
    10:(6,'Prevention does not eliminate the need for skilled human recovery.'),
}


def after(anchor,style):
    node=OxmlElement('w:p')
    anchor._p.addnext(node)
    p=Paragraph(node,anchor._parent)
    p.style=style
    return p


def insert():
    meta=json.loads((ROOT/'edition.json').read_text())
    source=ROOT/f'manuscript/The Support Machine - manuscript {meta["version"]}.docx'
    figures=json.loads((ROOT/'docs/illustrations/manifest.json').read_text())['figures']
    assert len(figures)==10
    # Gate numbers follow the operating map. Supplemental figures follow reading order.
    supplemental=sorted((f for f in figures if not f['gate']),key=lambda f:PLACEMENTS[f['number']][0])
    figure_numbers={f['number']:i for i,f in enumerate(supplemental,1)}
    doc=Document(source)
    for p in list(doc.paragraphs):
        if p.style.name in {'Book Figure','Book Figure Caption'}:
            p._p.getparent().remove(p._p)
    original=[p.text for p in doc.paragraphs]
    tables=[t._tbl.xml for t in doc.tables]
    for name in ['Book Figure','Book Figure Caption']:
        if name not in doc.styles:
            doc.styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
        style=doc.styles[name]
        style.base_style=doc.styles['Normal']
        style.font.name='Arial'
        style.font.color.rgb=RGBColor(0,0,0)
    image_style=doc.styles['Book Figure']
    image_style.font.size=Pt(1)
    image_style.paragraph_format.line_spacing=1
    image_style.paragraph_format.space_before=Pt(10)
    image_style.paragraph_format.space_after=Pt(3)
    image_style.paragraph_format.keep_with_next=True
    image_style.paragraph_format.keep_together=True
    caption_style=doc.styles['Book Figure Caption']
    caption_style.font.size=Pt(10)
    caption_style.paragraph_format.line_spacing=1.1
    caption_style.paragraph_format.space_after=Pt(10)
    caption_style.paragraph_format.keep_together=True
    caption_style.paragraph_format.keep_with_next=False
    for figure in figures:
        chapter,fragment=PLACEMENTS[figure['number']]
        current=None
        matches=[]
        for p in doc.paragraphs:
            if p.style.name=='Heading 1':
                m=re.match(r'^(\d+)\. ',p.text)
                current=int(m[1]) if m else None
            if current==chapter and p.text.startswith(fragment): matches.append(p)
        assert len(matches)==1,(figure['number'],matches)
        p=after(matches[0],'Book Figure')
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        image=ROOT/'docs/illustrations/book'/f'{figure["slug"]}.png'
        shape=p.add_run().add_picture(str(image),width=Inches(6.8))
        shape._inline.docPr.set('name',figure['slug'])
        shape._inline.docPr.set('title',figure['title'])
        shape._inline.docPr.set('descr',figure['caption'])
        caption=after(p,'Book Figure Caption')
        number=figure['number'] if figure['gate'] else figure_numbers[figure['number']]
        label=('Gate' if figure['gate'] else 'Figure')+f' {number} — {figure["title"]}. '
        caption.add_run(label).bold=True
        extra='The numbers are illustrative, not company results. ' if figure['number']==7 else ''
        caption.add_run(extra+figure['takeaway'])
    # Small paragraph-spacing adjustments keep the closing notes with these chapters.
    # Preserve font sizes and full-width artwork for print readability.
    chapter=None
    for p in doc.paragraphs:
        if p.style.name=='Heading 1':
            m=re.match(r'^(\d+)\. ',p.text)
            chapter=int(m[1]) if m else None
        if p.style.name=='Normal' and chapter in (13,28):
            p.paragraph_format.space_after=Pt(2 if chapter==13 else 4)
    assert [p.text for p in doc.paragraphs if p.style.name not in {'Book Figure','Book Figure Caption'}]==original
    assert [t._tbl.xml for t in doc.tables]==tables
    assert len(doc.inline_shapes)==10
    doc.save(source)
    print('Refreshed 10 captioned illustrations; all existing manuscript paragraphs and tables preserved.')


if __name__=='__main__':
    insert()
