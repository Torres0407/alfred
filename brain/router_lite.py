import json
import time
import re
from brain.providers import groq_client, gemini_client
from tools.registry_lite import TOOL_DEFINITIONS, execute_tool

MAX_TOOL_ROUNDS = 5
MAX_RATE_LIMIT_RETRIES = 2


def route(messages: list[dict]) -> str:
    last_error = None
    for attempt in range(MAX_RATE_LIMIT_RETRIES + 1):
        try:
            return _route_with_groq(messages)
        except Exception as e:
            last_error = e
            wait_match = re.search(r"try again in ([\d.]+)s", str(e))
            if wait_match and attempt < MAX_RATE_LIMIT_RETRIES:
                time.sleep(float(wait_match.group(1)) + 1)
                continue
            break

    try:
        clean_messages = []
        for m in messages:
            if m.get("role") == "system":
                clean_messages.append({
                    "role": "system",
                    "content": (
                        "You are Alfred, a helpful personal AI assistant demo. You currently do NOT have "
                        "access to tools right now. If asked to perform an action, say you're temporarily "
                        "unable to and never claim something succeeded."
                    )
                })
            elif m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str) and m.get("content"):
                clean_messages.append(m)
        reply = gemini_client.generate(clean_messages)
        return reply or "Sorry, I'm having trouble right now — please try again shortly."
    except Exception as e2:
        return "Sorry, both AI providers are currently unavailable. Please wait a moment and try again."


def _route_with_groq(messages: list[dict]) -> str:
    messages = list(messages)
    for _ in range(MAX_TOOL_ROUNDS):
        msg = groq_client.generate(messages, tools=TOOL_DEFINITIONS)
        if not msg.tool_calls:
            return msg.content or "Done."
        messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})
        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = execute_tool(tool_call.function.name, args)
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": result})
    return "I tried a few steps but couldn't finish that. Could you rephrase?"