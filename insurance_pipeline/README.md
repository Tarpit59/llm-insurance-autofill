
# 🧾 Insurance Template Filler Pipeline

This project automates the extraction of key-value data from multi-page photo report PDFs and fills them into a `.docx` insurance template using OCR, vector search, reranking, and LLM-based reasoning.

## 📁 Directory Structure
```plaintext
.
insurance_pipeline/
|
├── main.py                     # Main pipeline orchestrator
├── config.py                   # Loads API keys and configuration from .env
├── ocr_utils.py                # OCR utilities using PaddleOCR
├── vector_store.py             # Embedding and Pinecone vector DB logic
├── qa_utils.py                 # RAG-based QA pipeline with reranking and LLM
├── docx_utils.py               # Template filling and conversion to PDF
├── field_meaning_generator.py  # LLM-based field context understanding
└── README.md                   # This documentation
```

## 📄 File Descriptions
### main.py
- The main entry point — orchestrates the entire pipeline.

### config.py
- Loads environment variables from `.env` and stores global constants (e.g., API keys).

### ocr_utils.py
- Loads PDFs and performs OCR using PaddleOCR, with fallback mechanisms if needed.

### vector_store.py
- Converts PDF text into embeddings and stores them in a Pinecone vector database.

### qa_utils.py
- Retrieves relevant chunks from the vector DB, Rerank and extracts values using an LLM.

### docx_utils.py
- Replaces placeholders in `.docx` templates with the extracted values and can convert final document to PDF.

### field_meaning_generator.py
- Uses LLM to infer the meaning or description of fields directly from the template.


## 🚀 Running the Pipeline

1. ✅ Make sure:
  - Dependencies from `requirements.txt` are installed.
  - `.env` is properly configured with required API keys.
  - Input paths (`FOLDER_PATH`, `TEMPLATE_PATH`, `OUTPUT_PATH`) are set inside main.py.

2. ▶️ Run the pipeline:
```bash
python -m insurance_pipeline.main
```

#### What it does:
- ✅ Loads and OCRs all report pages.
- ✅ Chunk and embed texts with Google Generative AI Embeddings.
- ✅ Stores vector embeddings in Pinecone.
- ✅ Extracts field meanings from the `.docx` template using LLM-based reasoning.
- ✅ Extract field values using similarity search + reranking + LLM reasoning..
- ✅ Populates the `.docx` insurance template with the extracted values.
- ✅ Optionally converts the filled `.docx` into a final PDF using ConvertAPI.

## 🙏 Acknowledgements

 - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
 - [LangChain RAG](https://python.langchain.com/v0.2/docs/tutorials/rag/)
 - [Cohere ReRank with LangChain](https://docs.cohere.com/docs/rerank-on-langchain)
 - [Pinecone guides](https://docs.pinecone.io/guides/get-started/quickstart)
 - [ChatGroq](https://python.langchain.com/docs/integrations/chat/groq/)
 - [Google Generative AI Embeddings](https://api.python.langchain.com/en/latest/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html)
 - [Openrouter Documentation](https://openrouter.ai/docs/quickstart)
 - [ConvertAPI](https://www.convertapi.com/)