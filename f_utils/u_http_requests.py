import requests

def get(url: str,
		params: dict,
		headers: dict) -> str:
	return requests.request('GET', url, headers=headers, params=params).text

