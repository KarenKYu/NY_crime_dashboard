import app.api.src.models as models
import app.api.src.db as db
import app.api.src.adapters as adapters
import psycopg2

class RequestAndBuild:
    def __init__(self):
        self.client = adapters.Client() #create an instance of the Client class - from client.py file
        self.builder = adapters.Builder() # create an instance of the Builder class -from incidents_builder.py file
        self.conn = psycopg2.connect(database = 'nypd_complaints', 
                user = 'postgres', 
                password = 'postgres')
        self.cursor = self.conn.cursor()


    def run(self, query_params = {'$limit':50000}):
        incidents = self.client.request_incidents(query_params) #hit api and retrieves json files
        incident_ids = [incident['cmplnt_num'] for incident in incidents] #gets all incident #s
        incident_objs = []
        for incident_id in incident_ids: #hit api and retrieve individual incidents by incident #
            incident_details = self.client.request_incident(query_params = {'cmplnt_num':incident_id})
            incident_obj = self.builder.run(incident_details, self.conn, self.cursor) #takes json file for one incident and builds objs for incident, location and complaint
            incident_objs.append(incident_obj)
        return incident_objs


# >>> incid.request_incidents(query_params = {'$limit':2,'BORO_NM': 'MANHATTAN', 'OFNS_DESC': 'PETIT LARCENY'})
incident_jsons = [{'cmplnt_num': '604509546', 'addr_pct_cd': '14', 'boro_nm': 'MANHATTAN', 'cmplnt_fr_dt': '2020-09-26T00:00:00.000', 
'cmplnt_fr_tm': '19:30:00', 'crm_atpt_cptd_cd': 'COMPLETED', 'juris_desc': 'N.Y. POLICE DEPT', 'ky_cd': '341', 
'law_cat_cd': 'MISDEMEANOR', 'ofns_desc': 'PETIT LARCENY', 'pd_cd': '339.0', 'pd_desc': 'LARCENY,PETIT FROM OPEN AREAS,', 
'prem_typ_desc': 'STREET', 'rpt_dt': '2020-09-27T00:00:00.000', 
'location_1': {'type': 'Point', 'coordinates': [-73.99535613299997, 40.75469651000003]}, 'x_coord_cd': '985537',
 'y_coord_cd': '214230', 'latitude': '40.75469651000003', 'longitude': '-73.99535613299997'}, 
 {'cmplnt_num': '912654499', 'addr_pct_cd': '19', 'boro_nm': 'MANHATTAN', 'cmplnt_fr_dt': '2020-09-09T00:00:00.000', 
 'cmplnt_fr_tm': '18:00:00', 'cmplnt_to_dt': '2020-09-09T00:00:00.000', 'cmplnt_to_tm': '18:05:00', 
 'crm_atpt_cptd_cd': 'COMPLETED', 'juris_desc': 'N.Y. POLICE DEPT', 'ky_cd': '341', 'law_cat_cd': 'MISDEMEANOR', 
 'loc_of_occur_desc': 'INSIDE', 'ofns_desc': 'PETIT LARCENY', 'pd_cd': '349.0', 'pd_desc': 'LARCENY,PETIT OF LICENSE PLATE', 
 'prem_typ_desc': 'RESIDENCE-HOUSE', 'rpt_dt': '2020-09-17T00:00:00.000', 'location_1': {'type': 'Point', 'coordinates': [-73.96856394899999, 40.76894302300008]}, 
 'x_coord_cd': '992958', 'y_coord_cd': '219422', 'latitude': '40.76894302300008', 'longitude': '-73.96856394899999'}]