"""Render the repository's supported Markdown subset without external services."""
import html
import re
from urllib.parse import urlsplit
from manuscript_format import blocks, spans, slugify, plain

def safe_url(target):
    scheme = urlsplit(target).scheme.lower()
    if scheme and scheme not in ("http","https","mailto"):
        raise ValueError("unsupported link scheme: "+scheme)
    return html.escape(target, quote=True)

def inline(text):
    result = []
    for kind, value, target in spans(text):
        escaped = html.escape(value)
        if kind == "link":
            result.append(f'<a href="{safe_url(target)}">{escaped}</a>')
        elif kind in ("bold","italic","code"):
            tag = {"bold":"strong","italic":"em","code":"code"}[kind]
            result.append(f"<{tag}>{escaped}</{tag}>")
        else:
            result.append(re.sub(r"https?://[^\s<>()]+", lambda m: '<a href="'+safe_url(html.unescape(m[0].rstrip(".,;")))+'">'+m[0].rstrip(".,;")+"</a>"+m[0][len(m[0].rstrip(".,;")):], escaped))
    return "".join(result)

def markdown_to_html(markdown):
    out, toc, seen = [], [], {}
    list_kind = None
    def close_list():
        nonlocal list_kind
        if list_kind:
            out.append("</"+list_kind+">")
            list_kind = None
    for kind, content, extra in blocks(markdown):
        if kind not in ("number","bullet"):
            close_list()
        if kind == "heading":
            title = plain(content)
            anchor = slugify(title)
            seen[anchor] = seen.get(anchor,0)+1
            if seen[anchor]>1:
                anchor += "-"+str(seen[anchor])
            toc.append((extra,title,anchor))
            cls = ' class="part"' if title.startswith("Part ") else ""
            out.append(f'<h{extra}{cls} id="{anchor}">{inline(content)}</h{extra}>')
        elif kind in ("number","bullet"):
            requested = "ol" if kind=="number" else "ul"
            if requested != list_kind:
                close_list()
                start = f' start="{extra}"' if requested=="ol" and extra!=1 else ""
                out.append("<"+requested+start+">")
                list_kind = requested
            value = f' value="{extra}"' if kind=="number" else ""
            out.append(f"<li{value}>{inline(content)}</li>")
        elif kind=="table":
            out.append('<div class="table-wrap"><table><thead><tr>')
            out += [f'<th scope="col">{inline(cell)}</th>' for cell in content[0]]
            out.append("</tr></thead><tbody>")
            for row in content[1:]:
                out.append("<tr>"+"".join(f"<td>{inline(cell)}</td>" for cell in row)+"</tr>")
            out.append("</tbody></table></div>")
        elif kind=="code":
            out.append("<pre><code>"+html.escape(content)+"</code></pre>")
        elif kind=="quote":
            out.append("<blockquote>"+inline(content)+"</blockquote>")
        else:
            out.append("<p>"+inline(content)+"</p>")
    close_list()
    return "\n".join(out),toc
