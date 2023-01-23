import json
import requests


class T4CApi:
    def __init__(self, api_token,licensekey, host='https://api-t4cnext.lely.com'):
        self.host = host
        self.headers = {'Authorization': f'{api_token}', 'Content-Type': 'application/json',
                        'licensekey': f'{licensekey}'}

    def save_batch_routing(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/batch/routing', json=data, headers=self.headers)
        return self._handle_response(response)

    def save_batch_abortion(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/batch/abortion', json=data, headers=self.headers)
        return self._handle_response(response)

    def get_batch_pregcheck_preset(self, animal_ids):
        response = requests.get(f'https://api-t4cnext.lely.com/api/batch/pregnancycheck-preset?animalIds={animal_ids}',
                                headers=self.headers)
        return self._handle_response(response)

    def save_batch_pregcheck(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/batch/pregnancycheck', json=data,
                                 headers=self.headers)
        return self._handle_response(response)

    def post_batch_animal(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/batch/animal', json=data, headers=self.headers)
        return self._handle_response(response)

    def post_batch_routings(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/batch/endrouting', json=data, headers=self.headers)
        return self._handle_response(response)

    def save_batch_heat(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/batch/heat', json=data, headers=self.headers)
        return self._handle_response(response)

    def _handle_response(self, response):
        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise ValueError(f'Error code {response.status_code} : {response.text}')

    def get_milksamplings_list(self, production_date):
        url = self.host + '/api/milksamplings/bottle?productionDate=' + production_date
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def saveBatchInsemination(self, data):
        response = requests.post('https://api-t4cnext.lely.com/api/cowcard/insemination/batch',
                                 json=data,
                                 headers=self.headers)
        return self._handle_response(response)

    def get_animals(self, filter=''):
        url = self.host + '/api/animal/animals?' + filter
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)

    def get_sires(self, filter=''):
        response = requests.get(self.host + '/api/sires?' + filter, headers=self.headers)
        return self._handle_response(response)

    def save_sire(self, data):
        response = requests.post(self.host + '/api/v2/sire', json=data, headers=self.headers)
        return self._handle_response(response)

