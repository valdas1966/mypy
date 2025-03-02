from f_http.request import RequestGet, ResponseAPI
from unittest.mock import patch, Mock
from typing import Generator
import requests
import pytest


# Sample JSON response for successful API request
SAMPLE_SUCCESS_RESPONSE = {"id": 1, "name": "Alice"}
SAMPLE_INVALID_JSON_RESPONSE = "<html>Not JSON</html>"  # Simulate invalid JSON

# Mock URL for testing
VALID_URL = "https://jsonplaceholder.typicode.com/posts/1"
INVALID_URL = "https://jsonplaceholder.typicode.com/posts/99999"
FAKE_URL = "https://invalid-url.com"

@pytest.fixture
def mock_requests_get() -> Generator[Mock, None, None]:
    """Fixture to mock requests.get()"""
    with patch("requests.get") as mock_get:
        yield mock_get

def test_get_successful_request(mock_requests_get):
    """Test if get() correctly handles a valid API request (200 OK)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = SAMPLE_SUCCESS_RESPONSE
    mock_response.elapsed.total_seconds.return_value = 0.12

    mock_requests_get.return_value = mock_response

    response = RequestGet.get(VALID_URL)

    assert isinstance(response, ResponseAPI)
    assert response.status == 200
    assert response.is_valid
    assert response.data == SAMPLE_SUCCESS_RESPONSE
    assert response.elapsed == 0.12
    assert response.reason == "Request was successful."

def test_get_not_found(mock_requests_get):
    """Test if get() correctly handles a 404 Not Found response."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"error": "Not found"}
    mock_response.elapsed.total_seconds.return_value = 0.15

    mock_requests_get.return_value = mock_response

    response = RequestGet.get(INVALID_URL)

    assert isinstance(response, ResponseAPI)
    assert response.status == 404
    assert not response.is_valid
    assert response.data == {"error": "Not found"}
    assert response.elapsed == 0.15
    assert response.reason == "Not Found: The requested resource does not exist."

def test_get_invalid_json_response(mock_requests_get):
    """Test if get() correctly handles a response that is not JSON."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Invalid JSON", "", 0)
    mock_response.elapsed.total_seconds.return_value = 0.2

    mock_requests_get.return_value = mock_response

    response = RequestGet.get(VALID_URL)

    assert isinstance(response, ResponseAPI)
    assert response.status == 200
    assert response.is_valid
    assert response.data == {"error": "Invalid JSON response"}
    assert response.elapsed == 0.2
    assert response.reason == "Request was successful."

def test_get_network_error(mock_requests_get):
    """Test if get() correctly handles a network failure."""
    mock_requests_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

    response = RequestGet.get(FAKE_URL)

    assert isinstance(response, ResponseAPI)
    assert response.status == 0  # No response received
    assert not response.is_valid
    assert "Failed to connect" in response.data["error"]
    assert response.elapsed == 0.0
    assert response.reason == "Network error: No response from server (timeout, DNS failure, or no internet)."

def test_get_timeout(mock_requests_get):
    """Test if get() correctly handles a request timeout."""
    mock_requests_get.side_effect = requests.exceptions.Timeout("Request timed out")

    response = RequestGet.get(FAKE_URL)

    assert isinstance(response, ResponseAPI)
    assert response.status == 0  # No response received
    assert not response.is_valid
    assert "Request timed out" in response.data["error"]
    assert response.elapsed == 0.0
    assert response.reason == "Network error: No response from server (timeout, DNS failure, or no internet)."

def test_get_server_error(mock_requests_get):
    """Test if get() correctly handles a 500 Internal Server Error."""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"error": "Internal server error"}
    mock_response.elapsed.total_seconds.return_value = 0.25

    mock_requests_get.return_value = mock_response

    response = RequestGet.get(VALID_URL)

    assert isinstance(response, ResponseAPI)
    assert response.status == 500
    assert not response.is_valid
    assert response.data == {"error": "Internal server error"}
    assert response.elapsed == 0.25
    assert response.reason == "Server Error (500): The server encountered an error."
