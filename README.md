# LLM-Powered Fact Checker

AI-powered fact verification system using RAG (Retrieval-Augmented Generation) to verify claims against a trusted knowledge base.

## 🎯 Features

- **NLP-based claim extraction** using spaCy
- **Semantic search** with FAISS vector database
- **Local LLM verification** using Mistral via Ollama
- **Confidence scoring** with threshold filtering
- **Interactive Streamlit UI** with feedback mechanism

## 📋 Requirements

- Python 3.8+
- Ollama (for Mistral LLM)

## 🚀 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Install Ollama

Download from: https://ollama.com/download

```bash
ollama pull mistral
```

### 3. Initialize Fact Database

```bash
python main.py
```

This will create the FAISS index from `facts.txt` on first run.

## 💻 Usage

### Run Streamlit UI

```bash
streamlit run app.py
```

Access at: http://localhost:8501

### Programmatic Usage

```python
from fact_checker import FactChecker

# Initialize
checker = FactChecker()
checker.initialize_facts("facts.txt")

# Check a claim
result = checker.check_fact("Your claim here")

print(result['verdict'])      # True/False/Unverifiable
print(result['confidence'])   # Confidence score
print(result['reasoning'])    # Explanation
print(result['evidence'])     # Retrieved facts
```

## 📁 Project Structure

```
.
├── claim_extractor.py      # NLP claim extraction (spaCy)
├── vector_db.py           # FAISS vector database
├── llm_verifier.py        # Mistral LLM verification
├── fact_checker.py        # Main pipeline orchestrator
├── facts.txt              # Trusted fact database (30 facts)
├── app.py                 # Streamlit UI
├── main.py                # Example usage
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## 🔧 How It Works

1. **Input:** User enters a claim
2. **Confidence Check:** System calculates similarity to fact base
3. **Threshold Filter:** Claims with <30% confidence → "Unverifiable"
4. **Retrieval:** Top-3 most similar facts retrieved using FAISS
5. **LLM Verification:** Mistral compares claim against evidence
6. **Output:** Verdict (True/False/Unverifiable) + reasoning + evidence

## 📊 Sample Outputs

### False Claim
```json
{
  "verdict": "False",
  "confidence": 0.9453,
  "reasoning": "Evidence indicates no such announcement exists",
  "evidence": [
    "No nationwide free electricity to farmers program announced for July 2025",
    "State-specific subsidies exist but no central policy"
  ]
}
```

### Unverifiable Claim
```json
{
  "verdict": "Unverifiable",
  "confidence": 0.21,
  "reasoning": "Insufficient relevant evidence (confidence: 0.21)",
  "evidence": []
}
```

## 🎨 UI Features

- Clean, minimal interface
- Color-coded verdicts (Green/Red/Yellow)
- Confidence percentage display
- Evidence citations
- Feedback buttons (👍/👎)

## ⚙️ Configuration

**Adjust confidence threshold** in `fact_checker.py`:
```python
result = checker.check_fact(text, threshold=0.3)  # Default: 30%
```

**Change retrieval count** (top-k):
```python
result = checker.check_fact(text, top_k=3)  # Default: 3
```

## 🧪 Testing

**Test False claim:**
```
The Indian government has announced free electricity to all farmers starting July 2025.
```

**Test Unverifiable claim:**
```
Quantum computing will replace all classical computers by 2030.
```

## 📝 License

MIT License

## 👤 Author

Siddharth Mishra