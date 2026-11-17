# Legal notes for Embryo PDF

Embryo PDF is a modified version of **BentoPDF** (https://github.com/alam00000/bentopdf), copyright its authors.
License (read from its license file on 2026-11-16): **AGPL-3.0**. Original license files, unchanged: LICENSE, licensing.html.

- `LICENSE`: GNU AFFERO GENERAL PUBLIC LICENSE / Version 3, 19 November 2007 / Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
- `licensing.html`: <!doctype html> / <html lang="en"> / <head>

"BentoPDF" is the original project's name; ours is Embryo PDF, "based on BentoPDF". We do not use their names or logos to promote ours.

## When we offer it to people
- Offer the complete matching source code with any copy we hand out (or a written offer), under the same license.
- Keep the license and all copyright notices; add no extra restrictions.
- Changed files carry a notice and a date (CHANGES-EMBRYO.md).
- AGPL: people who use our changed version over the network (in the apps) must be offered its source: the app shows a link to our repository.
- Bundled third-party parts keep their own licenses: CHECK them before a release.
- What people make with the tool belongs to them; the tool's license does not cover its output.
- No warranty beyond what the license says.

## Parts we serve from our own server (2026-11-16)
- PDF engines: @bentopdf/pymupdf-wasm 0.11.16, @bentopdf/gs-wasm 0.1.1 (AGPL-3.0-only), coherentpdf 2.5.5 (AGPL-3.0-or-later).
- OCR: tesseract.js and tesseract.js-core 7.0.0 (Apache-2.0); 102 language files from @tesseract.js-data/* (MIT packaging,
  tessdata Apache-2.0).
- Fonts: Noto fonts (SIL Open Font License 1.1) from @embedpdf/fonts-* 1.0.0 and googlefonts/noto-fonts @ffebf8c,
  googlefonts/noto-cjk @f8d1575; each set keeps its LICENSE file; the fonts are not changed and not sold on their own.
- The viewer no longer loads Open Sans from Google Fonts (our app font is used instead).
