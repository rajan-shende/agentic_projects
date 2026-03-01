import unittest
import github_agent
from unittest.mock import MagicMock, patch
from github_agent import github_agent_workflow

class TestGithubAgentWorkflow(unittest.TestCase):

    @patch("github_agent.requests.get")
    def test_github_agent_workflow_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"name":"repo1"},
            {"name":"repo2"}
        ]
        mock_get.return_value = mock_response
        result = github_agent_workflow("get all repo of rajan-shende")
        self.assertEqual(result,["repo1","repo2"])

if __name__ == "__main__":
    unittest.main()

