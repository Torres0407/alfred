from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY, max_retries=0)


def generate(messages: list[dict], tools: list = None):
    kwargs = {"model": GROQ_MODEL, "messages": messages}
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message