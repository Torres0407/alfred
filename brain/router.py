import json
import time
import re
from brain.providers import groq_client, gemini_client
from tools.registry import TOOL_DEFINITIONS, execute_tool

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
                wait_time = float(wait_match.group(1)) + 1
                print(f"[router] Groq rate limited, waiting {wait_time:.1f}s and retrying ({attempt + 1}/{MAX_RATE_LIMIT_RETRIES})...")
                time.sleep(wait_time)
                continue
            break

    print(f"[router] Groq failed after retries ({last_error}), falling back to Gemini (simple mode, no tools)...")
    try:
        clean_messages = []
        for m in messages:
            if m.get("role") == "system":
                clean_messages.append({
                    "role": "system",
                    "content": (
                        "You are Alfred, a helpful personal AI assistant. You currently do NOT have access to "
                        "any tools, live data, or the ability to perform real actions (no email, music, files, "
                        "smart home, or system control). If the user asks you to DO something (play music, send "
                        "an email, check a file, control a device), you MUST clearly tell them you're temporarily "
                        "unable to perform actions right now and they should try again shortly — NEVER claim an "
                        "action succeeded or describe a result as if it happened. You may still answer general "
                        "knowledge questions normally."
                    )
                })
            elif m.get("role") in ("user", "assistant") and isinstance(m.get("content"), str) and m.get("content"):
                clean_messages.append(m)

        reply = gemini_client.generate(clean_messages)
        return reply or "Sorry, I'm having trouble generating a response right now — please try again shortly."
    except Exception as e2:
        print(f"[router] Gemini also failed ({e2})")
        return "Sorry, both AI providers are currently unavailable. Please wait a moment and try again."


def _route_with_groq(messages: list[dict]) -> str:
    messages = list(messages)

    for _ in range(MAX_TOOL_ROUNDS):
        msg = groq_client.generate(messages, tools=TOOL_DEFINITIONS)

        if not msg.tool_calls:
            return msg.content or "Done."

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": msg.tool_calls
        })

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            result = execute_tool(name, args)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "I tried a few steps but couldn't finish that. Could you rephrase?"