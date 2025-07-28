# 🧠 Adobe Hackathon 2025 - Round 1A

---

## 📝 Problem Statement

Given a collection of unstructured PDF documents, extract a **structured outline** in the form of:
- **Document Title**
- **Headings** categorized as H1, H2, H3

The solution must:
- Run **completely offline** (no internet access)
- Be Dockerized
- Handle multiple PDF files
- Output structured **JSON files** for each PDF

---

## 💡 Solution Overview

- Uses **PyMuPDF (`fitz`)** to parse PDFs offline.
- Extracts **text spans with font sizes and positions**.
- Detects heading levels using **font-size clustering**:
  - Highest font sizes are mapped to **H1**, **H2**, **H3**.
- Infers **document title** from the largest text element found on the first 1–2 pages.
- Outputs structured JSON files with:
  - `"title"`: Document title
  - `"outline"`: List of headings with `"heading"` and `"level"`

---

## 📁 Folder Structure

```
AdobeHackathonProject/
├── app/
│   ├── input/                  # Input PDFs go here
│   └── output/                 # Output JSONs will be saved here
├── src/
│   ├── extract_structure.py    # Core logic for PDF parsing and heading extraction
│   ├── heading_logic.py        # Heading detection, TOC alignment, etc.
│   └── utils.py                # Utility functions (e.g. cleaning, file ops, logging)
├── main.py                     # Entry point for PDF batch processing
├── requirements.txt            # Required Python packages
├── Dockerfile                  # For building offline-compatible image
├── .dockerignore               # Prevents unnecessary file copies into Docker image
├── .gitignore                  # Ignore rules for Git
└── README.md                   # This file

```

---

## 📥 Input JSON Format

**No input JSON needed.**  
You only need to drop PDF files into the `app/input/` folder.

---

## 📤 Output JSON Format

Each PDF generates a corresponding JSON with the following structure:

```json
{
  "title": "Understanding AI Systems",
  "outline": [
    { "heading": "1. Introduction", "level": "H1" },
    { "heading": "1.1 What is AI?", "level": "H2" },
    { "heading": "1.2 History", "level": "H2" },
    { "heading": "2. Applications", "level": "H1" },
    { "heading": "2.1 Healthcare", "level": "H2" },
    { "heading": "2.1.1 Diagnostics", "level": "H3" }
  ]
}
```

---

## 🐳 Running the Project with Docker

### ✅ Step 1: Build the Docker Image

```bash
docker build --platform=linux/amd64 -t pdf-outline-extractor .
```

### ▶️ Step 2: Run the Container

#### On Linux/macOS (bash, zsh):

```bash
docker run --rm \
  -v "$(pwd)/app/input:/app/input" \
  -v "$(pwd)/app/output:/app/output" \
  --network none \
  pdf-outline-extractor
```

#### On Windows (PowerShell):
```bash
docker run --rm -v "$(pwd)/app/input:/app/input" -v "$(pwd)/app/output:/app/output" --network none pdf-outline-extractor
```

> ℹ️ The container runs **completely offline**. Ensure your `input/` folder contains PDFs before running.

---

## 📦 Dependencies

Declared in `requirements.txt`:

```
torch==2.1.2
sentence-transformers==2.6.1
numpy==1.24.4
pandas==1.5.3
scikit-learn==1.2.2
PyMuPDF==1.23.7

```

Install locally using:

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing Your Setup

After building the image and adding PDFs to `app/input`, run the container. Check `app/output/` for the extracted `.json` files.

If no output is generated, verify:
- The PDF files are valid
- You’re mounting the correct folder
- Logs are printing any issues (check console)

---

## 📚 Example Collections

Place your test PDFs in:

```
app/input/
├── ai_research.pdf
├── machine_learning_basics.pdf
```

After running the container, you’ll get:

```
app/output/
├── ai_research.json
├── machine_learning_basics.json
```

Each `.json` file contains structured heading outlines.

---

## 👩‍💻 Author

Salusha — Participant, Adobe Hackathon 2025  
GitHub: [https://github.com/salusha](https://github.com/salusha)

Snehal Taori — Participant, Adobe Hackathon 2025  
GitHub: [https://github.com/snehaltaori](https://github.com/snehaltaori)

Deepanshi Verma — Participant, Adobe Hackathon 2025  
GitHub: [https://github.com/DeepanshiiVerma](https://github.com/DeepanshiiVerma)

---

> 📌 Built for Adobe Hackathon 2025 — Round 1A
