import json, os
from groq import Groq
from src.config import Config

client = Groq(api_key=Config.GROQ_API_KEY)

def generate_dataset(scenarios):
    with open("data/git_traces.jsonl", "w") as f:
        for s in scenarios:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": f"Create SRE trace JSON for: {s}"}],
                response_format={"type": "json_object"}
            )
            f.write(response.choices[0].message.content + "\n")