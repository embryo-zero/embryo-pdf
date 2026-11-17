#!/usr/bin/env python3
"""Embryo branding for the forked browser tools in /cluster/embryo-webtools (2026-11-16, owner: "it doesn't show our
stuff, our name and our font"). Run after every build/install. Visible names -> ours, our logo, our app font; one small
"based on X (license)" credit per tool stays (license duty; AGPL tools link to our source). Internal identifiers,
file formats and storage keys are not touched so nothing breaks. Safe to run again."""
import base64, glob, os, re, shutil
W = "/cluster/embryo-webtools"
ICON = "/cluster/embryo-zero/beta_icons/beta-icon-512.png"
FONT = 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif'
MARK = "/* embryo-brand */"

def rw(path, fn):
    s = open(path, encoding="utf-8", errors="surrogateescape").read(); t = fn(s)
    if t != s:
        open(path, "w", encoding="utf-8", errors="surrogateescape").write(t); return 1
    return 0

def inject(html, ours, based, lic, src, extra_css=""):
    def f(s):
        if MARK in s: return s
        css = (f"<style>{MARK}\nhtml,body,button,input,select,textarea{{font-family:{FONT} !important}}\n{extra_css}\n"
               ".embryo-credit{position:fixed;right:6px;bottom:4px;z-index:99999;font:11px " + FONT + ";opacity:.55;"
               "background:rgba(255,255,255,.75);color:#333;padding:1px 6px;border-radius:6px;pointer-events:auto}"
               ".embryo-credit a{color:inherit}</style>")
        credit = (f'<div class="embryo-credit">{ours} · based on {based} ({lic})'
                  + (f' · <a href="{src}" target="_blank" rel="noopener">source</a>' if src else "") + "</div>")
        s = s.replace("</head>", css + "</head>", 1) if "</head>" in s else css + s
        return s.replace("</body>", credit + "</body>", 1) if "</body>" in s else s + credit
    return rw(html, f)

def icons(d, names):
    png = open(ICON, "rb").read(); n = 0
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><image width="512" height="512" href="data:image/png;base64,'
           + base64.b64encode(png).decode() + '"/></svg>')
    shutil.copy(ICON, f"{d}/embryo-logo.png")
    for pat in names:
        for p in glob.glob(f"{d}/{pat}", recursive=True):
            if p.endswith(".svg"): open(p, "w").write(svg)
            elif p.endswith((".png", ".ico")): shutil.copy(ICON, p)
            n += 1
    return n

def in_strings(path, old, new, skip=r"$^"):
    """replace `old` only inside quoted string literals that read like text (have a space) or are exactly `old`."""
    def f(s):
        def lit(m):
            q, body = m.group(1), m.group(2)
            if old not in body or re.search(skip, body): return m.group(0)
            if " " not in body and body != old: return m.group(0)
            return q + body.replace(old, new) + q
        return re.sub(r'(["`])((?:\\.|(?!\1)[^\\\n]){0,400}?)\1', lit, s)
    return rw(path, f)

# ---- Embryo PDF (BentoPDF, AGPL) ----
d = f"{W}/pdf"; n = 0
for p in glob.glob(f"{d}/**/*.html", recursive=True):
    n += rw(p, lambda s: s.replace("Love BentoPDF? Help us keep it free and open source!", "Embryo PDF is based on BentoPDF, a free open-source project.")
            .replace("based on BentoPDF", "based on BENTO_KEEP").replace("BentoPDF", "Embryo PDF").replace("BENTO_KEEP", "BentoPDF")
            .replace("bentopdf.com", "embryo-zero.github.io"))
    inject(p, "Embryo PDF", "BentoPDF", "AGPL-3.0", "https://github.com/embryo-zero/embryo-pdf")
for p in glob.glob(f"{d}/assets/*.js"):
    n += in_strings(p, "BentoPDF", "Embryo PDF")
print("pdf: files changed", n, "icons", icons(d, ["images/favicon*", "images/apple-touch-icon.png", "favicon*", "images/bentopdf-tools.png"]))

# ---- Embryo Whiteboard (Excalidraw, MIT) ----
d = f"{W}/whiteboard"; n = 0
skip = r"Context|API|Error|Lib|excalidraw\.com|\+|mermaid|Excalidraw[A-Z]"
for p in glob.glob(f"{d}/assets/locales/*.js"):   # only the language files: editing the minified main bundle broke it (2026-11-16)
    n += in_strings(p, "Excalidraw", "Embryo Whiteboard", skip)
css = (".ExcalidrawLogo-icon,.ExcalidrawLogo-text{display:none !important}"
       ".ExcalidrawLogo::before{content:'';display:inline-block;width:44px;height:44px;margin-right:10px;vertical-align:middle;"
       "background:url(embryo-logo.png) center/contain no-repeat}"
       ".ExcalidrawLogo::after{content:'Embryo Whiteboard';font:700 28px " + FONT + ";vertical-align:middle}"
       "a[href*='plus.excalidraw.com'],a[href*='app.excalidraw.com']{display:none !important}")
inject(f"{d}/index.html", "Embryo Whiteboard", "Excalidraw", "MIT", "https://github.com/embryo-zero/embryo-whiteboard", css)
print("whiteboard: files changed", n, "icons", icons(d, ["favicon*", "apple-touch-icon*", "*.ico", "android-chrome*"]))

# ---- Embryo Diagrams (draw.io, Apache-2.0) ----
d = f"{W}/diagrams"; n = 0
rx = re.compile(r"(?<![\w./@-])draw\.io(?![\w/-])")
for p in glob.glob(f"{d}/resources/dia*.txt"):
    n += rw(p, lambda s: rx.sub("Embryo Diagrams", s))
for p in glob.glob(f"{d}/*.html"):
    n += rw(p, lambda s: re.sub(r"(<title>|>)([^<]*?)(?<![\w./@-])draw\.io(?![\w/-])", r"\1\2Embryo Diagrams", s.replace("based on draw.io", "based on DIO_KEEP")).replace("based on DIO_KEEP", "based on draw.io"))
inject(f"{d}/index.html", "Embryo Diagrams", "draw.io", "Apache-2.0", "https://github.com/embryo-zero/embryo-diagrams")
print("diagrams: files changed", n, "icons", icons(d, ["favicon*", "images/favicon*", "images/drawlogo*", "images/logo*", "images/apple-touch-icon*"]))

# ---- Embryo Paint (JS Paint, MIT) ----
d = f"{W}/paint-classic"; n = 0
for p in glob.glob(f"{d}/*.html"):
    n += rw(p, lambda s: s.replace("based on JS Paint", "based on JSP_KEEP").replace("JS Paint", "Embryo Paint").replace("JSP_KEEP", "JS Paint"))
for p in glob.glob(f"{d}/src/*.js"):
    if "electron" in p: continue
    n += in_strings(p, "JS Paint", "Embryo Paint")
inject(f"{d}/index.html", "Embryo Paint", "JS Paint by Isaiah Odhner", "MIT", "https://github.com/embryo-zero/embryo-paint")
print("paint: files changed", n, "icons", icons(d, ["favicon*", "images/icons/*.png", "images/icons/*.ico"]))

# ---- 2026-11-16 round 2: Embryo PDF texts that come from its translation files, and upstream-only buttons ----
import json as _json
d = f"{W}/pdf"; n = 0
def _fix(v):
    if isinstance(v, str):
        v = v.replace("Love Embryo PDF? Help us keep it free and open source!", "Embryo PDF is based on BentoPDF, a free open-source project.").replace("Love BentoPDF? Help us keep it free and open source!", "Embryo PDF is based on BentoPDF, a free open-source project.")
        return v.replace("based on BentoPDF", "based on BKEEP").replace("BentoPDF", "Embryo PDF").replace("based on BKEEP", "based on BentoPDF")
    if isinstance(v, dict): return {k: _fix(x) for k, x in v.items()}
    if isinstance(v, list): return [_fix(x) for x in v]
    return v
for p in glob.glob(f"{d}/locales/**/*.json", recursive=True):
    try:
        o = _json.load(open(p, encoding="utf-8")); t = _fix(o)
        if t != o:
            _json.dump(t, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2); n += 1
    except ValueError:
        pass
M2 = "/* embryo-brand-2 */"
HIDE = ("<style>" + M2 + "\na[href*='ko-fi.com'],a[href*='github.com/sponsors'],a[href*='github.com/alam00000'],.nav-products,a[data-i18n='nav.docs'],div:has(> a[href*='ko-fi.com']){display:none !important}</style>")
for p in glob.glob(f"{d}/**/*.html", recursive=True):
    n += rw(p, lambda s: s if M2 in s else s.replace("</head>", HIDE + "</head>", 1))
print("pdf round 2: files changed", n)
# round 2b: keep the self-removing service worker in place after rebuilds
_sw = open("/cluster/embryo-webtools/pdf/sw.js").read()
if "Embryo PDF (2026-11-16): the upstream offline cache is switched off" not in _sw:
    print("WARNING: pdf/sw.js was rebuilt; copy the self-removing worker back (see /cluster/CLAUDE.md)")
# appended to brand_webtools.py: round 3 (2026-11-16)
M3 = "/* embryo-brand-3 */"
CSS3 = ("<style>" + M3 + "\n"
        "h1,h2,h3,h4,h5,h6,p,span,a,button,div,li,label,input,select,textarea,small,b,strong{font-family:" + FONT + " !important}"
        "section:has([data-i18n^='usedBy']){display:none !important}</style>")
n = 0
for p in glob.glob(f"{W}/pdf/**/*.html", recursive=True):
    n += rw(p, lambda s: s if M3 in s else s.replace("</head>", CSS3 + "</head>", 1))
CSS3P = "<style>" + M3 + "\n.window,.menus,.tool,button,.status-area,label{font-family:" + FONT + " !important}</style>"
n += rw(f"{W}/paint-classic/index.html", lambda s: s if M3 in s else s.replace("</head>", CSS3P + "</head>", 1))
print("round 3: files changed", n)
# round 4 (2026-11-16): Embryo PDF display text inside its bundles; Embryo Diagrams logo
n = 0
for p in glob.glob(f"{W}/pdf/assets/*.js"):
    n += rw(p, lambda s: s.replace("based on BentoPDF", "based on BKEEP").replace("BentoPDF", "Embryo PDF").replace("based on BKEEP", "based on BentoPDF"))
M4 = "/* embryo-brand-4 */"
CSS4 = ("<style>" + M4 + "\n.geAppIcon{background-image:url(embryo-logo.png) !important;background-size:contain !important;"
        "background-repeat:no-repeat !important;background-position:center !important}</style>")
n += rw(f"{W}/diagrams/index.html", lambda s: s if M4 in s else s.replace("</head>", CSS4 + "</head>", 1))
print("round 4: files changed", n)
# round 5 (2026-11-16, owner OK "if it's legal to host it ourselves, then yes"): Embryo PDF's fallback fonts (Noto, OFL-1.1)
# served from our server: /cluster/build/embedpdf-fonts -> pdf/embedpdf-fonts, each pack with its own LICENSE (OFL duty).
if os.path.isdir("/cluster/build/embedpdf-fonts"):
    shutil.copytree("/cluster/build/embedpdf-fonts", f"{W}/pdf/embedpdf-fonts", dirs_exist_ok=True)
n = 0
for p in glob.glob(f"{W}/pdf/assets/*.js"):
    n += rw(p, lambda s: s.replace('`https://cdn.jsdelivr.net/npm/@embedpdf`', 'new URL("embedpdf-fonts",self.location.href).href'))
print("round 5: font address changed in", n, "file(s)")
# round 6 (2026-11-16): fonts Embryo PDF embeds into PDFs it makes (27 Noto fonts, OFL-1.1, pinned GitHub commits,
# each repo's LICENSE kept) served from our server; the viewer's Google Fonts import removed (privacy; our app font is used).
if os.path.isdir("/cluster/build/noto"):
    shutil.copytree("/cluster/build/noto", f"{W}/pdf/noto", dirs_exist_ok=True)
    if not os.path.exists(f"{W}/pdf/assets/noto"):
        os.symlink("../noto", f"{W}/pdf/assets/noto")
n = 0
for p in glob.glob(f"{W}/pdf/assets/*.js"):
    n += rw(p, lambda s: s.replace("https://rawcdn.githack.com/googlefonts/", "./noto/")
            .replace("@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');", ""))
print("round 6: files changed", n)
# round 7: the spaced spelling "Bento PDF" (logo labels etc.)
n = 0
for p in glob.glob(f"{W}/pdf/**/*.html", recursive=True):
    n += rw(p, lambda s: s.replace("Bento PDF", "Embryo PDF"))
print("round 7: files changed", n)
