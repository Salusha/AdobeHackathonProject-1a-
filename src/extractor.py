import fitz  # PyMuPDF

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_stats = {}
    headings = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    size = round(span["size"])
                    font = span["font"]

                    if not text or len(text) < 3: continue
                    if size not in font_stats:
                        font_stats[size] = 0
                    font_stats[size] += 1

    # Estimate top 3 font sizes used for headings
    sizes = sorted(font_stats.items(), key=lambda x: -x[1])
    heading_sizes = [s[0] for s in sizes[:3]]

    level_map = {heading_sizes[0]: "H1"}
    if len(heading_sizes) > 1:
        level_map[heading_sizes[1]] = "H2"
    if len(heading_sizes) > 2:
        level_map[heading_sizes[2]] = "H3"

    outline = []
    doc_title = None

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    size = round(span["size"])

                    if not text or len(text) < 3:
                        continue

                    if size in level_map:
                        level = level_map[size]
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num
                        })
                    
                    # Heuristic for title
                    if not doc_title and size == max(heading_sizes):
                        doc_title = text

    return {
        "title": doc_title or "Untitled Document",
        "outline": outline
    }
