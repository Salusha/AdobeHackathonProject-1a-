# import os
# import json
# from src.extractor import extract_outline

# # INPUT_DIR = "/app/input"
# # OUTPUT_DIR = "/app/output"
# if os.path.exists("/app/input") and os.path.exists("/app/output"):
#     INPUT_DIR = "/app/input"
#     OUTPUT_DIR = "/app/output"
# else:
#     INPUT_DIR = "input"
#     OUTPUT_DIR = "output"

# def main():
#     for filename in os.listdir(INPUT_DIR):
#         if filename.endswith(".pdf"):
#             pdf_path = os.path.join(INPUT_DIR, filename)
#             result = extract_outline(pdf_path)
#             output_filename = os.path.splitext(filename)[0] + ".json"
#             output_path = os.path.join(OUTPUT_DIR, output_filename)

#             with open(output_path, "w", encoding="utf-8") as f:
#                 json.dump(result, f, indent=2, ensure_ascii=False)

# if __name__ == "__main__":
#     main()


import os
import json
from src.extractor import extract_outline

# Detect environment (Docker vs Local)
if os.path.exists("/app/input") and os.path.exists("/app/output"):
    INPUT_DIR = "/app/input"
    OUTPUT_DIR = "/app/output"
else:
    INPUT_DIR = os.path.join("app", "input")
    OUTPUT_DIR = os.path.join("app", "output")

def main():
    # Check input directory exists
    if not os.path.exists(INPUT_DIR):
        raise FileNotFoundError(f"Input directory not found: {INPUT_DIR}")

    # Create output directory if not exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not files:
        print(f"No PDF files found in {INPUT_DIR}")
        return

    for filename in files:
        try:
            pdf_path = os.path.join(INPUT_DIR, filename)
            print(f"Processing: {filename}")
            result = extract_outline(pdf_path)

            output_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            print(f"Saved: {output_filename} ✅")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

if __name__ == "__main__":
    main()
