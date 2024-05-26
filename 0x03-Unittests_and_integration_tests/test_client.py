#!/usr/bin/env python3
"""
Parameterize and patch as decorators
"""
from client import (
    GithubOrgClient,
)
from unittest.mock import (
    patch,
    Mock,
    PropertyMock
)
from parameterized import parameterized

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
        response = {"login": org_name, "id":1}
        mock_get_json.return_value = response
        
        client = GithubOrgClient(org_name)
        
        result = client.org
        
        self.assertEqual(result, response)
        
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self, _public_repos_url):
        """
        method for  test_public_repos_url
        """
        with patch('GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = _public_repos_url()
            github_org_client = GithubOrgClient()
            print(github_org_client._public_repos_url)
            mock_public_repos_url.assert_called_once_with()
            
        
if __name__ =="__main__":
    unittest.main()