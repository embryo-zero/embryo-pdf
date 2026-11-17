# Changes made by Embryo-Zero (Embryo Zero Backyard Data Center Corporation) to BentoPDF

Forked from v2.8.11-22-gcc974294 (commit cc974294) on 2026-11-16. All changes are on the `embryo` branch; `git log` has the full detail.

| Date | Files | Change |
|---|---|---|
| 2026-11-16 | EMBRYO.md, LEGAL.md, CHANGES-EMBRYO.md (new) | Fork notes, legal notes and this list. No original file changed yet. |
| 2026-11-16 | README.md | Embryo name at the top; the original README follows unchanged |
| 2026-11-16 | src/js/utils/wasm-provider.ts, index.html, embryo/ (new) | WASM engines served from our own server (relative ./wasm paths), Embryo PDF name/logo/font and credit line (embryo/brand_webtools.py, run after build), upstream offline cache replaced by a self-removing worker (embryo/sw.js), donate/sponsor/paid-product links hidden |
| 2026-11-16 | src/js/utils/tesseract-runtime.ts, embryo/ | OCR engine, 102 OCR languages and all fonts served from our own server (relative ./ocr, ./noto, ./embedpdf-fonts); Google Fonts import removed; full build+install script embryo/install_pdf.sh |
