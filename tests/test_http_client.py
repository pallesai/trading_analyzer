"""Tests for the HTTP client module."""

from unittest.mock import Mock, patch

import pytest
import requests

from trading_analyzer.http_client.client import HTTPClient


class TestHTTPClient:
    """Test cases for HTTPClient class."""

    def test_init_default_values(self):
        """Test HTTPClient initialization with default values."""
        client = HTTPClient()
        
        assert client.base_url == ""
        assert client.timeout == 30
        assert client.session is not None
        
        client.close()

    def test_init_with_custom_values(self):
        """Test HTTPClient initialization with custom values."""
        base_url = "https://api.example.com"
        timeout = 60
        headers = {"Authorization": "Bearer token"}
        
        client = HTTPClient(base_url=base_url, timeout=timeout, headers=headers)
        
        assert client.base_url == base_url
        assert client.timeout == timeout
        assert "Authorization" in client.session.headers
        
        client.close()

    def test_build_url_with_base_url(self):
        """Test URL building with base URL."""
        client = HTTPClient(base_url="https://api.example.com")
        
        # Test relative endpoint
        url = client._build_url("/users")
        assert url == "https://api.example.com/users"
        
        # Test endpoint without leading slash
        url = client._build_url("users")
        assert url == "https://api.example.com/users"
        
        client.close()

    def test_build_url_without_base_url(self):
        """Test URL building without base URL."""
        client = HTTPClient()
        
        # Test full URL
        url = client._build_url("https://api.example.com/users")
        assert url == "https://api.example.com/users"
        
        # Test relative endpoint
        url = client._build_url("/users")
        assert url == "/users"
        
        client.close()

    @patch('trading_analyzer.http_client.client.requests.Session.get')
    def test_get_success(self, mock_get):
        """Test successful GET request."""
        # Setup mock
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = HTTPClient()
        response = client.get("https://api.example.com/users")
        
        assert response == mock_response
        mock_get.assert_called_once()
        client.close()

    @patch('trading_analyzer.http_client.client.requests.Session.get')
    def test_get_with_params(self, mock_get):
        """Test GET request with parameters."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        client = HTTPClient()
        params = {"page": 1, "limit": 10}
        client.get("https://api.example.com/users", params=params)
        
        mock_get.assert_called_once_with(
            url="https://api.example.com/users",
            params=params,
            headers=None,
            timeout=30
        )
        client.close()

    @patch('trading_analyzer.http_client.client.requests.Session.post')
    def test_post_with_json(self, mock_post):
        """Test POST request with JSON data."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        client = HTTPClient()
        json_data = {"name": "John", "email": "john@example.com"}
        client.post("https://api.example.com/users", json_data=json_data)
        
        mock_post.assert_called_once_with(
            url="https://api.example.com/users",
            data=None,
            json=json_data,
            params=None,
            headers=None,
            timeout=30
        )
        client.close()

    def test_context_manager(self):
        """Test HTTPClient as context manager."""
        with HTTPClient() as client:
            assert client.session is not None
        # Session should be closed after context exit

    @pytest.mark.integration
    def test_real_get_request(self):
        """Integration test with real HTTP request."""
        client = HTTPClient()
        try:
            response = client.get("https://httpbin.org/get")
            assert response.status_code == 200
            data = response.json()
            assert "url" in data
        except requests.RequestException:
            pytest.skip("Network request failed - skipping integration test")
        finally:
            client.close()
