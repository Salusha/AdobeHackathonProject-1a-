# Adobe Hackathon 2025 - Round 1A

## ✅ Approach

- Used PyMuPDF to extract text and layout info from PDF
- Font size frequency used to identify likely heading sizes
- Top 3 font sizes mapped to H1, H2, H3
- Title inferred from the largest text span on the first few pages

## 🛠️ Dependencies

- Python 3.10
- PyMuPDF 1.23.7

## 🚀 Build & Run Instructions

```bash
docker build --platform linux/amd64 -t pdfextractor:round1a .
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdfextractor:round1a
