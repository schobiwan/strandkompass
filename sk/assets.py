# -*- coding: utf-8 -*-
"""Schriften, Fotos, CSS und JS bündeln, Sitemap schreiben."""
import os, shutil, subprocess, datetime
from .core import *
from .icons import FAVICON

TOOLS = os.path.join(ROOT, "node_modules", ".bin")

SAFELIST = ["now", "open", "calm", "scrolled", "clear", "fcount", "pk"]

def build_assets():
    from PIL import Image
    write("favicon.svg", FAVICON)
    shutil.copytree(os.path.join(ROOT, "fonts"), os.path.join(OUT, "fonts"), dirs_exist_ok=True)
    os.makedirs(os.path.join(OUT, "photos"), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "photos")):
        if f.endswith(".webp"):
            shutil.copy(os.path.join(ROOT, "photos", f), os.path.join(OUT, "photos", f))
    # Vorschaubild für soziale Netzwerke (1.91:1)
    im = Image.open(os.path.join(ROOT, "photos_src", "sk-og.jpg")).convert("RGB")
    w, h = im.size; th = round(w / 1.91); y = (h - th) // 2
    im.crop((0, y, w, y + th)).save(os.path.join(OUT, "photos", "og.jpg"), quality=80, optimize=True, progressive=True)

def finalize():
    """CSS entschlacken und minifizieren, JS bündeln, Sitemap schreiben."""
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    css_src = os.path.join(OUT, "assets", "_full.css")
    with open(css_src, "w", encoding="utf-8") as f:
        f.write(open(os.path.join(ROOT, "src", "css", "base.css"), encoding="utf-8").read() + open(os.path.join(ROOT, "src", "css", "extra.css"), encoding="utf-8").read())
    purged = os.path.join(OUT, "assets", "_purged.css")
    subprocess.run([os.path.join(TOOLS, "purgecss"), "--css", css_src, "--content", f"{OUT}/**/*.html", f"{ROOT}/src/js/*.js",
                    "--safelist", *SAFELIST, "--output", purged], check=True)
    subprocess.run([os.path.join(TOOLS, "lightningcss"), "--minify", "--targets", ">= 0.5%", purged, "-o", os.path.join(OUT, "assets", "site.css")], check=True)
    os.remove(css_src); os.remove(purged)
    for f in os.listdir(os.path.join(OUT, "assets")):
        if f.endswith(".js"):
            os.remove(os.path.join(OUT, "assets", f))
    entries = [os.path.join(ROOT, "src", "js", f) for f in ("app.js", "home.js")]
    subprocess.run([os.path.join(TOOLS, "esbuild"), *entries, "--bundle", "--format=esm", "--minify", "--target=es2020",
                    "--legal-comments=none", f"--outdir={os.path.join(OUT, 'assets')}", "--log-level=warning"], check=True)
    urls = []
    for d, _, fs in os.walk(OUT):
        for f in fs:
            if f == "index.html":
                rel = os.path.relpath(os.path.join(d, f), OUT).replace(os.sep, "/")
                urls.append(DOMAIN + "/" + rel[:-len("index.html")])
    urls.sort(key=lambda u: (u.count("/"), u))
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    # Zeitpunkt des Builds, um zu prüfen, ob die Live-Seite aktuell ist
    write("version.txt", datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + "\n")
