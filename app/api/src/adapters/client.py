import requests
from flask import Flask

class Client:
    APP_TOKEN = '1tNkT6rxKKvprTlBlhQWK3t2V'
    ROOT_URL ="https://data.cityofnewyork.us/resource/2fra-mtpn.json"

    def auth_params(self):
        return {'$$app_token':self.APP_TOKEN}

    def full_params(self, query_params = {'$limit':500000,'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'}):
        params = self.auth_params().copy()
        params.update(query_params)
        return params

    def request_incidents(self, query_params = {'$limit':500000,'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'}):
        return requests.get(f'{self.ROOT_URL}', self.full_params(query_params)).json()

    def request_incident(self, query_params = {'cmplnt_num':604509546}):
        return requests.get(f'{self.ROOT_URL}', self.full_params(query_params)).json()
