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
PROGRESS_JS_PATH = ROOT / "site" / "progress.js"
SYLLABUS_PATH = ROOT / "docs" / "syllabus.md"
ROADMAP_PATH = ROOT / "ROADMAP.md"
GLOSSARY_PATH = ROOT / "glossary" / "terms.md"
DEFAULT_REPO_BLOB_BASE = "https://github.com/raghunandanask/gpu-training/blob/main"


def strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def lesson_href(lesson_id: str) -> str:
    return f"lessons/{lesson_id.replace('/', '__')}.html"


def phase_label(phase_id: str) -> str:
    label = re.sub(r"^\d+-", "", phase_id).replace("-", " ")
    return label.title()


def status_label(status: str) -> str:
    labels = {
        "planned": "Planned",
        "documented": "Documented",
        "runnable": "Runnable",
    }
    return labels.get(status, status.title())


def progress_percent(done: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return max(0.0, min(100.0, (done / total) * 100.0))


def detect_repo_blob_base(catalog: dict) -> str:
    for phase in catalog.get("phases", []):
        for lesson in phase.get("lessons", []):
            colab_url = str(lesson.get("colab_url", ""))
            match = re.search(
                r"colab\.research\.google\.com/github/([^/]+)/([^/]+)/blob/([^/]+)/",
                colab_url,
            )
            if match:
                owner, repo, branch = match.groups()
                return f"https://github.com/{owner}/{repo}/blob/{branch}"
    return DEFAULT_REPO_BLOB_BASE


def repo_blob_url(repo_blob_base: str, relative_path: str) -> str:
    return f"{repo_blob_base}/{relative_path.lstrip('/')}"


def md_to_html_inline(text: str) -> str:
    text = escape(text)
    text = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: f'<img alt="{escape(m.group(1))}" src="{escape(m.group(2))}" loading="lazy" />',
        text,
    )
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{escape(m.group(2))}">{escape(m.group(1))}</a>',
        text,
    )
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
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
            html.append(f"<li>{md_to_html_inline(line[2:])}</li>")
        else:
            html.append(f"<p>{md_to_html_inline(line)}</p>")

    if in_list:
        html.append("</ul>")
    if in_code:
        html.append("</code></pre>")

    return "\n".join(html)


def nav_link(href: str, label: str, current_page: str, path_prefix: str = "") -> str:
    active = ' aria-current="page"' if current_page == href else ""
    return f'<a class="nav-link" href="{path_prefix}{href}"{active}>{label}</a>'


def page_shell(
    title: str, content: str, current_page: str, scripts: str = "", path_prefix: str = ""
) -> str:
    nav = (
        nav_link("index.html", "Contents", current_page, path_prefix=path_prefix)
        + nav_link("catalog.html", "Catalog", current_page, path_prefix=path_prefix)
        + nav_link("roadmap.html", "Roadmap", current_page, path_prefix=path_prefix)
        + nav_link("glossary.html", "Glossary", current_page, path_prefix=path_prefix)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{escape(title)}</title>
  <style>
  :root{{
    --bg:#141416;
    --panel:#1d1d21;
    --panel-soft:#24242a;
    --text:#f5f5f4;
    --muted:#b8b8b2;
    --accent:#f97316;
    --accent-soft:#fdba74;
    --ok:#34d399;
    --warn:#fbbf24;
    --planned:#64748b;
  }}
  *{{box-sizing:border-box}}
  body{{font-family:Inter,Segoe UI,system-ui,-apple-system,sans-serif;background:var(--bg);color:var(--text);margin:0;line-height:1.6}}
  .skip-link{{position:absolute;left:-9999px}}
  .skip-link:focus{{left:16px;top:12px;background:#000;padding:6px 10px;border-radius:8px;z-index:10}}
  .site-header{{position:sticky;top:0;background:rgba(20,20,22,.95);border-bottom:1px solid #2a2a31;backdrop-filter:blur(8px);z-index:8}}
  .header-inner{{max-width:1120px;margin:0 auto;padding:10px 20px;display:flex;justify-content:space-between;gap:12px;align-items:center}}
  .site-name{{font-weight:700;letter-spacing:.02em}}
  nav{{display:flex;gap:6px;flex-wrap:wrap}}
  .nav-link{{display:inline-flex;padding:6px 10px;border-radius:999px;text-decoration:none;color:var(--muted);border:1px solid transparent}}
  .nav-link[aria-current="page"]{{color:var(--text);border-color:#3f3f46;background:#27272a}}
  .container{{max-width:1120px;margin:0 auto;padding:28px 20px 40px}}
  a{{color:var(--accent-soft)}}
  p{{margin:10px 0 14px}}
  h1,h2,h3{{font-family:"Avenir Next Condensed","Arial Narrow",Inter,sans-serif;letter-spacing:.02em;line-height:1.2}}
  h1{{font-size:clamp(2rem,4vw,3rem);margin:0 0 10px}}
  h2{{font-size:1.55rem;margin:26px 0 12px}}
  h3{{font-size:1.2rem;margin:22px 0 8px}}
  .mono, code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-variant-numeric:tabular-nums}}
  .muted{{color:var(--muted)}}
  .hero{{display:grid;grid-template-columns:1.3fr 1fr;gap:18px;align-items:start}}
  .hero-card{{background:var(--panel);border:1px solid #30303a;border-radius:14px;padding:16px}}
  .preface{{font-size:1.05rem}}
  .stats{{display:grid;gap:10px}}
  .stat{{display:grid;grid-template-columns:1fr auto;gap:8px;background:var(--panel);border:1px solid #30303a;border-radius:10px;padding:10px 12px}}
  .stat .bar{{grid-column:1 / -1;height:7px;background:#2d2d35;border-radius:999px;overflow:hidden}}
  .stat .bar > span{{display:block;height:100%;background:linear-gradient(90deg,var(--accent),#fb923c);width:0%}}
  .pill{{display:inline-flex;align-items:center;border:1px solid #3f3f46;border-radius:999px;padding:2px 10px;font-size:.78rem;line-height:1.6;margin-right:6px;color:#d4d4d8}}
  .pill.status-runnable{{border-color:#065f46;color:#34d399}}
  .pill.status-documented{{border-color:#713f12;color:#fbbf24}}
  .pill.status-planned{{border-color:#334155;color:#94a3b8}}
  .panel{{background:var(--panel);border:1px solid #30303a;border-radius:14px;padding:14px}}
  .phase-row{{border-bottom:1px dashed #3f3f46;padding:12px 0}}
  .phase-row:last-child{{border-bottom:none}}
  details summary{{cursor:pointer;list-style:none}}
  details summary::-webkit-details-marker{{display:none}}
  .phase-meta{{display:flex;justify-content:space-between;gap:8px;align-items:center;flex-wrap:wrap}}
  .mini-bar{{height:5px;background:#2f2f37;border-radius:999px;margin-top:8px;overflow:hidden}}
  .mini-bar > span{{display:block;height:100%;background:var(--accent);width:0%}}
  .lesson-list{{margin:10px 0 0 0;padding:0;list-style:none;display:grid;gap:10px}}
  .lesson-item{{background:var(--panel-soft);border:1px solid #34343f;border-radius:10px;padding:10px}}
  .lesson-item-top{{display:flex;justify-content:space-between;gap:8px;align-items:flex-start;flex-wrap:wrap}}
  .lesson-meta{{font-size:.88rem;color:var(--muted)}}
  .table-wrap{{overflow:auto}}
  table{{width:100%;border-collapse:collapse;min-width:780px;background:var(--panel);border:1px solid #30303a;border-radius:12px;overflow:hidden}}
  th,td{{padding:10px 12px;border-bottom:1px solid #2f2f39;text-align:left;vertical-align:top}}
  th{{font-size:.82rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}}
  tr:last-child td{{border-bottom:none}}
  .filters{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:10px;margin:14px 0 16px}}
  input,select,button{{background:#18181b;border:1px solid #3f3f46;color:var(--text);padding:8px 10px;border-radius:8px}}
  button{{cursor:pointer}}
  .lesson-shell{{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:18px}}
  .lesson-sidebar{{position:sticky;top:72px;align-self:start;display:grid;gap:10px}}
  .fact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px 12px;font-size:.92rem}}
  .fact-grid dt{{color:var(--muted)}}
  .fact-grid dd{{margin:0}}
  .cta{{display:inline-block;padding:9px 12px;background:var(--accent);color:#111;text-decoration:none;border-radius:9px;font-weight:600}}
  .checks{{display:grid;gap:8px;font-size:.95rem}}
  .site-footer{{margin-top:28px;padding-top:14px;border-top:1px solid #31313b;color:var(--muted);font-size:.9rem}}
  pre{{background:#0f1013;padding:12px;border-radius:8px;overflow:auto;position:relative;border:1px solid #2f3038}}
  .copy-button{{position:absolute;top:8px;right:8px;background:#1f2937;color:#fff;border:1px solid #374151;border-radius:6px;padding:4px 8px;cursor:pointer}}
  blockquote{{margin:16px 0;padding:10px 14px;border-left:4px solid var(--accent);background:#1d1d23}}
  img{{max-width:100%;height:auto}}
  @media (max-width:900px){{
    .hero{{grid-template-columns:1fr}}
    .lesson-shell{{grid-template-columns:1fr}}
    .lesson-sidebar{{position:static}}
    .filters{{grid-template-columns:1fr 1fr}}
  }}
  @media (max-width:640px){{
    .filters{{grid-template-columns:1fr}}
  }}
  </style>
</head>
<body>
  <a class="skip-link" href="#content">Skip to content</a>
  <header class="site-header">
    <div class="header-inner">
      <div class="site-name">GPU Engineering From Scratch</div>
      <nav aria-label="Global">{nav}</nav>
    </div>
  </header>
  <main class="container" id="content">
    {content}
    <footer class="site-footer">
      Colab-first curriculum. Open source on GitHub.
    </footer>
  </main>
  <script src="{path_prefix}progress.js" defer></script>
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
  {scripts}
</body>
</html>
"""


def make_index(catalog: dict, repo_blob_base: str) -> str:
    total_lessons = int(catalog.get("lesson_count", 0))
    total_runnable = int(catalog.get("runnable_count", 0))
    phase_count = int(catalog.get("phase_count", 0))
    terms_count = count_glossary_terms(GLOSSARY_PATH.read_text(encoding="utf-8"))

    rows = []
    for phase in catalog["phases"]:
        phase_id = str(phase["id"])
        lessons = phase["lessons"]
        runnable_count = sum(1 for lesson in lessons if lesson.get("status") == "runnable")
        rows.append(
            f'<details class="phase-row" data-phase-id="{escape(phase_id)}" open>'
            f'<summary>'
            f'<div class="phase-meta">'
            f'<div><strong class="mono">{escape(phase_id[:2])}</strong> {escape(phase_label(phase_id))}</div>'
            f'<div class="lesson-meta"><span data-phase-progress="{escape(phase_id)}">0/{len(lessons)}</span> lessons completed</div>'
            f"</div>"
            f'<div class="mini-bar"><span style="width:{progress_percent(runnable_count, len(lessons)):.2f}%"></span></div>'
            f"</summary>"
        )
        rows.append('<ul class="lesson-list">')
        for lesson in phase["lessons"]:
            href = lesson_href(lesson["id"])
            artifacts = lesson.get("artifacts", [])
            artifact_links = ""
            if artifacts:
                first_artifact = artifacts[0]
                artifact_links = (
                    f'<div class="lesson-meta">Artifact: '
                    f'<a href="{escape(repo_blob_url(repo_blob_base, str(first_artifact["path"])))}" target="_blank" rel="noreferrer">{escape(str(first_artifact["name"]))}</a>'
                    f"</div>"
                )
            rows.append(
                '<li class="lesson-item">'
                '<div class="lesson-item-top">'
                f'<a href="{escape(href)}"><strong>{escape(str(lesson["title"]))}</strong></a>'
                f'<div><span class="pill">{escape(str(lesson["type"]))}</span><span class="pill status-{escape(str(lesson.get("status", "planned")))}">{escape(status_label(str(lesson.get("status", "planned"))))}</span></div>'
                "</div>"
                f'<div class="lesson-meta mono">{int(lesson.get("duration_minutes", 0))} min | {escape(str(lesson.get("runtime", "Google Colab")))}</div>'
                f"{artifact_links}"
                "</li>"
            )
        rows.append("</ul></details>")
    content = "".join(
        [
            '<section class="hero">',
            '<article class="hero-card">',
            "<h1>GPU Engineering From Scratch (Colab First)</h1>",
            '<p class="preface">Colab-first GPU literacy for DevOps, Data Science, and Data Engineering teams. Learn core ideas, run practical labs, and ship reusable artifacts.</p>',
            '<p class="muted">Scattered GPU content rarely leads to repeatable outcomes. This curriculum keeps each lesson in a fixed loop: intuition, implementation, and a shipped output artifact.</p>',
            '<p><span class="pill">Linear Path: 00 -> 07</span><span class="pill">Role Path: DevOps | Data Science | Data Engineering</span></p>',
            "</article>",
            '<aside class="stats">',
            '<div class="stat"><div>Lessons finished</div><div class="mono" id="stat-lessons-finished">0/0</div><div class="bar"><span id="bar-lessons-finished"></span></div></div>',
            f'<div class="stat"><div>Colab labs runnable</div><div class="mono">{total_runnable}/{total_lessons}</div><div class="bar"><span style="width:{progress_percent(total_runnable, total_lessons):.2f}%"></span></div></div>',
            '<div class="stat"><div>Phases started</div><div class="mono" id="stat-phases-started">0/0</div><div class="bar"><span id="bar-phases-started"></span></div></div>',
            f'<div class="stat"><div>Glossary terms</div><div class="mono">{terms_count}</div><div class="bar"><span style="width:100%"></span></div></div>',
            "</aside>",
            "</section>",
            '<section class="panel" style="margin-top:16px">',
            "<h2>Phase Contents</h2>",
            "".join(rows),
            "</section>",
            '<section class="panel" style="margin-top:16px">',
            "<h2>Colophon</h2>",
            "<p>This curriculum is Colab-only by design. Use lesson pages for notebooks and artifact outputs.</p>",
            '<p class="mono">git clone https://github.com/raghunandanask/gpu-training.git</p>',
            f'<p><a href="{escape(repo_blob_url(repo_blob_base, "docs/colab-guide.md"))}" target="_blank" rel="noreferrer">Read the Colab guide</a> | <button type="button" id="reset-progress">Reset browser progress</button></p>',
            "</section>",
        ]
    )
    scripts = (
        '<script id="catalog-json" type="application/json">'
        + json.dumps(catalog)
        + "</script>"
        """
<script>
  window.addEventListener('DOMContentLoaded',()=>{
    const el=document.getElementById('catalog-json');
    if(!el || !window.GPUProgress) return;
    const catalog=JSON.parse(el.textContent);
    window.GPUProgress.renderHomeStats(catalog);
    const btn=document.getElementById('reset-progress');
    if(btn){
      btn.addEventListener('click',()=>{
        window.GPUProgress.reset();
        window.GPUProgress.renderHomeStats(catalog);
      });
    }
  });
</script>
"""
    )
    return page_shell("GPU Curriculum", content, "index.html", scripts=scripts)


def count_glossary_terms(md_text: str) -> int:
    return sum(1 for line in md_text.splitlines() if line.startswith("## "))


def lesson_index(catalog: dict) -> list[dict]:
    ordered: list[dict] = []
    for phase in catalog["phases"]:
        for lesson in phase["lessons"]:
            ordered.append(lesson)
    return ordered


def make_catalog(catalog: dict, repo_blob_base: str) -> str:
    phase_options = ['<option value="">All phases</option>']
    phase_options.extend(
        f'<option value="{escape(str(phase["id"]))}">{escape(phase_label(str(phase["id"])))}</option>'
        for phase in catalog["phases"]
    )
    rows = []
    for phase in catalog["phases"]:
        for lesson in phase["lessons"]:
            roles = ",".join(str(role) for role in lesson.get("roles", []))
            artifacts = lesson.get("artifacts", [])
            artifact_html = ""
            if artifacts:
                links = [
                    f'<a href="{escape(repo_blob_url(repo_blob_base, str(item["path"])))}" target="_blank" rel="noreferrer">{escape(str(item["name"]))}</a>'
                    for item in artifacts
                ]
                artifact_html = " | ".join(links)
            else:
                artifact_html = "<span class='muted'>-</span>"
            rows.append(
                "<tr "
                f'data-title="{escape(str(lesson["title"]).lower())}" '
                f'data-phase="{escape(str(phase["id"]))}" '
                f'data-type="{escape(str(lesson.get("type", "")))}" '
                f'data-status="{escape(str(lesson.get("status", "planned")))}" '
                f'data-roles="{escape(roles)}">'
                f"<td>{escape(str(phase['id'])[:2])}</td>"
                f'<td><a href="{escape(lesson_href(str(lesson["id"])))}">{escape(str(lesson["title"]))}</a></td>'
                f"<td>{escape(str(lesson.get('type', 'Learn')))}</td>"
                f"<td>{escape(str(lesson.get('runtime', 'Google Colab')))}</td>"
                f"<td><span class='pill status-{escape(str(lesson.get('status', 'planned')))}'>{escape(status_label(str(lesson.get('status', 'planned'))))}</span></td>"
                f"<td>{artifact_html}</td>"
                "</tr>"
            )
    content = (
        "<h1>Catalog</h1>"
        "<p class='muted'>Filter lessons by phase, type, role, status, or free-text query.</p>"
        "<div class='filters'>"
        '<input id="catalog-search" type="search" placeholder="Search lessons or artifacts..." />'
        f'<select id="catalog-phase">{"".join(phase_options)}</select>'
        '<select id="catalog-type"><option value="">All types</option><option value="Learn">Learn</option><option value="Build">Build</option><option value="Project">Project</option></select>'
        '<select id="catalog-status"><option value="">All status</option><option value="runnable">Runnable</option><option value="documented">Documented</option><option value="planned">Planned</option></select>'
        '<select id="catalog-role"><option value="">All roles</option><option value="devops">DevOps</option><option value="data-science">Data Science</option><option value="data-engineering">Data Engineering</option></select>'
        "</div>"
        "<div class='table-wrap'>"
        "<table>"
        "<thead><tr><th>Phase</th><th>Lesson</th><th>Type</th><th>Runtime</th><th>Status</th><th>Outputs</th></tr></thead>"
        f"<tbody id='catalog-body'>{''.join(rows)}</tbody>"
        "</table>"
        "</div>"
    )
    scripts = """
<script>
window.addEventListener('DOMContentLoaded',()=>{
  const body=document.getElementById('catalog-body');
  const search=document.getElementById('catalog-search');
  const phase=document.getElementById('catalog-phase');
  const type=document.getElementById('catalog-type');
  const status=document.getElementById('catalog-status');
  const role=document.getElementById('catalog-role');
  if(!body || !search || !phase || !type || !status || !role) return;

  const params=new URLSearchParams(window.location.search);
  if(params.get('q')) search.value=params.get('q');
  if(params.get('phase')) phase.value=params.get('phase');
  if(params.get('type')) type.value=params.get('type');
  if(params.get('status')) status.value=params.get('status');
  if(params.get('role')) role.value=params.get('role');

  const apply=()=>{
    const q=search.value.trim().toLowerCase();
    const p=phase.value;
    const t=type.value;
    const s=status.value;
    const r=role.value;
    Array.from(body.querySelectorAll('tr')).forEach((row)=>{
      const title=(row.dataset.title || '');
      const phaseMatch=!p || row.dataset.phase===p;
      const typeMatch=!t || row.dataset.type===t;
      const statusMatch=!s || row.dataset.status===s;
      const roleMatch=!r || (row.dataset.roles || '').split(',').includes(r);
      const queryMatch=!q || row.textContent.toLowerCase().includes(q) || title.includes(q);
      row.hidden=!(phaseMatch && typeMatch && statusMatch && roleMatch && queryMatch);
    });
    const next=new URLSearchParams();
    if(q) next.set('q',q);
    if(p) next.set('phase',p);
    if(t) next.set('type',t);
    if(s) next.set('status',s);
    if(r) next.set('role',r);
    const query=next.toString();
    window.history.replaceState({},'',query ? `?${query}` : window.location.pathname);
  };

  [search,phase,type,status,role].forEach((el)=>el.addEventListener('input',apply));
  [phase,type,status,role].forEach((el)=>el.addEventListener('change',apply));
  apply();
});
</script>
"""
    return page_shell("Catalog", content, "catalog.html", scripts=scripts)


def make_glossary() -> str:
    md_text = GLOSSARY_PATH.read_text(encoding="utf-8")
    lines = strip_front_matter(md_text).splitlines()
    html_parts = ["<h1>Glossary</h1>", "<p class='muted'>Plain-language terms used across labs and capstones.</p>"]
    for line in lines:
        if line.startswith("## "):
            term = line[3:].strip()
            slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
            html_parts.append(f'<h2 id="{escape(slug)}">{escape(term)}</h2>')
        elif line.startswith("# "):
            continue
        elif line.strip():
            html_parts.append(f"<p>{md_to_html_inline(line)}</p>")
    return page_shell("Glossary", "".join(html_parts), "glossary.html")


def make_roadmap() -> str:
    syllabus_html = md_to_html(SYLLABUS_PATH.read_text(encoding="utf-8"))
    roadmap_html = md_to_html(ROADMAP_PATH.read_text(encoding="utf-8"))
    content = (
        "<h1>Syllabus and Roadmap</h1>"
        "<p class='muted'>Curriculum structure plus milestone waves for delivery.</p>"
        "<section class='panel'><h2>Syllabus</h2>"
        f"{syllabus_html}</section>"
        "<section class='panel' style='margin-top:14px'><h2>Wave Milestones</h2>"
        f"{roadmap_html}</section>"
    )
    return page_shell("Roadmap", content, "roadmap.html")


def remove_colab_badge_line(md_text: str) -> str:
    lines = md_text.splitlines()
    cleaned = [line for line in lines if "colab-badge.svg" not in line]
    return "\n".join(cleaned)


def lesson_meta_list(items: list[str]) -> str:
    if not items:
        return "<span class='muted'>-</span>"
    return ", ".join(escape(item) for item in items)


def make_lesson_page(
    catalog: dict, lesson: dict, previous: dict | None, next_lesson: dict | None, repo_blob_base: str
) -> str:
    doc_path = ROOT / str(lesson["doc_path"])
    raw_md = doc_path.read_text(encoding="utf-8")
    body = md_to_html(remove_colab_badge_line(raw_md))
    lesson_id = str(lesson["id"])
    prev_link = (
        f'<a href="../{escape(lesson_href(str(previous["id"])))}">Previous</a>'
        if previous
        else "<span class='muted'>Previous</span>"
    )
    next_link = (
        f'<a href="../{escape(lesson_href(str(next_lesson["id"])))}">Next</a>'
        if next_lesson
        else "<span class='muted'>Next</span>"
    )
    artifacts = lesson.get("artifacts", [])
    artifact_links = "<span class='muted'>No outputs indexed yet.</span>"
    if artifacts:
        links = [
            f'<li><a href="{escape(repo_blob_url(repo_blob_base, str(item["path"])))}" target="_blank" rel="noreferrer">{escape(str(item["name"]))}</a> <span class="pill">{escape(str(item["type"]))}</span></li>'
            for item in artifacts
        ]
        artifact_links = f"<ul>{''.join(links)}</ul>"

    colab_url = str(lesson.get("colab_url", "")).strip()
    colab_cta = "<span class='muted'>Notebook pending.</span>"
    if colab_url.startswith("https://"):
        colab_cta = (
            f'<a class="cta" href="{escape(colab_url)}" target="_blank" rel="noreferrer">Open in Colab</a>'
        )

    sidebar = (
        '<aside class="lesson-sidebar">'
        f"{colab_cta}"
        f"<div class='panel'><strong>{escape(str(lesson.get('title', 'Lesson')))}</strong>"
        "<dl class='fact-grid'>"
        f"<dt>Type</dt><dd>{escape(str(lesson.get('type', 'Learn')))}</dd>"
        f"<dt>Status</dt><dd>{escape(status_label(str(lesson.get('status', 'planned'))))}</dd>"
        f"<dt>Duration</dt><dd class='mono'>{int(lesson.get('duration_minutes', 0))} min</dd>"
        f"<dt>Runtime</dt><dd>{escape(str(lesson.get('runtime', 'Google Colab')))}</dd>"
        f"<dt>Roles</dt><dd>{lesson_meta_list([str(v) for v in lesson.get('roles', [])])}</dd>"
        f"<dt>Prerequisites</dt><dd>{lesson_meta_list([str(v) for v in lesson.get('prerequisites', [])])}</dd>"
        f"<dt>Objectives</dt><dd>{lesson_meta_list([str(v) for v in lesson.get('objectives', [])])}</dd>"
        "</dl></div>"
        f"<div class='panel'><strong>Outputs</strong>{artifact_links}</div>"
        f"<div class='panel checks'>"
        f'<label><input type="checkbox" data-lesson-check="ran" data-lesson-id="{escape(lesson_id)}" /> Ran Colab notebook</label>'
        f'<label><input type="checkbox" data-lesson-check="artifact" data-lesson-id="{escape(lesson_id)}" /> Saved artifact to outputs/</label>'
        f'<button type="button" data-mark-complete="{escape(lesson_id)}">Mark complete</button>'
        "</div>"
        f"<div class='panel mono'>{prev_link} | {next_link}</div>"
        "</aside>"
    )
    content = (
        '<div class="lesson-shell">'
        '<article class="panel">'
        f'<p><a href="../index.html">Back to Contents</a> | <a href="../catalog.html">Open Catalog</a></p>'
        f"{body}"
        "</article>"
        f"{sidebar}"
        "</div>"
    )
    scripts = """
<script>
window.addEventListener('DOMContentLoaded',()=>{
  if(!window.GPUProgress) return;
  window.GPUProgress.bindLessonControls();
});
</script>
"""
    return page_shell(str(lesson["title"]), content, "", scripts=scripts, path_prefix="../")


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    repo_blob_base = detect_repo_blob_base(catalog)

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    (DIST_DIR / "lessons").mkdir(parents=True, exist_ok=True)

    (DIST_DIR / "index.html").write_text(make_index(catalog, repo_blob_base), encoding="utf-8")
    (DIST_DIR / "catalog.html").write_text(make_catalog(catalog, repo_blob_base), encoding="utf-8")
    (DIST_DIR / "glossary.html").write_text(make_glossary(), encoding="utf-8")
    (DIST_DIR / "roadmap.html").write_text(make_roadmap(), encoding="utf-8")
    shutil.copy2(PROGRESS_JS_PATH, DIST_DIR / "progress.js")

    ordered_lessons = lesson_index(catalog)
    for idx, lesson in enumerate(ordered_lessons):
        previous = ordered_lessons[idx - 1] if idx > 0 else None
        next_lesson = ordered_lessons[idx + 1] if idx + 1 < len(ordered_lessons) else None
        page = make_lesson_page(catalog, lesson, previous, next_lesson, repo_blob_base)
        out_path = DIST_DIR / lesson_href(str(lesson["id"]))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")

    (DIST_DIR / "catalog.json").write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Built site at {DIST_DIR}")


if __name__ == "__main__":
    main()
