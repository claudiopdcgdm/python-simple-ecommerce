import requests
from pprint import pprint
_print = print
print = pprint


class Api():

    def isPostPedido(self, data):
        url = 'https://claudiomorais.herokuapp.com/api/apipedidos/'

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
        url = 'https://claudiomorais.herokuapp.com/api/apiendereco/'

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
        url = 'https://claudiomorais.herokuapp.com/api/apiclientes/'

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

        url = f'https://claudiomorais.herokuapp.com/api/apiclientes/{uid}/?format=json'

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
        url = 'https://claudiomorais.herokuapp.com/api/apiclientes/'
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
        url = 'https://claudiomorais.herokuapp.com/api/apiendereco/'
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
        url = f'https://claudiomorais.herokuapp.com/api/apiclientes/{uid}/?format=json'

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
