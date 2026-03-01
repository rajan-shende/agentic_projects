# SDD (Spec driven developement)
'''
User Input
   ↓
Create Spec
   ↓
Create Plan
   ↓
Call GitHub API
   ↓
Return Result
'''

import requests
import logging
user_input = "get rpepos of rajan-shende"

# ---------------- SPEC ----------------
# The Spec Agent converts raw human language into structured machine-readable instructions.

def generate_specification(user_input):
    words = user_input.split()
    if if any(word in user_input.lower() for word in ["repo", "repository", "repositories"]):
        return {
            "task": "get_user_repos",
            "username": words[-1] 
        }


# ---------------- PLANNER ----------------
#  Converts the specification to the step by step execution plan
#  We are returning the lists of actions to be performed.

def generate_plan(specification):
    if specification["task"] == "get_user_repos":
        return ["call_github_api", "list_repo"]


# ---------------- EXECUTOR ----------------
#  step by step execution of planned tasks
#  We are executing the lists of actions.

def execute_plan(spec, plan):
    username = spec["username"]
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        logging.error("USER NOT FOUND EXITING")
    data = response.json()
    repo_names = [repo["name"] for repo in data]
    return repo_names

# ---------------- MAIN WORKFLOW ----------------
def github_agent_workflow(user_input):
    spec = generate_specification(user_input)
    plan = generate_plan(spec)
    result = execute_plan(spec, plan)
    return result


# ---------------- RUN ----------------
if __name__ == "__main__":
    output = github_agent_workflow("Get repo of moeru-ai")
    print("Top Repositories:", output)
