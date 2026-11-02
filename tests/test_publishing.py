import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import base64
from docx import Document
from docx.shared import Inches

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from manuscript_format import blocks,plain
from import_markdown_to_docx import create
from export_docx_to_markdown import export_docx
from render_markdown import markdown_to_html

class PublishingTests(unittest.TestCase):
    def test_docx_round_trip_links_numbers_and_tables(self):
        text="# Test Book\n\n## Contents\n\n- [A chapter](#1-a-chapter)\n\n## 1. A chapter\n\nAn **important** [source](https://example.com/a?x=1&y=2).\n\n3. First\n4. Next\n\n| Item | Evidence |\n|---|---|\n| One | [Record](https://example.com/record) |\n"
        with TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/"input.md").write_text(text)
            create(p/"input.md",p/"output.docx")
            export_docx(p/"output.docx",p/"output.md")
            result=(p/"output.md").read_text()
        self.assertIn("[A chapter](#1-a-chapter)",result)
        self.assertIn("[source](https://example.com/a?x=1&y=2)",result)
        self.assertIn("3. First\n\n4. Next",result)
        self.assertIn("[Record](https://example.com/record)",result)
        self.assertIn("**important**",result)

    def test_html_numbers_and_unique_anchors(self):
        text="## Same\n\n3. Three\n4. Four\n\n## Same\n\n- One\n\nTail."
        html,toc=markdown_to_html(text)
        self.assertIn('<ol start="3">',html)
        self.assertIn('<li value="4">Four</li>',html)
        self.assertIn("</ol>",html)
        self.assertEqual([x[2] for x in toc],["same","same-2"])
        self.assertIn("</ul>\n<p>Tail.</p>",html)

    def test_html_escapes_text_and_blocks_executable_links(self):
        html,_=markdown_to_html("Text <script> and [safe](https://example.com/?a=1&b=2).")
        self.assertIn("&lt;script&gt;",html)
        self.assertIn("a=1&amp;b=2",html)
        with self.assertRaises(ValueError):
            markdown_to_html("[bad](javascript:alert)")

    def test_illustration_bytes_and_alt_survive_all_text_formats(self):
        png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+X2ioAAAAASUVORK5CYII=')
        alt='Evidence [checked] & followed up'
        with TemporaryDirectory() as tmp:
            p=Path(tmp)
            (p/'sample.png').write_bytes(png)
            doc=Document()
            doc.add_paragraph('Illustrated book',style='Title')
            shape=doc.add_paragraph().add_run().add_picture(str(p/'sample.png'),width=Inches(1))
            shape._inline.docPr.set('name','sample')
            shape._inline.docPr.set('descr',alt)
            caption=doc.add_paragraph()
            caption.add_run('Figure 1 — Evidence. ').bold=True
            caption.add_run('Check the outcome.')
            doc.save(p/'source.docx')
            export_docx(p/'source.docx',p/'book.md')
            result=(p/'book.md').read_text()
            self.assertEqual((p/'illustrations/sample.png').read_bytes(),png)
            html,_=markdown_to_html(result,image_base='downloads')
            self.assertIn('src="downloads/illustrations/sample.png"',html)
            self.assertIn('alt="Evidence [checked] &amp; followed up"',html)
            self.assertIn('<figcaption><strong>Figure 1',html)
            create(p/'book.md',p/'imported.docx')
            imported=Document(p/'imported.docx')
            self.assertEqual(len(imported.inline_shapes),1)
            self.assertEqual(imported.inline_shapes[0]._inline.docPr.get('descr'),alt)
            self.assertEqual(len([p for p in imported.paragraphs if p.style.name=='Book Figure']),1)
            self.assertEqual(len([p for p in imported.paragraphs if p.style.name=='Book Figure Caption']),1)

    def test_html_rejects_executable_image_urls(self):
        with self.assertRaises(ValueError):
            markdown_to_html('![Picture](javascript:alert)')

if __name__=="__main__":
    unittest.main()
