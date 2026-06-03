from settings import OPENROUTER_KEY

from openai import OpenAI

from src.config.settings import OPENROUTER_KEY

client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)