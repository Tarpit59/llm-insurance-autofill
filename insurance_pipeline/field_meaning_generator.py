import os
import re
import json
import requests
from insurance_pipeline.config import OPENROUTER_LLM_FIELD_UNDERSTANDING_MODEL, OPENROUTER_API_KEY
from insurance_pipeline.docx_utils import extract_field_contexts


def extract_json_from_markdown(response_text):
    """Extracts JSON from inside a markdown code block."""
    match = re.search(r"```(?:json)?\s*({.*?})\s*```", response_text, re.DOTALL)
    if match:
        return match.group(1)
    return response_text


def build_meaning_prompt(field_contexts):
    prompt = (
        "You are an expert at understanding document templates. "
        "For each field, you'll see one or more example sentences showing how it's used. "
        "Return a JSON where each key is the field, and each value is its meaning.\n\n"
        "Format:\n```json\n{\n  \"FIELD\": \"meaning\", ...\n}\n```"
    )

    for field, sents in field_contexts.items():
        combined = " | ".join(sents)
        prompt += f"\n\nField: {field}\nSentences: {combined}"

    return prompt


def query_openrouter(prompt, api_key, model=OPENROUTER_LLM_FIELD_UNDERSTANDING_MODEL):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Output exactly one JSON object."},
            {"role": "user", "content": prompt}
        ]
    }

    for attempt in range(3):
        response = requests.post(url, headers=headers, json=body)
        data = response.json()
        content = data['choices'][0]['message']['content'].strip()

        if content and content != "```":
            try:
                json_str = extract_json_from_markdown(content)
                return json.loads(json_str)
            except json.JSONDecodeError:
                print(f"Attempt {attempt+1}: Invalid JSON, retrying...")
        else:
            print(f"Attempt {attempt+1}: Empty or placeholder response, retrying...")

    print("❌ Failed after 3 attempts.")
    print("🧾 Last response:\n", response.text)
    return {}


def extract_field_meanings(doc_path):
    field_contexts = extract_field_contexts(doc_path)
    prompt = build_meaning_prompt(field_contexts)
    field_meanings = query_openrouter(prompt, OPENROUTER_API_KEY)
    print(" Extracted Field Meanings:\n", json.dumps(field_meanings, indent=2))
    return field_meanings


if __name__ == "__main__":
    template_path = "path/to/insurance/template/doc"
    meanings = extract_field_meanings(template_path)
