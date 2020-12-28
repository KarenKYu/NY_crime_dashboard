import requests

class Client:
    APP_TOKEN = '1tNkT6rxKKvprTlBlhQWK3t2V'
    ROOT_URL ="https://data.cityofnewyork.us/resource/2fra-mtpn.json?"

    def auth_params(self):
        return {'app_token':self.APP_TOKEN}

    def full_params(self, query_params = {'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'}):
        params = self.auth_params().copy()
        params.update(query_params)
        return params

    def request_incidents(self, query_params = {'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'})
        return requests.get(f'{self.ROOT_URL}', self.full_params(query_params)).json()

        return f'{self.ROOT_URL}&$$app_token={self.APP_TOKEN}'