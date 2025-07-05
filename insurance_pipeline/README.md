
# Insurance Template Filler Pipeline

This project automates the extraction of key-value data from multi-page photo report PDFs and fills them into a .docx insurance template using OCR, vector search, reranking, and LLM-based reasoning.

## Directory Structure
```plaintext
.
insurance_pipeline/
│
├── main.py
│
├── config.py
│
├── ocr_utils.py
│
├── vector_store.py
│
├── qa_utils.py
│
├── docx_utils.py
│
├── field_meaning_generator.py
│
└── README.md
```

## Files Details
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
- Infers missing field descriptions from the `.docx` template using LLM context.

### README.md
- Pipeline Documentation.


## Running the Pipeline
- Make sure all required dependencies are installed and `.env` is configured.

### Run main.py
```bash
python -m insurance_pipeline.main
```
This will:
- Load and OCR the PDF photo reports.
- Chunk and embed the text using Google Generative AI.
- Store embeddings in Pinecone.
- Understand field meaning and get descriptions about fields using LLM reasoning.
- Extract field values using similarity search + reranking + LLM reasoning.
- Fill those values into the `.docx` insurance template.
- Convert the output .docx to PDF using ConvertAPI.

## Acknowledgements

 - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
 - [LangChain RAG](https://python.langchain.com/v0.2/docs/tutorials/rag/)
 - [Cohere ReRank with LangChain](https://docs.cohere.com/docs/rerank-on-langchain)
 - [Pinecone guides](https://docs.pinecone.io/guides/get-started/quickstart)
 - [ChatGroq](https://python.langchain.com/docs/integrations/chat/groq/)
 - [Google Generative AI Embeddings](https://api.python.langchain.com/en/latest/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html)
 - [Openrouter Documentation](https://openrouter.ai/docs/quickstart)
 - [ConvertAPI](https://www.convertapi.com/)