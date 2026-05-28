import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = None

def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")
        _client = genai.Client(api_key=api_key)
    return _client


def generate(prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    client = get_client()
    response = client.models.generate_content(model=model_name, contents=prompt)
    return response.text
