import gradio as gr

import requests
import json

API_URL = "http://localhost:8000"

def text2knowledge(text):
    url = f"{API_URL}/knowledges"
    response = requests.post(
        url,
        json = {
            "text": text
        }
    )

    response_text = response.text

    obj = json.loads(response_text)

    return json.dumps(obj, indent=2, ensure_ascii=False)


interface = gr.Interface(
    fn=text2knowledge, 
    inputs="text", 
    outputs="textarea",
    examples=["田中さんはABC株式会社でエンジニアをしています"],
)