#!/usr/bin/env python3
"""
Parameterize and patch as decorators
"""
from client import (
    GithubOrgClient,
)
from unittest.mock import (
    patch
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

if __name__ =="__main__":
    unittest.main()