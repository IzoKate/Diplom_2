import json
from urllib.error import HTTPError

import allure
import pytest
import requests

from constants import Constants


class RequestProcessing:
    def update_headers(self, additional_headers):
        default_headers = {}
        if additional_headers:
           default_headers.update(additional_headers)
        return default_headers


    @allure.step("Отправляем запрос")
    def make_request(self, r_type, url: str, data=None, headers= None):
        headers = self.update_headers(headers)
        try:
            if r_type in ('get', 'delete', 'put'):
                self.response = getattr(requests, r_type)(url=url, params=data, headers=headers)
                return self.response
            elif r_type in ('patch'):
                self.response = getattr(requests, r_type)(url=url,headers=headers, data=json.dumps(data))
                return self.response
            else:
                self.response = getattr(requests, r_type)(url, data=json.dumps(data), headers=headers)
                allure.attach(f'Статус ответа {self.response.status_code}')
                return self.response
        except HTTPError as e:
            pytest.fail(f'Ошибка в запросе {e}\n{self.response.text()}')
        except json.decoder.JSONDecodeError as e:
            pytest.fail(f'Ошибка в запросе {e}\n{self.response.text()}')
