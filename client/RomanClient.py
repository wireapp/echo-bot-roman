import json
import logging

import requests

from api.Configuration import Config

logger = logging.getLogger(__name__)


class RomanClient:
    def __init__(self, config: Config):
        self.url = config.roman_url

    def send_message(self, token: str, payload: dict) -> str:
        logger.debug(f'Sending {payload} to {self.url}/conversation.')
        try:
            r = requests.post(f"{self.url}/conversation", data=json.dumps(payload),
                              headers={"content-type": "application/json", "Authorization": f"Bearer {token}"})
            logger.debug(f'Status code: {r.status_code}')
            j = r.json()
            logger.debug(f'Response: {j}')
            logger.debug(f'Headers: {r.headers}')
            return j
        except Exception as ex:
            logger.error(f'Exception {ex} during sending data to roman. {payload}, url: {self.url}')
            logger.exception(ex)
