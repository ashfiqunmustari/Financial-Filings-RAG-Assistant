import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")

client = InferenceClient(api_key=HF_TOKEN)


def generate_answer(question, context):

    prompt = f"""
You are a financial analyst answering questions about a company's SEC 10-K filing.

Use ONLY the information provided in the context.

If the answer cannot be found in the context, reply exactly:
"I couldn't find that information in the filing."

Do not use outside knowledge.
Do not make assumptions.
Keep the answer concise.
Use bullet points whenever appropriate.

Context:
--------------------------------------------------
{context}
--------------------------------------------------

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model=HF_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()