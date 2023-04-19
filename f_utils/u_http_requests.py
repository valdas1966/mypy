from requests import request, get
import json


def get_response(url: str, params: dict, headers: dict):
	return request('GET', url, params=params, headers=headers)

def get_text(url: str,
			 params: dict,
			 headers: dict) -> str:
	response = get_response(url=url, params=params, headers=headers)
	return response.text


def get_dict(url: str,
			 params: dict,
			 headers: dict) -> dict:
	text = get_text(url=url, params=params, headers=headers)
	return json.loads(s=text)


def download(url: str, filepath: str):
	response = get(url)
	with open(filepath, 'wb') as f:
		f.write(response.content)
