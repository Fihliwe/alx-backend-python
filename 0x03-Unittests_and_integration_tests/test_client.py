#!/usr/bin/env python3
"""
Parameterize and patch as decorators
"""
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
import unittest


class TestGithubOrgClient(unittest.TestCase):
    """
    class for TestGithubOrgClient
    """
    @parameterized.expand([
        ("google", ),
        ("abc", ),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        test org method
        """
        response = {"login": org_name, "id": 1}
        mock_get_json.return_value = response

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, response)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_public_repos_url):
        """
        method for test_public_repos_url
        """
        mock_public_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
        github_org_client = GithubOrgClient("test-org")
        
        result = github_org_client._public_repos_url
        
        self.assertEqual(result, "https://api.github.com/orgs/test-org/repos")
        mock_public_repos_url.assert_called_once_with()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        method for test_public_repos
        """
        mock_public_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("test-org")
        result = client.public_repos()

        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])   
    def test_has_license(self, repo, license_key, expected):
        """
        method for test_has_license
        """
        client = GithubOrgClient("some_org")
        assert client.has_license(repo, license_key) == expected
    
@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload, 
     "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the class by patching requests.get."""
        cls.get_patcher = patch('requests.get', side_effect=cls.get_side_effect)
        cls.mock_get = cls.get_patcher.start()
    
    @classmethod
    def tearDownClass(cls):
        """Tear down the class by stopping the patcher."""
        cls.get_patcher.stop()
    
    @classmethod
    def get_side_effect(cls, url):
        """Side effect function to mock requests.get().json() behavior."""
        if url == "https://api.github.com/orgs/apache":
            return Mock(json=lambda: cls.org_payload)
        elif url == "https://api.github.com/orgs/apache/repos":
            return Mock(json=lambda: cls.repos_payload)
        return None
    
    def test_public_repos(self):
        """Test the public_repos method."""
        client = GithubOrgClient("apache")
        self.assertEqual(client.public_repos(), self.expected_repos)
    
     
if __name__ == "__main__":
    unittest.main()
