import glob, os, re
os.chdir("/cluster/embryo-webtools/pdf")
pages = {os.path.splitext(f)[0] for f in glob.glob("*.html")}
n = 0
for f in glob.glob("*.html"):
    s = open(f, encoding="utf-8").read(); o = s
    s = re.sub(r'(src|href)="/(assets|images|js|css|fonts|locales|wasm|static)/', r'\1="\2/', s)
    s = re.sub(r'(src|href)="/(favicon[^"]*|manifest[^"]*|[^"/]+\.(?:png|svg|ico|webmanifest|json|js|css))"', r'\1="\2"', s)
    def page(m):
        p = m.group(1).strip("/").split("#")[0].split("?")[0]
        if p == "":
            return 'href="index.html"'
        return f'href="{p}.html"' if p in pages else m.group(0)
    s = re.sub(r'href="(/[a-z0-9\-/]*)"', page, s)
    if s != o:
        open(f, "w", encoding="utf-8").write(s); n += 1
print(n, "pages fixed")
# leftover upstream links (blog, home anchor, paid products) -> ours or nowhere
blog = "blog/index.html" if os.path.exists("blog/index.html") else "index.html"
for f in glob.glob("*.html"):
    s = open(f, encoding="utf-8").read(); o = s
    s = s.replace('href="/blog"', f'href="{blog}"').replace('href="/#tools-header"', 'href="index.html#tools-header"')
    s = s.replace('href="/index.html#tools-header"', 'href="index.html#tools-header"')
    s = re.sub(r'href="/(kura|hyper-compress|licensing)#[a-z-]*"', 'href="#"', s)
    if s != o:
        open(f, "w", encoding="utf-8").write(s)
print("absolute links left:", sum(open(f, encoding="utf-8").read().count('href="/') for f in glob.glob("*.html")))
# 2026-11-16: vite builds tool pages two folders deep and they are moved to the top, leaving "../../assets/..."
# links; rewrite every "../" chain that points at a top-level folder/file to the right depth for that page.
tops = set(os.listdir("."))
fixed = 0
for f in glob.glob("**/*.html", recursive=True):
    depth = f.count("/"); pre = "../" * depth if depth else "./"
    s = open(f, encoding="utf-8").read(); o = s
    def fix(m):
        attr, target = m.group(1), m.group(3)
        first = target.split("/")[0].split("?")[0].split("#")[0]
        return f'{attr}="{pre}{target}"' if first in tops else m.group(0)
    s = re.sub(r'(src|href)="((?:\.\./)+)([^"]+)"', fix, s)
    if s != o:
        open(f, "w", encoding="utf-8").write(s); fixed += 1
print("depth-fixed pages:", fixed)
