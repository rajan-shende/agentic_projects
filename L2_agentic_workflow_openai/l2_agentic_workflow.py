import os
import json
import requests
import google.genai as ai
import os

def load_api_key():
    base_dir = os.path.dirname(__file__)   # directory of current script
    key_path = os.path.join(base_dir, "creds", "key.txt")
    with open(key_path, "r") as file:
        return file.read().strip()

key = load_api_key()
# ---------------- INIT OPENAI CLIENT ----------------
client = ai.Client(api_key=key)


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
        response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )

        content = response.text
        print(content)

        # Safety: Remove accidental markdown wrapping
        if content.startswith("```"):
            content = content.split("```")[1]

        return json.loads(content)

    except Exception as e:
        print("Spec generation failed:", e)
        return None


# ---------------- PLANNER ----------------
def generate_plan(spec: dict) -> list:
    """
    Converts spec into execution steps.
    """
    if spec and spec.get("task") == "get_user_repos":
        return ["call_github_api", "extract_repo_names"]
    return []


# ---------------- EXECUTOR ----------------
def execute_plan(spec: dict, plan: list):
    """
    Executes GitHub API call.
    """

    if not spec or "username" not in spec:
        return "Invalid specification."

    username = spec["username"]

    url = f"https://api.github.com/users/{username}/repos"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return f"GitHub user '{username}' not found."

        if response.status_code != 200:
            return f"GitHub API error: {response.status_code}"

        data = response.json()

        if not data:
            return "No repositories found."

        # Sort by stars (professional touch)
        sorted_repos = sorted(
            data,
            key=lambda x: x.get("stargazers_count", 0),
            reverse=True
        )

        top_repos = [repo["name"] for repo in sorted_repos]

        return top_repos

    except requests.exceptions.RequestException as e:
        return f"Network error: {e}"


# ---------------- MAIN WORKFLOW ----------------
def github_agent_workflow(user_input: str):
    print("Generating spec using LLM...")
    spec = generate_specification(user_input)

    if not spec:
        return "Spec generation failed."

    print("Generated Spec:", spec)

    plan = generate_plan(spec)

    if not plan:
        return "No execution plan available."

    print("Executing plan...")

    result = execute_plan(spec, plan)

    return result


# ---------------- RUN ----------------
if __name__ == "__main__":
    user_query = input("Enter your request: ")
    output = github_agent_workflow(user_query)
    print("\nResult:", output)
