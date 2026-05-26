#!/usr/bin/env python3
"""Build a static curriculum site in site/dist."""

from __future__ import annotations

import json
import re
import shutil
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = ROOT / "site" / "dist"
CATALOG_PATH = ROOT / "catalog.json"


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def md_to_html(md: str) -> str:
    lines = strip_front_matter(md).splitlines()
    html = []
    in_code = False
    code_lang = ""
    in_list = False

    for line in lines:
        if line.startswith("```"):
            if in_code:
                html.append("</code></pre>")
                in_code = False
                code_lang = ""
            else:
                code_lang = line.removeprefix("```").strip()
                cls = f' class="language-{escape(code_lang)}"' if code_lang else ""
                html.append(f"<pre><code{cls}>")
                in_code = True
            continue

        if in_code:
            html.append(escape(line))
            continue

        if not line.strip():
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append("")
            continue

        if line.startswith("### "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h3>{escape(line[4:])}</h3>")
        elif line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{escape(line[3:])}</h2>")
        elif line.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h1>{escape(line[2:])}</h1>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{escape(line[2:])}</li>")
        else:
            line = re.sub(r"`([^`]+)`", r"<code>\1</code>", escape(line))
            html.append(f"<p>{line}</p>")

    if in_list:
        html.append("</ul>")
    if in_code:
        html.append("</code></pre>")

    return "\n".join(html)


def lesson_path(lesson_id: str) -> str:
    return f"lessons/{lesson_id.replace('/', '__')}.html"


def page_shell(title: str, content: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <style>
  body{{font-family:Arial,sans-serif;background:#0e1116;color:#e6edf3;margin:0}}
  .container{{max-width:980px;margin:0 auto;padding:24px}}
  a{{color:#7db3ff}}
  pre{{background:#111827;padding:12px;border-radius:8px;overflow:auto;position:relative}}
  code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
  .pill{{display:inline-block;border:1px solid #374151;border-radius:999px;padding:2px 8px;font-size:12px;margin-left:6px}}
  .copy-button{{position:absolute;top:8px;right:8px;background:#1f2937;color:#fff;border:1px solid #374151;border-radius:6px;padding:4px 8px;cursor:pointer}}
  </style>
</head>
<body>
  <main class="container">
    {content}
  </main>
  <script>
    document.querySelectorAll('pre').forEach((pre)=>{{
      const btn=document.createElement('button');
      btn.className='copy-button';
      btn.textContent='Copy';
      btn.addEventListener('click',async()=>{{
        const code=pre.querySelector('code');
        if(!code) return;
        await navigator.clipboard.writeText(code.innerText);
        btn.textContent='Copied';
        setTimeout(()=>btn.textContent='Copy',1000);
      }});
      pre.appendChild(btn);
    }});
  </script>
</body>
</html>
"""


def make_index(catalog: dict) -> str:
    rows = []
    for phase in catalog["phases"]:
        rows.append(f"<section><h2>{escape(phase['id'])}</h2>")
        rows.append("<ul>")
        for lesson in phase["lessons"]:
            href = lesson_path(lesson["id"])
            rows.append(
                f'<li><a href="{escape(href)}">{escape(str(lesson["title"]))}</a> '
                f'<span class="pill">{escape(str(lesson["type"]))}</span></li>'
            )
        rows.append("</ul></section>")
    content = (
        "<h1>GPU Engineering From Scratch (Colab First)</h1>"
        "<p>All executable lessons are Colab-only. Use the lesson page to copy code or open notebook directly in Colab.</p>"
        + "".join(rows)
    )
    return page_shell("GPU Curriculum", content)


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    (DIST_DIR / "lessons").mkdir(parents=True, exist_ok=True)

    (DIST_DIR / "index.html").write_text(make_index(catalog), encoding="utf-8")

    for phase in catalog["phases"]:
        for lesson in phase["lessons"]:
            doc_rel = lesson["doc_path"]
            doc_path = ROOT / doc_rel
            raw_md = doc_path.read_text(encoding="utf-8")
            body = md_to_html(raw_md)
            colab_link = ""
            if lesson.get("colab_url"):
                colab = escape(lesson["colab_url"])
                colab_link = f'<p><a href="{colab}" target="_blank" rel="noreferrer">Open in Colab</a></p>'
            home_link = '<p><a href="../index.html">Back to curriculum</a></p>'
            page = page_shell(str(lesson["title"]), home_link + colab_link + body)
            out_path = DIST_DIR / lesson_path(lesson["id"])
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(page, encoding="utf-8")

    (DIST_DIR / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Built site at {DIST_DIR}")


if __name__ == "__main__":
    main()
