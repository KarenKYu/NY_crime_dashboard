import requests

class NYPDComplaintsClient:
    def run(self):
        self.complaints_data = self.retrieve_complaints()

# takes in user search parameters and returns query string
    def build_query(**params):
        root_url ="https://data.cityofnewyork.us/resource/2fra-mtpn.json?"
  	query ="".join([f"{k}={v}&" for k,v in params.items()])
        return root_url+query

# takes in query string and return json response from api
    def retrieve_complaints(self.build_query):
        return requests.get(self.build_query).json()

# takes json data and create complaints with Complaint class object
    def create_complaint(self, complaints_data):
        complaint = Complaint(


app_token = '1tNkT6rxKKvprTlBlhQWK3t2V'
client = Socrata(domain='data.cityofnewyork.us', app_token=app_token)
data = client.get('9w7m-hzhe', content_type = 'json')

def retrieve_data(payload):
  app_token = '1tNkT6rxKKvprTlBlhQWK3t2V'
  root_url = f'https://data.cityofnewyork.us/resource/9w7m-hzhe.json?&$$app_token={app_token}'
  return requests.get(root_url, params=payload).json()

payload = {'cuisine_description': 'American', 'zipcode': 11229, '$limit':2}

american2 = retrieve_data(payload)
american2