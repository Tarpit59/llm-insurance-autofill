from insurance_pipeline.config import *
from insurance_pipeline.ocr_utils import load_documents_with_ocr
from insurance_pipeline.vector_store import initialize_pinecone, chunk_documents, create_vector_store
from insurance_pipeline.qa_utils import extract_all_fields
from insurance_pipeline.docx_utils import fill_placeholders_in_docx
from insurance_pipeline.field_meaning_generator import extract_field_meanings
from insurance_pipeline.docx_utils import convert_docx_to_pdf_via_convertapi
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
import json
import os
import time

llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=GROQ_LLM_QA_MODEL)
qa_chain = load_qa_chain(llm, chain_type="stuff")
embeddings = GoogleGenerativeAIEmbeddings(google_api_key=GOOGLE_API_KEY, model=EMBEDDINGS_MODEL_NAME)

def setup_vector_store(index_name, folder_path):
    """Initializes Pinecone, loads and chunks documents, and creates vector store."""

    initialize_pinecone(api_key=PINECONE_API_KEY, index_name=index_name)
    docs = load_documents_with_ocr(folder_path)
    chunks = chunk_documents(docs)
    vector_store = create_vector_store(chunks, embeddings, index_name)
    return vector_store

def run_pipeline(folder_path, template_path, output_path=None, index_name=PINECONE_INDEX_NAME):
    """Runs the full extraction + document generation pipeline."""
    vector_store = setup_vector_store(index_name, folder_path)

    print("Extracting field descriptions from template...")
    field_descriptions = extract_field_meanings(template_path)
    time.sleep(2)
    print("Running field value extraction...")
    all_extracted_values = extract_all_fields(
        field_descriptions,
        vector_store,
        qa_chain,
        COHERE_API_KEY
    )

    print("\n\n All Extracted Values:")
    print(json.dumps(all_extracted_values, indent=2))

    print("Filling template with extracted values...")
    doc = fill_placeholders_in_docx(
        template_path=template_path,
        extracted_values=all_extracted_values
    )
    
    if output_path is not None:
        doc.save(output_path)
        print(f"Document saved at: {output_path}")

        try:
            pdf_output_path = convert_docx_to_pdf_via_convertapi(
                input_path=output_path,
                output_dir=os.path.dirname(output_path)
            )
            print(f"PDF saved at: {pdf_output_path}")
            os.remove(output_path)
            return pdf_output_path

        except Exception as e:
            print(f"PDF conversion via ConvertAPI failed: {e}")
            return None

if __name__ == "__main__":
    
    FOLDER_PATH  = 'path/to/reports/folder'
    TEMPLATE_PATH ='path/to/template/docx'
    OUTPUT_PATH  = "path/to/output/filled_output.docx"
    pdf_output_path = run_pipeline(FOLDER_PATH, TEMPLATE_PATH, OUTPUT_PATH)