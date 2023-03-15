from f_utils import u_http_requests


class WhatsApp:

    def __init__(self, key: str):
        self._host = 'whatsapp-profile-pic.p.rapidapi.com'
        self._key = key
        self._headers = {'X-RapidAPI-Key': self._key,
                         'X-RapidAPI-Host': self._host}

    def tel_to_url(self, tel: str) -> str:
        url = f'https://{self._host}/wspic/url'
        params = {'phone': tel}
        return u_http_requests.get_text(url=url,
                                        params=params,
                                        headers=self._headers)

    def tel_to_pic(self, tel: str, folder: str) -> None:
        url = self.tel_to_url(tel=tel)
        filepath = f'{folder}\\{tel}.jpg'
        u_http_requests.download(url=url, filepath=filepath)

    def __repr__(self):
        return 'Class WhatsApp'
