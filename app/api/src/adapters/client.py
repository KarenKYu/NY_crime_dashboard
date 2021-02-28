import requests
from flask import Flask

class Client:
    APP_TOKEN = '1tNkT6rxKKvprTlBlhQWK3t2V'
    ROOT_URL ="https://data.cityofnewyork.us/resource/2fra-mtpn.json"

    def auth_params(self):
        return {'$$app_token':APP_TOKEN}

    def full_params(self, query_params = {'$limit':500000,'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'}):
        params = self.auth_params().copy()
        params.update(query_params)
        return params

    def request_incidents(self, query_params = {'$limit':500000,'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'}):
        return requests.get(f'{self.ROOT_URL}', self.full_params(query_params)).json()

    def request_incident(self, query_params = {'cmplnt_num':604509546}):
        return requests.get(f'{self.ROOT_URL}', self.full_params(query_params)).json()


        #cmplnt_num':'797931560'
        # return f'{self.ROOT_URL}&$$app_token={self.APP_TOKEN}'

    # def request_incident(self, incident_id):
    #     response = requests.get(f"{self.ROOT_URL}/incidents/{incident_id}", self.auth_params())
    #     return response.json()#['response']['incident']

# """Create and configure an instance of the Flask application. you can change the configuration info by changing arguments passed"""
# def create_app(database='foursquare_development', testing = False, debug = True):
#     app = Flask(__name__)
#     app.config.from_mapping(
#         DATABASE=database,
#         DEBUG = debug,
#         TESTING = testing
#     )

# >>> flask1 = create_app(database='foursquare_development', testing = False, debug = True)
# >>>

# """Create and configure an instance of the Flask with all the below hard coded configuration info."""
# def create_app():
#     app = Flask(__name__)
#     app.config.from_mapping(
#         DATABASE='foursquare_development',
#         DEBUG = True,
#         TESTING = False
#     )

# >>> flask2 = create_app()
# >>>  
