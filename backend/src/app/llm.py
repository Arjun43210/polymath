# backend/src/app/llm.py
import os
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_KEY

def answer_with_llm(question: str, retrieved: list, max_tokens: int = 300):
    # Build a short prompt that instructs the LLM to only use the provided context
    context = "\n\n---\n".join([f"[p{r['page']}]\n{r['text']}" for r in retrieved])
    prompt = (
        "You are an assistant that answers questions using ONLY the provided textbook excerpts. "
        "Cite pages in brackets (e.g., [p12]). If the answer is not contained in the excerpts, say "
        "'I don't know based on the textbook.'\n\n"
        "Context:\n" + context + "\n\n"
        f"Question: {question}\nAnswer:"
    )
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # replace with model you have access to or local model call
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.0,
    )
    return resp["choices"][0]["message"]["content"].strip()
