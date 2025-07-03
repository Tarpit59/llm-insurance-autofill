import re
import cohere
import time
import json
from insurance_pipeline.config import COHERE_RERANK_MODEL

def rerank_results_with_cohere(query, search_results, cohere_api_key,
                               rerank_model,relevance_threshold=0.0001):
    try:
        co = cohere.Client(api_key=cohere_api_key)
        documents = [doc.page_content for doc in search_results]
        rerank_response = co.rerank(query=query, documents=documents, model=rerank_model)

        reranked_results = sorted(
            [
                (doc, result.relevance_score)
                for doc, result in zip(search_results, rerank_response.results)
                if result.relevance_score >= relevance_threshold
            ],
            key=lambda x: x[1], reverse=True
        )
        return [result[0] for result in reranked_results]
    except Exception as e:
        print(f"Error reranking results: {e}")

def retrieve_answers(index, chain, query, cohere_api_key):
    try:
        search_results = index.similarity_search(query, k=12)
        
        if len(search_results) == 0:
            return None
        reranked_results = rerank_results_with_cohere(query, search_results, cohere_api_key, COHERE_RERANK_MODEL)

        response = chain.run(input_documents=reranked_results, question=query)
        return response
    except Exception as e:
        print(f"Error retrieving answers: {e}")

def extract_exact_field_json(answer_text: str, field: str):
    pattern = r'\{\s*"' + re.escape(field) + r'"\s*:\s*"([^"]*)"\s*\}'
    match = re.search(pattern, answer_text, re.DOTALL)
    if match:
        value = match.group(1).strip()
        return {field: value}, True
    else:
        return None, False

def get_field_value_with_retry(vector_store, qa_chain, field, description, cohere_api_key, max_retries=2):
    query = f"""
You are extracting data for the insurance report: {field}
Field Meaning : {description}

Question:
What is the best value for: "{description}"?

Rules:
- Return only the exact short value.
- Return one **valid JSON object** only, like:

json
  {{
    "{field}": "ABC"
  }}

  or

json
  {{
    "{field}": ""
  }}

- **Do NOT** include anything else: no commentary, no wrapping tags, no backticks.
- If you cannot find a value, return the JSON with an empty string.
"""
    for attempt in range(1, max_retries + 1):
        
        answer = retrieve_answers(vector_store, qa_chain, query, cohere_api_key=cohere_api_key)

        if answer is None:
            return None
        result, success = extract_exact_field_json(answer, field)
        
        if success:
            return result
    return None

def extract_all_fields(field_descriptions, vector_store, qa_chain, cohere_api_key):

    final_results = {}

    for field, description in field_descriptions.items():

        result = get_field_value_with_retry(
            vector_store, qa_chain, field, description, cohere_api_key, max_retries=3)
        if result:
            print(f"✅ Final Extracted: {result}")
            final_results[field] = result[field]
        else:
            print(f"❌ Could not determine {field}")
            final_results[field] = ""

        time.sleep(5)

    return final_results
