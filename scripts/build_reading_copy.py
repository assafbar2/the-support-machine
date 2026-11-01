"""Copy the canonical DOCX for Google Docs and build a plain navigation guide."""
import json
from pathlib import Path
import re
import shutil


def build():
    root = Path(__file__).resolve().parents[1]
    meta = json.loads((root / 'edition.json').read_text())
    version = meta['version']
    source = root / f'manuscript/The Support Machine - manuscript {version}.docx'
    destination = root / f'review/the-support-machine-{version}-reading-copy.docx'
    text = (root / 'skills/the-support-machine/references/book.md').read_text()
    chapters = re.findall(r'^## (\d+\. .+)$', text, re.M)
    appendices = re.findall(r'^## (Appendix [A-Z]: .+)$', text, re.M)
    assert len(chapters) == meta['chapters']
    assert len(appendices) == meta['appendices']
    destination.parent.mkdir(exist_ok=True)
    shutil.copyfile(source, destination)
    assert destination.read_bytes() == source.read_bytes()
    guide = [f'# The Support Machine {version} Reading Guide', '',
             'The reading copy contains the complete current book, with plain chapter titles in the contents and document outline. It is identical to the canonical manuscript. Discuss edits by chapter title and passage in our chat.', '',
             f'[Notes for the new version](../release-notes/{version}.md) explain what changed for returning readers.', '',
             '## Chapters', '']
    guide += [f'- {title}' for title in chapters]
    guide += ['', '## Appendices', '']
    guide += [f'- {title}' for title in appendices]
    guide += ['', "The Reader's Note links to The Prompt Room episode. Appendix G starts with skill installation and verification, followed by 80 practical prompts.", '']
    (root / f'review/{version}-reading-guide.md').write_text('\n'.join(guide))
    print(f'Created label-free Google Docs reading copy: {len(chapters)} chapters and {len(appendices)} appendices; identical to the canonical DOCX.')
    print(destination)


if __name__ == '__main__':
    build()
