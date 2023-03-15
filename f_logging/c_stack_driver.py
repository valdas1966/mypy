from google.cloud import logging


class StackDriver:

    def __init__(self, json_key: str, name: str = 'StackDriver'):
        self._json_key = json_key
        self._name = name
        self._client = logging.Client.from_service_account_json(json_key)
        self._logger = self._client.logger(name)

    def log(self, struct: dict) -> None:
        self._logger.log_struct(struct)

    def close(self):
        self._client.close()

    def __del__(self):
        self.close()
