"""Build the complete chapter-marked reading copy from the canonical DOCX."""
from pathlib import Path
import re
from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt

def build():
    root = Path(__file__).resolve().parents[1]
    source = root / 'manuscript/The Support Machine - manuscript v0.3.docx'
    destination = root / 'review/the-support-machine-v0.3-reading-copy.docx'
    text = (root / 'skills/the-support-machine/references/book.md').read_text()
    titles = {int(n): title for n, title in re.findall(r'^## (\d+)\. (.+)$', text, re.M)}
    new = {5, 8, 15, 16, 27, 28}
    light = {1, 2, 3, 11, 12, 25}
    updated = set(titles) - new - light
    assert len(new) == 6 and len(light) == 6 and len(updated) == 17
    status = {n: 'NEW' if n in new else 'LIGHT EDITS' if n in light else 'UPDATED' for n in titles}
    replacements = {f'{n}. {title}': f'{status[n]} | {n}. {title}' for n, title in titles.items()}
    appendices = re.findall(r'^## (Appendix ([A-Z]): .+)$', text, re.M)
    for title, letter in appendices:
        replacements[title] = ('NEW' if letter in 'EFGH' else 'UPDATED') + ' | ' + title

    doc = Document(source)
    unmodified_body = doc.element.xml
    occurrences = {title: 0 for title in replacements}
    for node in doc.element.xpath('.//w:t'):
        if node.text in replacements:
            old = node.text
            node.text = replacements[old]
            occurrences[old] += 1
    assert all(count == 2 for count in occurrences.values()), occurrences

    version = [p for p in doc.paragraphs if p.text == 'v0.3 · November 1, 2026 · Review edition']
    assert len(version) == 1
    cover = version[0]
    cover.add_run('\nReading copy for Google Docs')
    cover.add_run('\nNEW marks added chapters. UPDATED marks substantive revisions. LIGHT EDITS marks limited wording and example refinements that can be skipped on a first reread.')
    cover.add_run('\nThe contents and chapter headings carry these labels. All chapter text is included, with the current wording ready to read.')

    guide = ['# The Support Machine v0.3 Reading Guide', '',
             'Use these chapter names in the Google Docs outline. Numbers refer to v0.3. NEW marks an added chapter; UPDATED marks substantive revisions; LIGHT EDITS marks limited wording and example refinements that can be skipped on a first reread.', '',
             'This is a guide to the current text, not a word-by-word redline. All 23 existing chapters received some edits; none is labeled unchanged.', '']
    for label, numbers in [('New chapters', new), ('Updated chapters', updated), ('Light edits', light)]:
        guide += ['## ' + label, '']
        guide += [f'- {n}. {titles[n]}' for n in sorted(numbers)]
        guide += ['']
    guide += ['## Appendices', '', 'Appendices E through H are new: All Field Notes; Repositories Behind the Book; Talk to the Book; Sources and Further Reading. Appendices A through D are updated.', '',
              'The separate reading copy preserves every chapter and appendix. Its labels do not change the canonical manuscript or published edition.', '']
    (root / 'review/v0.3-reading-guide.md').write_text('\n'.join(guide))

    # Keep the book source untouched. Only the separate review copy receives navigation labels.
    destination.parent.mkdir(exist_ok=True)
    doc.save(destination)
    check = Document(destination)
    new_headings = [p.text for p in check.paragraphs if p.style.name == 'Heading 1' and re.match(r'^(NEW|UPDATED|LIGHT EDITS) \| \d+\.', p.text)]
    assert len(new_headings) == 29
    for node in check.element.xpath('.//w:t'):
        inverse = {value: key for key, value in replacements.items()}
        if node.text in inverse:
            node.text = inverse[node.text]
    restored_cover = [p for p in check.paragraphs if p.text.startswith('v0.3 · November 1, 2026 · Review edition')][0]
    for run in list(restored_cover._p.findall(qn('w:r')))[1:]:
        restored_cover._p.remove(run)
    assert check.element.xml == unmodified_body, 'A change outside the review labels or cover was detected'
    # Keep navigation labels visibly smaller than chapter titles so they do not
    # push a chapter's closing paragraphs onto a near-empty extra page.
    before_label_styling = [p.text for p in doc.paragraphs]
    for p in doc.paragraphs:
        if p.style.name == 'Heading 1' and re.match(r'^(NEW|UPDATED|LIGHT EDITS) \| ', p.text):
            assert len(p.runs) == 1
            label, title = p.text.split(' | ', 1)
            original_run = p.runs[0]
            original_run.text = title
            if title.startswith(('3. ', '4. ', '7. ', 'Appendix B:')):
                original_run.font.size = Pt(19.5)
            marker = p.add_run(label + ' | ')
            marker.font.size = Pt(9.5)
            marker.bold = True
            original_run._r.addprevious(marker._r)
    assert [p.text for p in doc.paragraphs] == before_label_styling
    doc.save(destination)
    print('Created Google Docs reading copy: 6 NEW, 17 UPDATED, 6 LIGHT EDITS, and 8 appendices; all body content preserved.')
    print(destination)


if __name__ == "__main__":
    build()
