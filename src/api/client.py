"""
API Module
Provides utilities for accessing remote APIs and services
"""

import requests
from typing import Any, Dict, List, Optional, Union
import logging
import time


class APIClient:
    """Generic API client for remote service access"""
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None,
                 timeout: int = 30, retry_attempts: int = 3):
        """
        Initialize API client
        
        Args:
            base_url: Base URL for the API
            headers: Default headers to include in requests
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts for failed requests
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.logger = logging.getLogger(f"APIClient.{base_url}")
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def _make_request(self, method: str, endpoint: str, 
                     headers: Optional[Dict[str, str]] = None,
                     params: Optional[Dict[str, Any]] = None,
                     data: Optional[Union[Dict, str]] = None,
                     json: Optional[Dict] = None) -> requests.Response:
        """
        Make HTTP request with retry logic
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint
            headers: Additional headers
            params: Query parameters
            data: Request body data
            json: JSON request body
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        request_headers = {**self.headers, **(headers or {})}
        
        for attempt in range(self.retry_attempts):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    headers=request_headers,
                    params=params,
                    data=data,
                    json=json,
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                self.logger.warning(
                    f"Request failed (attempt {attempt + 1}/{self.retry_attempts}): {str(e)}"
                )
                if attempt == self.retry_attempts - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> Union[Dict, List, str]:
        """
        Make GET request
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Additional headers
            
        Returns:
            Response data
        """
        response = self._make_request('GET', endpoint, headers=headers, params=params)
        try:
            return response.json()
        except:
            return response.text
    
    def post(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
             json: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict, List, str]:
        """
        Make POST request
        
        Args:
            endpoint: API endpoint
            data: Request body data
            json: JSON request body
            headers: Additional headers
            
        Returns:
            Response data
        """
        response = self._make_request('POST', endpoint, headers=headers, data=data, json=json)
        try:
            return response.json()
        except:
            return response.text
    
    def put(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
            json: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict, List, str]:
        """
        Make PUT request
        
        Args:
            endpoint: API endpoint
            data: Request body data
            json: JSON request body
            headers: Additional headers
            
        Returns:
            Response data
        """
        response = self._make_request('PUT', endpoint, headers=headers, data=data, json=json)
        try:
            return response.json()
        except:
            return response.text
    
    def delete(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> Union[Dict, List, str]:
        """
        Make DELETE request
        
        Args:
            endpoint: API endpoint
            headers: Additional headers
            
        Returns:
            Response data
        """
        response = self._make_request('DELETE', endpoint, headers=headers)
        try:
            return response.json()
        except:
            return response.text
    
    def patch(self, endpoint: str, data: Optional[Union[Dict, str]] = None,
              json: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None) -> Union[Dict, List, str]:
        """
        Make PATCH request
        
        Args:
            endpoint: API endpoint
            data: Request body data
            json: JSON request body
            headers: Additional headers
            
        Returns:
            Response data
        """
        response = self._make_request('PATCH', endpoint, headers=headers, data=data, json=json)
        try:
            return response.json()
        except:
            return response.text
    
    def set_auth_token(self, token: str, token_type: str = 'Bearer') -> None:
        """
        Set authentication token
        
        Args:
            token: Authentication token
            token_type: Token type (Bearer, Token, etc.)
        """
        self.session.headers.update({'Authorization': f'{token_type} {token}'})
    
    def set_api_key(self, api_key: str, header_name: str = 'X-API-Key') -> None:
        """
        Set API key
        
        Args:
            api_key: API key value
            header_name: Header name for API key
        """
        self.session.headers.update({header_name: api_key})


class PublicAPIExamples:
    """Examples of accessing public APIs"""
    
    @staticmethod
    def get_weather(city: str, api_key: Optional[str] = None) -> Dict:
        """
        Get weather data from OpenWeatherMap API
        Note: Requires API key from openweathermap.org
        
        Args:
            city: City name
            api_key: OpenWeatherMap API key
            
        Returns:
            Weather data
        """
        if not api_key:
            return {"error": "API key required for OpenWeatherMap"}
        
        client = APIClient("https://api.openweathermap.org/data/2.5")
        return client.get("weather", params={"q": city, "appid": api_key, "units": "metric"})
    
    @staticmethod
    def get_github_user(username: str) -> Dict:
        """
        Get GitHub user information
        
        Args:
            username: GitHub username
            
        Returns:
            User data
        """
        client = APIClient("https://api.github.com")
        return client.get(f"users/{username}")
    
    @staticmethod
    def get_github_repos(username: str) -> List[Dict]:
        """
        Get GitHub user repositories
        
        Args:
            username: GitHub username
            
        Returns:
            List of repositories
        """
        client = APIClient("https://api.github.com")
        return client.get(f"users/{username}/repos")
    
    @staticmethod
    def get_random_user() -> Dict:
        """
        Get random user data from randomuser.me API
        
        Returns:
            Random user data
        """
        client = APIClient("https://randomuser.me/api")
        return client.get("")
    
    @staticmethod
    def get_exchange_rates(base_currency: str = 'USD') -> Dict:
        """
        Get exchange rates
        
        Args:
            base_currency: Base currency code
            
        Returns:
            Exchange rates
        """
        client = APIClient("https://api.exchangerate-api.com/v4")
        return client.get(f"latest/{base_currency}")
    
    @staticmethod
    def get_country_info(country: str) -> List[Dict]:
        """
        Get country information
        
        Args:
            country: Country name
            
        Returns:
            Country data
        """
        client = APIClient("https://restcountries.com/v3.1")
        return client.get(f"name/{country}")
    
    @staticmethod
    def search_universities(country: str) -> List[Dict]:
        """
        Search universities by country
        
        Args:
            country: Country name
            
        Returns:
            List of universities
        """
        client = APIClient("http://universities.hipolabs.com")
        return client.get("search", params={"country": country})
