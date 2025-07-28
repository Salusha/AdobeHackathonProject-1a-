import re

def normalize_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def detect_heading_level(text):
    text = text.strip()
    if re.match(r'^\d+\.\d+', text): return "H2"
    if re.match(r'^\d+\.', text): return "H1"
    return None

def looks_like_table_entry(text):
    return len(text.split()) <= 5 and (
        text.isupper() or re.match(r'^[\d\s\-:/().,]+$', text)
    )

def is_noise(text):
    if not text or len(text) < 3:
        return True
    if re.fullmatch(r'[\W\d\s]+', text):
        return True
    if re.search(r'\b\d{4}\b', text):
        return True
    if re.search(r'\.{3,}', text) or re.search(r'\bpage\s*\d+', text.lower()):
        return True
    return False

def extract_multiline_title(df):
    title_lines = []
    first_page = df[df['page'] == 0]
    if first_page.empty:
        return ""

    max_font = first_page['font_size'].max()
    font_threshold = max_font * 0.9

    x_min, x_max = first_page['x'].min(), first_page['x'].max()
    y_min, y_max = first_page['y'].min(), first_page['y'].max()

    x_center_min = x_min + (x_max - x_min) * 0.25
    x_center_max = x_min + (x_max - x_min) * 0.75
    y_top = y_min + (y_max - y_min) * 0.4

    top_lines = first_page[
        (first_page['font_size'] >= font_threshold) &
        (first_page['x'].between(x_center_min, x_center_max)) &
        (first_page['y'] >= y_top)
    ].sort_values(by='y', ascending=False)

    for _, row in top_lines.iterrows():
        text = normalize_text(row['text'])
        if text.lower() not in {"overview", "page", "version"} and len(text.split()) < 15:
            title_lines.append(text)

    return normalize_text(" ".join(title_lines)) if title_lines else ""

def extract_outline(df):
    df = df.sort_values(by=['page', 'font_size', 'y'], ascending=[True, False, False]).copy()
    font_max = df['font_size'].max()
    font_q95 = df['font_size'].quantile(0.95)
    font_q50 = df['font_size'].quantile(0.5)

    title = extract_multiline_title(df)

    merged_headings = []
    prev_row = None

    for _, row in df.iterrows():
        text = normalize_text(row['text'])
        if is_noise(text): continue
        if row['font_size'] < 12: continue
        if looks_like_table_entry(text): continue
        if len(text.split()) > 10 and not text.strip().endswith(':') and not re.match(r'^[A-Z\s]+$', text):
            continue

        if prev_row is not None and abs(prev_row['y'] - row['y']) < 5 and prev_row['page'] == row['page']:
            if row['font_size'] == prev_row['font_size'] and len(merged_headings[-1]['text'].split()) < 15:
                merged_headings[-1]['text'] += ' ' + text
                continue
        else:
            merged_headings.append({
                'text': text,
                'page': int(row['page']),
                'font_size': row['font_size'],
                'y': row['y']
            })
            prev_row = row

    seen = set()
    outline = []

    for h in merged_headings:
        text = normalize_text(h['text'])
        if text.lower() in seen or (title and text.lower() in title.lower()):
            continue
        seen.add(text.lower())

        if title and text.lower() == title.lower() and len(outline) > 0:
            continue

        level = detect_heading_level(text)
        if not level:
            if h['font_size'] >= font_q95:
                level = "H1"
            elif h['font_size'] >= font_q50:
                level = "H2"
            else:
                continue

        outline.append({
            "level": level,
            "text": text,
            "page": h["page"]
        })

    return {"title": title or "", "outline": outline}
