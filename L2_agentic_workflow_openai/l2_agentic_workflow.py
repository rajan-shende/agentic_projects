import os
import json
import requests
from openai import OpenAI
import os

def load_api_key():
    base_dir = os.path.dirname(__file__)   # directory of current script
    key_path = os.path.join(base_dir, "creds", "key.txt")
    with open(key_path, "r") as file:
        return file.read().strip()

key = load_api_key()
# ---------------- INIT OPENAI CLIENT ----------------
client = OpenAI(api_key=key)


# ---------------- SPEC (LLM POWERED) ----------------
def generate_specification(user_input: str) -> dict:
    """
    Uses LLM to convert natural language into structured JSON spec.
    """
    prompt = f"""
    Convert the following user request into JSON.

    User Request: "{user_input}"

    Output strictly in this format:
    {{
        "task": "get_user_repos",
        "username": "github_username"
    }}

    Only return valid JSON. No explanation.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # Safety: Remove accidental markdown wrapping
        if content.startswith("```"):
            content = content.split("```")[1]

        return json.loads(content)

    except Exception as e:
        print("❌ Spec generation failed:", e)
        return None


print(generate_specification("i was checking all public work of rajan shende on github"))