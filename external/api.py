# self.data_api = {
#     "code": "33333-TESTE",
#             "create_at": "2021-06-16T16:22:57-03:00",
#             "deadline": "2021-06-16T16:22:57-03:00",
#             "total": 97.03,
#             "status": "A",
#             "payment": "BP",
#             "client": "200"
# }

import requests
from pprint import pprint
_print = print
print = pprint


class Api():

    def isPostPedido(self, data):
        url = 'http://127.0.0.1:8000/api/apipedidos/'

        response = requests.post(url=url, json=data)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f'POST status code - {response.status_code}')
            print(f'POST Reason - {response.reason}')
            # print(f'Reason - {response.text}')
            print(f'POST Reason - {response.json()}')

        else:
            # Falha
            print(f'POST status code - {response.status_code}')
            print(f'POST Reason - {response.reason}')
            print(f'POST Reason - {response.text}')
            # print(f'Reason - {response.content}')

    def isPostEndereco(self, data):
        url = 'http://127.0.0.1:8000/api/apiendereco/'

        response = requests.post(url=url, json=data)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f'POST status code - {response.status_code}')
            print(f'POST Reason - {response.reason}')
            # print(f'Reason - {response.text}')
            print(f'POST Reason - {response.json()}')
            return response.json()

        else:
            # Falha
            print(f'POST status code - {response.status_code}')
            print(f'POST Reason - {response.reason}')
            print(f'POST Reason - {response.text}')
            # print(f'Reason - {response.content}')

    def isPostCliente(self, data):
        # print(data)
        url = 'http://127.0.0.1:8000/api/apiclientes/'

        response = requests.post(url=url, json=data)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f'POST  status code - {response.status_code}')
            print(f'POST  Reason - {response.reason}')
            # print(f'Reason - {response.text}')
            print(f'POST  Reason - {response.json()}')

        else:
            # Falha
            print(f'POST status code - {response.status_code}')
            print(f'POST Reason - {response.reason}')
            print(f'POST Reason - {response.text}')
            # print(f'Reason - {response.content}')

    def isPutCliente(self, data, uid):

        url = f'http://127.0.0.1:8000/api/apiclientes/{uid}/?format=json'

        response = requests.put(url=url, json=data)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f'PUT status code - {response.status_code}')
            print(f'PUT Reason - {response.reason}')
            # print(f'Reason - {response.text}')
            print(f'PUT Reason - {response.json()}')

        else:
            # Falha
            print(f'PUT status code - {response.status_code}')
            print(f'PUT Reason - {response.reason}')
            print(f'PUT Reason - {response.text}')
            # print(f'Reason - {response.content}')

    def isGetCliente(self):
        url = 'http://127.0.0.1:8000/api/apiclientes/'
        # data = {}
        response = requests.get(url=url)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f' GET status code - {response.status_code}')
            print(f'GET Reason - {response.reason}')
            # print(f'Reason - {response.text}')
            print(f'GET Reason - {response.json()}')
            return response.json()

        else:
            # Falha
            print(f'GET status code - {response.status_code}')
            print(f'GET Reason - {response.reason}')
            print(f'GET Reason - {response.text}')
            # print(f'Reason - {response.content}')

    def isGetEndereco(self):
        url = 'http://127.0.0.1:8000/api/apiendereco/'
        # data = {}
        response = requests.get(url=url)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f' GET status code - {response.status_code}')
            print(f'GET Reason - {response.reason}')
            # print(f'Reason - {response.text}')
            print(f'GET Reason - {response.json()}')
            return response.json()

        else:
            # Falha
            print(f'GET status code - {response.status_code}')
            print(f'GET Reason - {response.reason}')
            print(f'GET Reason - {response.text}')
            # print(f'Reason - {response.content}')

    def isDeleteCliente(self, uid):
        url = f'http://127.0.0.1:8000/api/apiclientes/{uid}/?format=json'

        response = requests.delete(url=url)

        if response.status_code >= 200 and response.status_code <= 299:
            # sucesso
            print(f'DELETE status code - {response.status_code}')
            print(f'DELETE Reason - {response.reason}')
            # # print(f'Reason - {response.text}')
            # print(f'DELETE Reason - {response.json()}')

        else:
            # Falha
            print(f'DELETE status code - {response.status_code}')
            print(f'Reason - {response.content}')
