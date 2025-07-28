# 🚀 Adobe Hackathon 2025 - Round 1A: 

## ✅ Approach

- Used **PyMuPDF** (`fitz`) for fast and accurate PDF parsing.
- Extracted **text spans along with font sizes and positions**.
- Computed a **font size frequency histogram** to determine heading styles:
  - Top 3 most frequent large font sizes → mapped to **H1**, **H2**, and **H3**.
- The **document title** is inferred from the **largest text span** on the first 1–2 pages.
- Outputs a structured JSON with:
  - `"title"`: Title of the document
  - `"outline"`: List of extracted headings with their hierarchy (H1, H2, H3)

---

## 🛠️ Dependencies

- Python 3.10+
- [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/) (`fitz`) — version 1.23.7

Install the dependencies using:

```bash
pip install -r requirements.txt
```

---

## 📂 Directory Structure

```
AdobeHackathonProject/
├── app/
│   ├── input/        # Input PDFs (mounted into Docker)
│   ├── output/       # Output JSONs (mounted into Docker)
├── src/
│   └── extractor.py  # Core logic for heading/title extraction
├── main.py           # Entry point to run outline extraction
├── requirements.txt  # Required Python packages
├── Dockerfile        # Offline Docker image build
└── README.md         # Project documentation
```

---

## 🐳 Build & Run Instructions (Offline Docker)

### 🔨 Step 1: Build the Docker Image

```bash
docker build --platform linux/amd64 -t pdfextractor:round1a .
```

### 🚀 Step 2: Run the Container

```bash
docker run --rm \
  -v $(pwd)/app/input:/app/input \
  -v $(pwd)/app/output:/app/output \
  --network none \
  pdfextractor:round1a
```

> 📌 This runs completely **offline** (as per Round 1A requirements).

---

## 📥 Input Format

Place all your `.pdf` files inside the `app/input/` directory.

---

## 📤 Output Format

Each PDF file will produce a corresponding `.json` file in `app/output/` with the following structure:

```json
{
  "title": "Understanding AI Systems",
  "outline": [
    { "heading": "1. Introduction", "level": "H1" },
    { "heading": "1.1 What is AI?", "level": "H2" },
    { "heading": "2. Applications", "level": "H1" },
    { "heading": "2.1 Healthcare", "level": "H2" },
    { "heading": "2.1.1 Diagnostics", "level": "H3" }
  ]
}
```

---

## ✅ Features

- ✅ Accurate outline extraction using font size logic
- ✅ Handles multiple PDFs in one run
- ✅ Fully offline, Dockerized solution
- ✅ Fast processing even for large PDFs
- ✅ Clean and structured JSON output

---

## 👩‍💻 Author

Salusha — Participant, Adobe Hackathon 2025  
GitHub: [https://github.com/salusha](https://github.com/salusha)

Snehal Taori — Participant, Adobe Hackathon 2025  
GitHub: [https://github.com/snehaltaori](https://github.com/snehaltaori)

Deepanshi Verma — Participant, Adobe Hackathon 2025  
GitHub: [https://github.com/DeepanshiiVerma](https://github.com/DeepanshiiVerma)


---
