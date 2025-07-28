import os
from src.extract_structure import process_all_pdfs

def main():
    input_dir = "app/input"
    output_dir = "app/output"

    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    print("Starting outline extraction...")
    process_all_pdfs(input_dir, output_dir)
    print("Finished processing all PDFs.")

if __name__ == "__main__":
    main()
