"""Regenerate all derived edition files from the current DOCX and its rendered PDF."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from export_docx_to_markdown import export_docx
from build_site import build

ROOT=Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf",required=True,type=Path,help="PDF rendered from the current canonical DOCX")
    args=parser.parse_args()
    if not args.pdf.is_file():
        parser.error("rendered PDF does not exist")
    meta=json.loads((ROOT/"edition.json").read_text())
    version=meta["version"]
    source=ROOT/f"manuscript/The Support Machine - manuscript {version}.docx"
    markdown=ROOT/"skills/the-support-machine/references/book.md"
    pdf=ROOT/f"docs/the-support-machine-{version}.pdf"
    export_docx(source,markdown)
    if args.pdf.resolve()!=pdf.resolve():
        shutil.copyfile(args.pdf,pdf)
    build()
    paths=[source,markdown,pdf,ROOT/"docs/book.html",ROOT/"docs/notes.html",ROOT/"docs/review.html"]
    paths+=sorted((ROOT/"docs/downloads").glob("*"+version+"*"))
    paths+=[ROOT/"docs/downloads/the-support-machine.skill",ROOT/"docs/downloads/support-ai-evals.skill"]
    manifest={"version":version,"source":str(source.relative_to(ROOT)),
              "files":{str(p.relative_to(ROOT)):sha(p) for p in paths}}
    (ROOT/f"release-notes/{version}-checksums.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Built "+version+" from canonical DOCX and supplied rendered PDF.")

if __name__=="__main__":
    main()
