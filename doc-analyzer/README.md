# AI-Powered Document Analysis API

Intelligent document processing system that extracts, analyses, and summarises content from **PDF**, **DOCX**, and **image** files using Claude AI.

## Features
- 📄 **Multi-format support** — PDF, DOCX, PNG/JPG/TIFF images
- 🔍 **Text extraction** — pdfplumber (PDF), python-docx (DOCX), Tesseract OCR (images)
- 🤖 **AI summarisation** — concise 2–4 sentence summary via Claude
- 🏷️ **Named entity extraction** — persons, organisations, locations, dates, monetary amounts
- 💬 **Sentiment analysis** — positive / negative / neutral with numeric score (−1 to 1)

## API Reference

### `POST /analyze`

Upload a document for full analysis.

**Headers**
```
X-API-Key: <your-api-key>
Content-Type: multipart/form-data
```

**Body**
| Field | Type | Description |
|-------|------|-------------|
| `file` | file | PDF, DOCX, or image file |

**Response (200)**
```json
{
  "filename": "report.pdf",
  "file_type": "pdf",
  "extracted_text_preview": "First 500 chars of extracted text…",
  "summary": "This document describes quarterly financial results for Acme Corp...",
  "entities": {
    "persons": ["John Smith", "Jane Doe"],
    "organisations": ["Acme Corp", "World Bank"],
    "locations": ["New York", "London"],
    "dates": ["January 2024", "Q3 2023"],
    "monetary_amounts": ["$1.2 million", "€500,000"],
    "other": []
  },
  "sentiment": {
    "label": "positive",
    "score": 0.72,
    "explanation": "The document uses optimistic language about growth and future prospects."
  }
}
```

**cURL example**
```bash
curl -X POST https://your-app.onrender.com/analyze \
  -H "X-API-Key: your-api-key" \
  -F "file=@/path/to/document.pdf"
```

### `GET /health`
Returns `{"status": "ok"}` — used for deployment health checks.

---

## Local Development

### Prerequisites
- Python 3.11+
- Tesseract OCR: `sudo apt install tesseract-ocr` (Linux) or `brew install tesseract` (Mac)
- Poppler: `sudo apt install poppler-utils` (Linux) or `brew install poppler` (Mac)

### Setup
```bash
git clone https://github.com/your-username/doc-analyzer
cd doc-analyzer

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

export ANTHROPIC_API_KEY=sk-ant-...
export DOC_API_KEY=your-chosen-key

uvicorn app.main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### Run tests
```bash
python tests/test_api.py --url http://localhost:8000 --key your-chosen-key --file tests/sample.pdf
```

---

## Deployment on Render (Free)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service** → connect your repo.
3. Render auto-detects the `Dockerfile` — click **Create Web Service**.
4. In **Environment Variables**, add:
   - `ANTHROPIC_API_KEY` = your Anthropic key
   - `DOC_API_KEY` = your chosen API key (share this with the evaluators)
5. Your public URL will be `https://doc-analyzer-api.onrender.com`.

> **Note**: Free Render services spin down after inactivity. First request may take ~30s.

---

## Project Structure
```
doc-analyzer/
├── app/
│   └── main.py          # FastAPI app — extraction + AI analysis
├── tests/
│   └── test_api.py      # Smoke-test script
├── Dockerfile           # Production container
├── render.yaml          # One-click Render deployment
├── requirements.txt
└── README.md
```

## Tech Stack
| Layer | Technology |
|-------|-----------|
| API framework | FastAPI |
| AI model | Anthropic Claude (claude-opus-4-5) |
| PDF extraction | pdfplumber |
| DOCX extraction | python-docx |
| OCR | Tesseract via pytesseract |
| Deployment | Docker on Render.com |
