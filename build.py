#!/usr/bin/env python3
import os, shutil, re, sys
from pathlib import Path
from datetime import datetime
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown

ROOT = Path(__file__).parent
PROJECTS = ROOT / "projects"
TEMPLATES = ROOT / "templates"
SITE = ROOT / "site"
ASSETS = ROOT / "assets"

def slugify(text):
    t = re.sub(r"[^a-zA-Z0-9\-]+", "-", text.strip().lower())
    t = re.sub(r"-+", "-", t).strip("-")
    return t or "proj"

def read_project_dir(pdir: Path):
    meta_path = pdir / "meta.yml"
    summary_md = pdir / "summary.md"
    if not meta_path.exists() or not summary_md.exists():
        return None
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    # normalize
    meta["id"] = str(meta.get("id", pdir.name)).strip()
    meta["title"] = meta.get("title","Projeto sem título").strip()
    meta["topic"] = meta.get("topic","Geral").strip()
    meta["ods"] = list(meta.get("ods", []))
    meta["type"] = meta.get("type","web-static").strip()
    meta["date"] = meta.get("date","")
    meta["leaders"] = list(meta.get("leaders", []))
    meta["team"] = list(meta.get("team", []))
    meta["repo_url"] = meta.get("repo_url","")
    meta["demo_url"] = meta.get("demo_url","")
    meta["tags"] = list(meta.get("tags", []))

    slug = slugify(meta["id"] + "-" + meta["title"])
    # markdown → html
    summary_html = markdown.markdown(summary_md.read_text(encoding="utf-8"), extensions=["extra"])
    return {"dir": pdir, "meta": meta, "slug": slug, "summary_html": summary_html}

def copy_assets_for_project(p, dest_dir: Path):
    src_assets = p["dir"] / "assets"
    if src_assets.exists():
        shutil.copytree(src_assets, dest_dir / "assets", dirs_exist_ok=True)

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir(parents=True)

    # copy global assets
    shutil.copytree(ASSETS, SITE / "assets", dirs_exist_ok=True)

    # load projects
    projects = []
    for pdir in sorted(PROJECTS.iterdir() if PROJECTS.exists() else [], key=lambda x: x.name.lower()):
        if not pdir.is_dir(): continue
        p = read_project_dir(pdir)
        if p: projects.append(p)

    # sort by date desc then title
    def sort_key(p):
        d = p["meta"].get("date","")
        try:
            dt = datetime.fromisoformat(d)
        except Exception:
            dt = datetime.min
        return (-int(dt.timestamp()), p["meta"]["title"].lower())

    projects.sort(key=sort_key)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(['html', 'xml'])
    )

    # render index
    tpl_index = env.get_template("index.html.j2")
    (SITE / "index.html").write_text(tpl_index.render(projects=[x["meta"] | {"slug": x["slug"]} for x in projects]), encoding="utf-8")

    # render each project
    tpl_proj = env.get_template("project.html.j2")
    for p in projects:
        pdir = SITE / "projects" / p["slug"]
        pdir.mkdir(parents=True, exist_ok=True)
        copy_assets_for_project(p, pdir)
        html = tpl_proj.render(meta=p["meta"], summary_html=p["summary_html"])
        (pdir / "index.html").write_text(html, encoding="utf-8")

    print(f"Built {len(projects)} project(s) into {SITE}")

if __name__ == "__main__":
    main()
