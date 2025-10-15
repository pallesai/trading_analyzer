"""
Simple and generic HTTP client with GET and POST methods.
"""

import json
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

import requests


class HTTPClient:
    """
    A simple and generic HTTP client for making GET and POST requests.
    """
    
    def __init__(self, base_url: str = "", timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the HTTP client.
        
        Args:
            base_url (str): Base URL for all requests
            timeout (int): Request timeout in seconds
            headers (Dict[str, str]): Default headers to include in all requests
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        default_headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Generic-HTTP-Client/1.0'
        }
        
        if headers:
            default_headers.update(headers)
            
        self.session.headers.update(default_headers)
    
    def _build_url(self, endpoint: str) -> str:
        """
        Build the full URL from base URL and endpoint.
        
        Args:
            endpoint (str): API endpoint
            
        Returns:
            str: Full URL
        """
        if endpoint.startswith('http'):
            return endpoint
        
        if self.base_url:
            return urljoin(self.base_url + '/', endpoint.lstrip('/'))
        
        return endpoint
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, 
            headers: Optional[Dict[str, str]] = None, timeout: Optional[int] = None) -> requests.Response:
        """
        Make a GET request.
        
        Args:
            endpoint (str): API endpoint or full URL
            params (Dict[str, Any]): Query parameters
            headers (Dict[str, str]): Additional headers for this request
            timeout (int): Request timeout (overrides default)
            
        Returns:
            requests.Response: Response object
            
        Raises:
            requests.RequestException: If request fails
        """
        url = self._build_url(endpoint)
        request_timeout = timeout or self.timeout
        
        try:
            response = self.session.get(
                url=url,
                params=params,
                headers=headers,
                timeout=request_timeout
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"GET request failed for {url}: {str(e)}")
    
    def post(self, endpoint: str, data: Optional[Union[Dict[str, Any], str]] = None,
             json_data: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None, timeout: Optional[int] = None) -> requests.Response:
        """
        Make a POST request.
        
        Args:
            endpoint (str): API endpoint or full URL
            data (Union[Dict[str, Any], str]): Form data or raw string data
            json_data (Dict[str, Any]): JSON data to send in request body
            params (Dict[str, Any]): Query parameters
            headers (Dict[str, str]): Additional headers for this request
            timeout (int): Request timeout (overrides default)
            
        Returns:
            requests.Response: Response object
            
        Raises:
            requests.RequestException: If request fails
        """
        url = self._build_url(endpoint)
        request_timeout = timeout or self.timeout
        
        try:
            response = self.session.post(
                url=url,
                data=data,
                json=json_data,
                params=params,
                headers=headers,
                timeout=request_timeout
            )
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"POST request failed for {url}: {str(e)}")
    
    def get_json(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str, str]] = None, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Make a GET request and return JSON response.
        
        Args:
            endpoint (str): API endpoint or full URL
            params (Dict[str, Any]): Query parameters
            headers (Dict[str, str]): Additional headers for this request
            timeout (int): Request timeout (overrides default)
            
        Returns:
            Dict[str, Any]: JSON response data
            
        Raises:
            requests.RequestException: If request fails
            json.JSONDecodeError: If response is not valid JSON
        """
        response = self.get(endpoint, params, headers, timeout)
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Failed to decode JSON response: {str(e)}")
    
    def post_json(self, endpoint: str, json_data: Optional[Dict[str, Any]] = None,
                  params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None,
                  timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Make a POST request with JSON data and return JSON response.
        
        Args:
            endpoint (str): API endpoint or full URL
            json_data (Dict[str, Any]): JSON data to send in request body
            params (Dict[str, Any]): Query parameters
            headers (Dict[str, str]): Additional headers for this request
            timeout (int): Request timeout (overrides default)
            
        Returns:
            Dict[str, Any]: JSON response data
            
        Raises:
            requests.RequestException: If request fails
            json.JSONDecodeError: If response is not valid JSON
        """
        response = self.post(endpoint, json_data=json_data, params=params, headers=headers, timeout=timeout)
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Failed to decode JSON response: {str(e)}")
    
    def close(self):
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
