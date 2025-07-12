
# 🧾 Insurance Template Filler – Web App

This web app allows users to upload insurance photo report PDFs and a `.docx` template. The system uses OCR + AI to extract relevant information and automatically fills the template. The final result can be downloaded as a filled PDF or viewed directly in the browser.

## 📁 Project Structure
```plaintext
.
├── insurance_pipeline/     # Core pipeline (OCR, extraction, LLMs, etc.)
├── sample/                 # Sample input/output files
├── app.py                  # Streamlit app for UI interaction
├── .env                    # API keys
├── requirements.txt        # Dependencies list
└── README.md               # Project documentation
```

## 🚀 Setup Instructions

1. Create & Activate Virtual Environment:
```bash
python3.9 -m venv task_3
source task_3/bin/activate   # macOS/Linux
task_3\Scripts\activate      # Windows
```

2. Install PaddleOCR:

If you have a GPU and CUDA 11.8:

```bash
python -m pip install paddlepaddle-gpu==3.1.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```

If not, use the CPU version:

```bash
pip install paddlepaddle
```
- More installation details: [PaddlePaddle Installation Guide](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/develop/install/pip/linux-pip_en.html).

3. Install Other Dependencies:
```bash
pip install -r requirements.txt
```

4. Add API Keys to `.env` File:

- Make sure your `.env` file includes:

```bash
OPENROUTER_API_KEY = "openrouter_api_key"
GOOGLE_API_KEY = "google_api_key"
PINECONE_API_KEY = "pinecone_api_key"
COHERE_API_KEY = "cohere_api_key"
GROQ_API_KEY = "groq_api_key"
CONVERTAPI_API_KEY = "convertapi_api_key"
```

5. Run the Application:
```bash
streamlit run app.py
```
- A local server will start and open the app in your default browser.

## 🧠 Pipeline Overview
```text
┌────────────────────────────┐
│        Upload Inputs       │
│ ┌────────────────────────┐ │
│ │       Report PDFs      │ │
│ │     .docx Template     │ │
│ └────────────────────────┘ │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│    OCR + Text Chunking     │
│ - OCR PDFs                 │
│ - Split into text chunks   │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│  Embedding + Pinecone DB   │
│ - Convert chunks to vectors│
│ - Store in Pinecone index  │
└────────────┬───────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│   Field Meaning Extraction (LLM)     │
│ - Extract placeholders from .docx    │
│ - Understand meaning (OpenRouter LLM)│
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│     Semantic Retrieval + QA          │
│ - Similarity search (Pinecone)       │
│ - Rerank with Cohere                 │
│ - Final answer via GROQ LLM          │
└────────────┬─────────────────────────┘
             │
             ▼
┌────────────────────────────┐
│    Fill Template Fields    │
│ - Replace placeholders     │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│      Convert to PDF        │
│ - Use ConvertAPI           │
└────────────┬───────────────┘
             │
             ▼
┌────────────────────────────┐
│    Preview & Download PDF  │
│ - View PDF in browser      │
│ - Download final PDF       │
└────────────────────────────┘

```

## ⏱️ Performance Note

To manage LLM API usage and rate limits, a delay is added between field queries. You can modify this in: `insurance_pipeline/qa_utils.py`

- insurance_pipeline/qa_utils.py : Modify in this file.

```python
def extract_all_fields(...):
    ...
    time.sleep(5)  # Delay between LLM requests
```

## 📸 Sample Files
- You can find sample `.docx` templates and insurance report PDFs in the `sample/` directory for testing.

## 🙏 Acknowledgements

 - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
 - [LangChain RAG](https://python.langchain.com/v0.2/docs/tutorials/rag/)
 - [Cohere ReRank with LangChain](https://docs.cohere.com/docs/rerank-on-langchain)
 - [Pinecone guides](https://docs.pinecone.io/guides/get-started/quickstart)
 - [ChatGroq](https://python.langchain.com/docs/integrations/chat/groq/)
 - [Google Generative AI Embeddings](https://api.python.langchain.com/en/latest/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html)
 - [Openrouter Documentation](https://openrouter.ai/docs/quickstart)
 - [Convertapi](https://www.convertapi.com/)
 - [Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts)