---
name: thesis-defense-ppt
category: productivity
description: Generate thesis defense PPT from DOCX thesis — reads content without python-docx, generates editable PPTX via Node.js pptxgenjs when pip is unavailable. Covers fallback approaches for restricted environments.
---

# Thesis Defense PPT Generator

Generate professional thesis defense presentations from `.docx` thesis files. Handles restricted environments where pip/apt-get are unavailable.

## Prerequisites

- Node.js + npm (usually pre-installed)
- Python 3 (with built-in zipfile + xml.etree.ElementTree — no pip needed)

## Workflow

### Step 1: Extract DOCX Content (without python-docx)

DOCX files are ZIP archives containing XML. Use Python's standard library:

```python
import zipfile, xml.etree.ElementTree as ET

zf = zipfile.ZipFile('thesis.docx')
doc_xml = zf.read('word/document.xml')
root = ET.fromstring(doc_xml)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

texts = []
for para in root.findall('.//w:p', ns):
    p_text = ''
    for t in para.findall('.//w:t', ns):
        if t.text:
            p_text += t.text
    if p_text.strip():
        texts.append(p_text.strip())

# texts[0..N] now contains all paragraphs in order
```

### Step 2: Install pptxgenjs (when pip unavailable)

```bash
mkdir -p /tmp/ppt-gen
cd /tmp/ppt-gen
npm init -y
npm install pptxgenjs
```

### Step 3: Generate PPTX with pptxgenjs

Create a Node.js script that builds slides with `pptxgenjs`:

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// Configure theme
const C = {
  navy: "1A237E",
  medBlue: "3F51B5",
  white: "FFFFFF",
  offWhite: "F5F7FA",
  accent: "FF6F00",
  // ...
};

// Add slides
const slide = pptx.addSlide();
slide.background = { fill: C.offWhite };

// Text
slide.addText("Title", { x: 0.5, y: 0.3, w: 8, h: 0.7, fontSize: 24, bold: true, color: C.navy });

// Rectangles
slide.addShape(pptx.ShapeType.rect, {
  x: 0.5, y: 1.2, w: 4, h: 2, fill: { color: C.white },
  rectRadius: 0.1, shadow: { type: "outer", blur: 6, offset: 2, color: "DDDDDD", opacity: 0.3 }
});

// Export
pptx.writeFile({ fileName: 'output.pptx' })
  .then(() => console.log('Done'))
  .catch(err => console.error(err));
```

### Step 4: Thesis Defense PPT Structure

Recommended 10-slide structure for Chinese university thesis defense:

| Slide | Title | Content |
|-------|-------|---------|
| 1 | 封面 | Title, student name, advisor, university, major |
| 2 | 汇报提纲 | 6-8 section overview with numbered items |
| 3 | 研究背景与意义 | Background + significance (two-column layout) |
| 4 | 设计任务与目标 | Tasks + technical targets/specs table |
| 5 | 系统总体方案设计 | Architecture diagram + control strategy cards |
| 6 | 硬件设计 | PLC selection, sensor specs, electrical design |
| 7 | 软件设计 | IDE, programming language, module listing, flow chart |
| 8 | 系统仿真与调试 | Test scenarios grid (4-quadrant) + HMI overview |
| 9 | 结论与展望 | Summary (left) + outlook (right) |
| 10 | 致谢 | Thank you + invite questions |

## Color Themes for Engineering Theses

| Theme | Primary | Secondary | Accent | Best for |
|-------|---------|-----------|--------|----------|
| Professional Navy | #1A237E | #3F51B5 | #FF6F00 | Electrical/Mechanical/CS |
| Green Tech | #1B5E20 | #388E3C | #FF8F00 | Environmental/Bio |
| Deep Red | #B71C1C | #D32F2F | #FFD600 | Architecture/Civil |
| Purple Academic | #4A148C | #7B1FA2 | #00BCD4 | Science/Math |

## Key Design Principles for Thesis Defense

- Dark background for title + conclusion slides, light for content ("sandwich" structure)
- Use cards/callout boxes for key results (avoid plain bullet lists)
- Technical specs should be in a table or badge layout
- Include a highlight bar at the bottom of each content slide for key takeaway
- Every slide needs a visual element — even a colored accent bar counts
- Use 24pt+ for slide titles, 11-14pt for body text
- Keep text minimal — bullet points, not paragraphs

## Pitfalls

- **Node.js not available** → Fallback: use python-pptx via `pip3 install --user python-pptx` or build XML manually
- **No npm** → Download pptxgenjs from CDN or use python-pptx with `pip3 install --user python-pptx`
- **DOCX has images/tables** → The zipfile XML approach only gets text. For tables, iterate `w:tbl` elements in the XML
- **Large DOCX (>100 paragraphs)** → Read in batches; print indices to find key sections
- **Chinese font rendering** → pptxgenjs embeds font names but doesn't embed font files. Use common system fonts like "Calibri", "Microsoft YaHei"
