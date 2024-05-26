#!/usr/bin/env python3
"""
Parameterize a unit test
"""
import unittest
from unittest.mock import (
    patch,
    Mock
)
from utils import (
    access_nested_map,
    get_json,
    memoize
    
)
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """
     TestAccessNestedMap class 
     that inherits from unittest.TestCase
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Testing the access nested map
        """
        self.assertEqual(access_nested_map(nested_map, path),expected)
    
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Implement TestAccessNestedMap.test_access_nested_map_exception
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], path[next(i for i, key in enumerate(path) if key not in nested_map)])
        
class TestGetJson(unittest.TestCase):
    """
    TestGetJson that inherits unittest.TestCase
    """
    def test_get_json(self):
        """
        testing the get_json module
        """
        test_cases = [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
        
        for test_url, test_payload in test_cases:
            with patch("requests.get") as mock_get:
                
                mock_response = Mock()
                mock_response.json.return_value = test_payload
                mock_get.return_value = mock_response
                
                result = get_json(test_url)

class TestMemoize(unittest.TestCase):
    """
    class for testing the memoize decorator
    """
    def test_memoize(self):
        """
        method for testing the memoize 
        """
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
            
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            test_instance = TestClass()
            
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            
            mock_method.assert_called_once()
            
            self.assertEqual(result1, 42)
            self.assertEqual(result1, 42)

if __name__ == "__main__":
    unittest.main()