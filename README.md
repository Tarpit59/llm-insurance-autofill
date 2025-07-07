
# Insurance Template Filler – Web App

This web app allows users to upload insurance photo report PDFs and a .docx template. The system uses OCR + AI to extract relevant information and automatically fills the template. The final result can be downloaded as a filled PDF or viewed directly in the browser.

## Directory Structure
```plaintext
.
│
├── insurance_pipeline/
│
├── sample/
│
├── app.py
│
├── .env
│
├── requirements.txt
│
└── README.md
```

## Files Details
### insurance_pipeline/
- Core pipeline code (extraction, OCR, LLM, etc.)

### sample/
- Sample input and output files are available.

### app.py
- Streamlit app for UI interaction.

### .env
- API keys and environment variables.

### requirements.txt
- Required packages to run web application.

### README.md
- Project documentation.


## Setup Instructions

1. Create & Activate Virtual Environment:
```bash
python3.9 -m venv task_3
source task_3/bin/activate   # macOS/Linux
task_3\Scripts\activate      # Windows
```

2. Install paddlepaddle-gpu:
```bash
python -m pip install paddlepaddle-gpu==3.1.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```
- Make sure your system has CUDA 11.8. If not, you can alternatively install `paddlepaddle-cpu`.
- For more information visit [here](https://www.paddlepaddle.org.cn/en/install/quick?docurl=/documentation/docs/en/develop/install/pip/linux-pip_en.html).

3. Install other dependencies required to run application:
```bash
pip install -r requirements.txt
```

4. Make sure required api keys are not empty in .env file:
```bash
OPENROUTER_API_KEY = "openrouter_api_key"
GOOGLE_API_KEY = "google_api_key"
PINECONE_API_KEY = "pinecone_api_key"
COHERE_API_KEY = "cohere_api_key"
GROQ_API_KEY = "groq_api_key"
CONVERTAPI_API_KEY = "convertapi_api_key"
```

5. Run the App:
```bash
streamlit run app.py
```
- This will launch a local web server and open the app in your browser.

## Pipeline Flow (Text-Based Diagram)
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

## Performance Considerations

**Note on Performance:** Please be aware that there is a **5-second delay** after each request to the Large Language Model (LLM) when retrieving field data. This is an intentional pause implemented to manage API usage.

- insurance_pipeline/qa_utils.py : Modify in this file.

```python
def extract_all_fields(field_descriptions, vector_store, ...):

    final_results = {}
       
    # ... rest of the code

        time.sleep(5)

    return final_results
```


## Acknowledgements

 - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
 - [LangChain RAG](https://python.langchain.com/v0.2/docs/tutorials/rag/)
 - [Cohere ReRank with LangChain](https://docs.cohere.com/docs/rerank-on-langchain)
 - [Pinecone guides](https://docs.pinecone.io/guides/get-started/quickstart)
 - [ChatGroq](https://python.langchain.com/docs/integrations/chat/groq/)
 - [Google Generative AI Embeddings](https://api.python.langchain.com/en/latest/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html)
 - [Openrouter Documentation](https://openrouter.ai/docs/quickstart)
 - [Convertapi](https://www.convertapi.com/)
 - [Streamlit](https://docs.streamlit.io/get-started/fundamentals/main-concepts)