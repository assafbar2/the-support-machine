import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

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

if __name__=="__main__":
    unittest.main()
