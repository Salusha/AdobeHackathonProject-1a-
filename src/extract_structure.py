import os
import json
from src.utils import extract_text_elements_with_page, classify_by_font_size
from src.heading_logic import extract_outline

def process_pdf(pdf_path, output_path):
    df = extract_text_elements_with_page(pdf_path)
    df = classify_by_font_size(df)
    df = df[df['label'].isin(['Title', 'Heading', 'Subheading'])]
    df = df.sort_values(by=['page', 'y'], ascending=[True, False])
    outline_data = extract_outline(df)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(outline_data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Saved to: {output_path}")

def process_all_pdfs(input_dir="app/input", output_dir="app/output"):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".json")
            print(f"📄 Processing: {filename}")
            process_pdf(input_path, output_path)
