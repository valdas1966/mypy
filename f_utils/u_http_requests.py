from requests import request, get
import json


def get_text(url: str,
			 params: dict,
			 headers: dict) -> str:
	response = request('GET', url, headers=headers, params=params)
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
