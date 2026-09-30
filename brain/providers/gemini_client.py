from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def generate(messages: list[dict]) -> str:
    system_texts = [m["content"] for m in messages if m["role"] == "system"]
    system_instruction = "\n".join(system_texts) if system_texts else None

    contents = []
    for m in messages:
        if m["role"] == "system":
            continue
        gemini_role = "model" if m["role"] == "assistant" else "user"
        contents.append({"role": gemini_role, "parts": [{"text": m["content"]}]})

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config={"system_instruction": system_instruction} if system_instruction else None,
    )

    if not response.text:
        print(f"[gemini_client] Empty response. Full object: {response}")
        # Check if candidates exist and why generation stopped
        if response.candidates:
            reason = response.candidates[0].finish_reason
            print(f"[gemini_client] finish_reason: {reason}")

    return response.text