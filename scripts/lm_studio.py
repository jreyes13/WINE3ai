#!/usr/bin/env python3
"""
LM Studio Client Helper for WINE³ai
Delegates generation, translations, summaries, and text processing
to the local LM Studio instance running on http://localhost:1234.
"""

import sys
import json
import urllib.request
import urllib.error

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3.5-9b"

def query_lm(prompt, system_prompt=None, model=DEFAULT_MODEL, max_tokens=5000, temperature=0.2, return_usage=False):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    req = urllib.request.Request(
        LM_STUDIO_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload).encode("utf-8")
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            choice = data["choices"][0]
            msg = choice["message"]
            content = msg.get("content", "").strip()
            finish_reason = choice.get("finish_reason", "")
            usage = data.get("usage", {})
            
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            total_tokens = usage.get("total_tokens", 0)
            reasoning_tokens = usage.get("completion_tokens_details", {}).get("reasoning_tokens", 0)

            token_stats = {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "reasoning_tokens": reasoning_tokens
            }

            if finish_reason == "length":
                sys.stderr.write(f"[LM Studio Warning] Response hit max_tokens limit ({max_tokens}) and was truncated.\n")

            if return_usage:
                return content, token_stats
            return content
    except Exception as e:
        sys.stderr.write(f"[LM Studio Error] {type(e).__name__}: {e}\n")
        if return_usage:
            return None, {}
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 lm_studio.py '<prompt>' ['<system_prompt>']")
        sys.exit(1)

    user_prompt = sys.argv[1]
    sys_prompt = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = query_lm(user_prompt, sys_prompt)
    if result:
        print(result)
    else:
        sys.exit(1)
