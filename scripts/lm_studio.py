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

def query_lm(prompt, system_prompt=None, model=DEFAULT_MODEL, max_tokens=4096, temperature=0.3):
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
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            msg = data["choices"][0]["message"]
            content = msg.get("content", "").strip()
            
            # If content is empty (e.g. truncated thinking), extract reasoning content
            if not content and "reasoning_content" in msg:
                content = msg["reasoning_content"].strip()
                
            return content
    except urllib.error.URLError as e:
        sys.stderr.write(f"[LM Studio Error] {e}\n")
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
