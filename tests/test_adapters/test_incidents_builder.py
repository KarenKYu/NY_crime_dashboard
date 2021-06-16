#from app.api.src.models.incident import Incident
import pytest
import psycopg2
from decimal import *
from app.api.src.db.db import save
#from api.src.models import incident, location, complaint
from app.api.src.adapters.incidents_builder import Builder, IncidentBuilder, LocationBuilder, ComplaintBuilder

# conn = psycopg2.connect(database = 'nypd_complaints', 
#                         user = 'postgres', 
#                         password = 'postgres')

# cursor = conn.cursor()

incident_details = [{'cmplnt_num': '604509546', 'addr_pct_cd': '14', 'boro_nm': 'MANHATTAN', 'cmplnt_fr_dt': '2020-09-26T00:00:00.000', 
'cmplnt_fr_tm': '19:30:00', 'crm_atpt_cptd_cd': 'COMPLETED', 'juris_desc': 'N.Y. POLICE DEPT', 'ky_cd': '341', 
'law_cat_cd': 'MISDEMEANOR', 'ofns_desc': 'PETIT LARCENY', 'pd_cd': '339.0', 'pd_desc': 'LARCENY,PETIT FROM OPEN AREAS,', 
'prem_typ_desc': 'STREET', 'rpt_dt': '2020-09-27T00:00:00.000', 
'location_1': {'type': 'Point', 'coordinates': [-73.99535613299997, 40.75469651000003]}, 'x_coord_cd': '985537',
 'y_coord_cd': '214230', 'latitude': '40.75469651000003', 'longitude': '-73.99535613299997'}]
 
 @pytest.fixture()
 def db_with_one_incident():
    insert_into = 'INSERT INTO incidents ('incident_num', 'incident_date','incident_time) VALUES (%s, %s, %s)''
    cursor.execute(insert_into, ('604509546', '2020-09-26T00:00:00.000', '19:30:00'))
    cursor.commit()
# def test_Builder(incident_json):
#    #takes in list of json files and outputs incident, location and complaint objs for each json
#     sb = Builder()
#     assert sb.run(self, incident_details, conn, cursor) 

def test_IncidentBuilder():
    builder = IncidentBuilder()
    selected_attr = builder.select_attributes(incident_details)
    assert selected_attr == {"incident_num":'604509546', 'incident_date':'2020-09-26T00:00:00.000', 'incident_time':'19:30:00'}
    obj = builder.run(incident_details, conn, cursor)
    assert obj.__dict__ == {"incident_num":'604509546', 'incident_date':'2020-09-26T00:00:00.000', 'incident_time':'19:30:00'}

def test_LocationBuilder():
    builder = LocationBuilder()
    selected_attr = builder.select_attributes(incident_details)
    assert selected_attr == {'borough':'MANHATTAN','latitude':'40.75469651000003','longitude':'-73.99535613299997','setting':'STREET','precinct':'14'}
    obj = builder.run(incident_details, conn, cursor)
    assert obj.__dict__ == {'id': 12653, 'borough': 'MANHATTAN', 'latitude': Decimal('40.754697'), 'longitude': Decimal('-73.995356'), 'setting': 'STREET', 'precinct': 14}

def test_ComplaintBuilder():  
    builder = ComplaintBuilder()
    selected_attr = builder.select_attributes(incident_details)
    assert selected_attr == {'desc_offense':'PETIT LARCENY', 'level_offense':'MISDEMEANOR', 'dept_juris':'N.Y. POLICE DEPT'}
    obj = builder.run(incident_details, conn, cursor)
    assert obj.__dict__ == {'id': 12652, 'desc_offense':'PETIT LARCENY', 'level_offense':'MISDEMEANOR', 'dept_juris':'N.Y. POLICE DEPT'}