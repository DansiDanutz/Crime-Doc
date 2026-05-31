#!/usr/bin/env python3
"""export-episode.py — STATE 7. Bundle an episode's states into one clean document.

Concatenates 01-idea → 05-thumbnails behind a cover sheet (pulled from episode.yaml) and a
shotlist summary (from production/shotlist.json), writing a combined Markdown file and a
standalone, printable HTML file (open in a browser → Print → Save as PDF). No third-party deps.

Usage:
    tools/export-episode.py <channel> <episode-slug>
    tools/export-episode.py channels/umbra/episodes/ep01-the-man-who-said-no
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTIONS = ["01-idea.md", "02-script.md", "03-characters.md", "04-scenes.md", "05-thumbnails.md"]


def read_yaml_lite(path: Path) -> dict:
    """Tiny top-level `key: value` reader — avoids a yaml dependency."""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        m = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def shotlist_summary(path: Path) -> str:
    if not path.exists():
        return "_No shotlist generated yet._"
    d = json.loads(path.read_text())
    chapters = d.get("chapters", [])
    n_scenes = sum(len(c.get("scenes", [])) for c in chapters)
    total_s = sum(c.get("duration_s", 0) for c in chapters)
    cast = ", ".join(c.get("id", "?") for c in d.get("characters", [])) or "—"
    lines = [
        f"- **Chapters:** {len(chapters)}  ·  **Scenes:** {n_scenes}  ·  "
        f"**Runtime (storyboarded):** {total_s // 60}:{total_s % 60:02d}",
        f"- **Cast:** {cast}",
        f"- **Aspect ratio:** {d.get('aspect_ratio', '—')}  ·  "
        f"**Image model:** {d.get('models', {}).get('image', '—')}  ·  "
        f"**Video model:** {d.get('models', {}).get('video', '—')}",
    ]
    return "\n".join(lines)


def build_markdown(ep_dir: Path) -> str:
    meta = read_yaml_lite(ep_dir / "episode.yaml")
    title = meta.get("title", ep_dir.name)
    parts = [
        f"# {title}",
        "",
        f"**Channel:** {meta.get('channel', '—')}  ·  **Episode:** `{ep_dir.name}`",
        "",
        f"**Subject:** {meta.get('subject', '—')}",
        "",
        f"**Target:** {meta.get('duration_minutes', '—')} min "
        f"(~{meta.get('target_words', '—')} words)  ·  "
        f"**Status:** {meta.get('status', '—')}  ·  **Ending:** {meta.get('ending_type', '—')}",
        "",
        "## Production summary",
        shotlist_summary(ep_dir / "production" / "shotlist.json"),
        "",
        "---",
        "",
    ]
    for fname in SECTIONS:
        fpath = ep_dir / fname
        if not fpath.exists():
            continue
        body = fpath.read_text().strip()
        # demote the file's own H1 so the cover title stays the document title
        body = re.sub(r"^#\s+", "## ", body, count=1, flags=re.MULTILINE)
        parts.append(body)
        parts.append("\n\n---\n")
    return "\n".join(parts).rstrip() + "\n"


def md_to_html(md: str, title: str) -> str:
    """Minimal, dependency-free Markdown → HTML for the printable bundle."""
    out: list[str] = []
    in_code = in_table = False
    for raw in md.splitlines():
        line = raw.rstrip("\n")
        if line.strip().startswith("```"):
            if in_code:
                out.append("</pre>"); in_code = False
            else:
                out.append('<pre class="code">'); in_code = True
            continue
        if in_code:
            out.append(html.escape(line)); continue

        if line.startswith("|") and "|" in line[1:]:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue  # table divider row
            if not in_table:
                out.append("<table>"); in_table = True
            tag = "td"
            out.append("<tr>" + "".join(f"<{tag}>{inline(c)}</{tag}>" for c in cells) + "</tr>")
            continue
        elif in_table:
            out.append("</table>"); in_table = False

        if not line.strip():
            out.append(""); continue
        if line.startswith("#### "):
            out.append(f"<h4>{inline(line[5:])}</h4>")
        elif line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.strip() in ("---", "***"):
            out.append("<hr/>")
        elif re.match(r"^[-*]\s+", line):
            item = re.sub(r"^[-*]\s+", "", line)
            out.append(f"<li>{inline(item)}</li>")
        elif re.match(r"^>\s?", line):
            quote = re.sub(r"^>\s?", "", line)
            out.append(f"<blockquote>{inline(quote)}</blockquote>")
        else:
            out.append(f"<p>{inline(line)}</p>")
    if in_table:
        out.append("</table>")

    # wrap consecutive <li> into <ul>
    body = "\n".join(out)
    body = re.sub(r"(?:<li>.*?</li>\n?)+", lambda m: f"<ul>{m.group(0)}</ul>", body, flags=re.S)

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html.escape(title)}</title>
<style>
  :root {{ --red:#e23; --ink:#111; --muted:#666; --line:#ddd; }}
  body {{ font: 16px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
         color: var(--ink); max-width: 820px; margin: 40px auto; padding: 0 24px; }}
  h1 {{ font-size: 2.1rem; border-bottom: 3px solid var(--red); padding-bottom: .3em; }}
  h2 {{ font-size: 1.45rem; margin-top: 2em; border-bottom: 1px solid var(--line); padding-bottom:.2em; }}
  h3 {{ font-size: 1.12rem; color:#222; margin-top: 1.4em; }}
  h4 {{ font-size: 1rem; color: var(--muted); text-transform: uppercase; letter-spacing:.04em; }}
  pre.code {{ background:#0e0e10; color:#e8e8ea; padding:14px 16px; border-radius:8px;
             overflow-x:auto; font:13px/1.5 ui-monospace,Menlo,Consolas,monospace; white-space:pre-wrap; }}
  blockquote {{ border-left:3px solid var(--red); margin:1em 0; padding:.2em 1em; color:var(--muted); background:#fafafa; }}
  table {{ border-collapse:collapse; width:100%; margin:1em 0; font-size:.92rem; }}
  td {{ border:1px solid var(--line); padding:6px 10px; vertical-align:top; }}
  hr {{ border:0; border-top:1px solid var(--line); margin:2em 0; }}
  ul {{ margin:.4em 0 .8em 1.2em; }}
  code {{ background:#f2f2f4; padding:.1em .35em; border-radius:4px; font-size:.9em; }}
  @media print {{ body {{ margin:0; max-width:none; }} pre.code {{ white-space:pre-wrap; }} }}
</style></head><body>
{body}
</body></html>
"""


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    return s


def main() -> int:
    args = sys.argv[1:]
    if len(args) == 1:
        ep_dir = (ROOT / args[0]).resolve()
    elif len(args) == 2:
        ep_dir = (ROOT / "channels" / args[0] / "episodes" / args[1]).resolve()
    else:
        print(__doc__)
        return 1
    if not (ep_dir / "episode.yaml").exists():
        print(f"error: {ep_dir}/episode.yaml not found", file=sys.stderr)
        return 1

    meta = read_yaml_lite(ep_dir / "episode.yaml")
    title = meta.get("title", ep_dir.name)
    md = build_markdown(ep_dir)
    out_dir = ep_dir / "export"
    out_dir.mkdir(exist_ok=True)
    md_path = out_dir / f"{ep_dir.name}.md"
    html_path = out_dir / f"{ep_dir.name}.html"
    md_path.write_text(md)
    html_path.write_text(md_to_html(md, title))
    print(f"wrote {md_path.relative_to(ROOT)}")
    print(f"wrote {html_path.relative_to(ROOT)}  (open in a browser → Print → Save as PDF)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
