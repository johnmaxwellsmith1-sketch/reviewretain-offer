#!/usr/bin/env python3
"""
ReviewRetain — Review Response Agent
Drafts a warm, specific reply to a Google review using an LLM API.
Requires: OPENAI_API_KEY (or ANTHROPIC_API_KEY) in env.
Usage: python3 review_agent.py "review text here"
"""
import os, sys, json

def draft_reply(review_text, business_type="local business"):
    """Draft a reply using OpenAI-compatible API."""
    key = os.environ.get("OPENAI_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return "ERROR: Set OPENAI_API_KEY or ANTHROPIC_API_KEY in your environment."
    # Detect sentiment roughly
    neg_words = ["bad","terrible","worst","rude","slow","never","awful","disappointed","unprofessional"]
    is_negative = any(w in review_text.lower() for w in neg_words)
    tone = "apologetic, accountable, and offer to make it right" if is_negative else "warm, specific, and inviting repeat business"
    prompt = f"""You are a customer-service expert for a {business_type}.
Draft a reply to this Google review. Keep it under 60 words, {tone}.
Reference something specific from the review. Do NOT use generic filler.
Review: "{review_text}"
Reply:"""
    # OpenAI-compatible call
    import urllib.request
    body = json.dumps({
        "model": os.environ.get("LLM_MODEL", "gpt-4o-mini"),
        "messages": [{"role":"user","content":prompt}],
        "temperature": 0.7
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    return data["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 review_agent.py \"<review text>\"")
        sys.exit(1)
    print(draft_reply(sys.argv[1]))
