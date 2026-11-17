#!/bin/bash
# Embryo PDF full build + install (2026-11-16). Everything served from our own server: PDF engines (AGPL),
# editor fallback fonts (Noto, OFL-1.1), OCR engine (tesseract.js, Apache-2.0) and 102 OCR languages.
set -e
B=/cluster/build/pdf; T=/cluster/embryo-webtools/pdf
cd $B
python3 - <<'PY'
p = "src/js/utils/tesseract-runtime.ts"; s = open(p).read()
old = "  return trimmed.replace(/\\/+$/, '');\n}"
new = ("  // Embryo PDF: \"./ocr/...\" is made absolute from the page, so the OCR worker gets full addresses\n"
       "  const abs = trimmed.startsWith('./') && typeof self !== 'undefined' && self.location\n"
       "    ? new URL(trimmed, self.location.href).href : trimmed;\n"
       "  return abs.replace(/\\/+$/, '');\n}")
if "Embryo PDF: \"./ocr" not in s:
    assert s.count(old) == 2, s.count(old); s = s.replace(old, new); open(p, "w").write(s)
PY
cat > .env.production.local <<E2
VITE_WASM_PYMUPDF_URL=./wasm/pymupdf/
VITE_WASM_GS_URL=./wasm/gs/assets/
VITE_WASM_CPDF_URL=./wasm/cpdf/dist/
VITE_TESSERACT_WORKER_URL=./ocr/worker.min.js
VITE_TESSERACT_CORE_URL=./ocr/core/
VITE_TESSERACT_LANG_URL=./ocr/lang/
E2
export NODE_OPTIONS=--max-old-space-size=3072
nice -n 10 node scripts/generate-blog.mjs > /cluster/build/pdf3.log 2>&1
nice -n 10 node scripts/generate-static-tool-links.mjs >> /cluster/build/pdf3.log 2>&1
rm -rf dist && nice -n 10 npx vite build --base ./ >> /cluster/build/pdf3.log 2>&1
cp -r /cluster/build/wasm dist/wasm && ln -sfn ../wasm dist/assets/wasm
mkdir -p dist/ocr/core dist/ocr/lang
cp node_modules/tesseract.js/dist/worker.min.js node_modules/tesseract.js/dist/worker.min.js.LICENSE.txt dist/ocr/
cp node_modules/tesseract.js-core/*.js node_modules/tesseract.js-core/*.wasm node_modules/tesseract.js-core/LICENSE dist/ocr/core/
cp /cluster/build/ocr-lang/* dist/ocr/lang/
cp node_modules/tesseract.js/LICENSE* dist/ocr/ 2>/dev/null || true
rsync -a --delete dist/ $T/
cp LICENSE LEGAL.md $T/ 2>/dev/null || true
cp /cluster/embryo-webtools/pdf-sw.js $T/sw.js
python3 /cluster/embryo-webtools/relpdf.py
python3 /cluster/embryo-webtools/brand_webtools.py
for f in $T/assets/*.js; do cp "$f" /tmp/c_pdf.mjs; node --check /tmp/c_pdf.mjs || { echo "BROKEN $f"; exit 1; }; done
echo "INSTALLED: jsdelivr addresses left in code: $(grep -l jsdelivr $T/assets/*.js | wc -l) files (unused defaults)"
