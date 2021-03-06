from api.src.models import *
import api.src.adapters as adapters
from api.src.db.db import dev_conn
from api.src.adapters.client import Client


conn= dev_conn
cursor = conn.cursor()

incident = Incident.find_by_incident_num('604509546',cursor)
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

#  nypd_complaints=# SELECT * FROM complaints;
#  id |         desc_offense         | level_offense |    dept_juris
# ----+------------------------------+---------------+------------------
#   1 | THEFT-FRAUD                  | FELONY        | N.Y. POLICE DEPT
#   2 | ASSAULT 3 & RELATED OFFENSES | MISDEMEANOR   | N.Y. POLICE DEPT
#   3 | ROBBERY                      | FELONY        | N.Y. POLICE DEPT
#   4 | MISCELLANEOUS PENAL LAW      | FELONY        | N.Y. POLICE DEPT
#   5 | PETIT LARCENY                | MISDEMEANOR   | N.Y. POLICE DEPT
# (5 rows)
# nypd_complaints=# SELECT * FROM incidents;  
#  id | incident_num | complaint_id | incident_date | incident_time | location_id
# ----+--------------+--------------+---------------+---------------+-------------
#   1 |    797931560 |            1 | 2020-09-16    | 00:30:00      |           1
#   2 |    664557183 |            2 | 2020-06-24    | 21:20:00      |           2
#   3 |    453437883 |            3 | 2020-09-28    | 20:00:00      |           3
#   4 |    949043828 |            4 | 2020-07-26    | 01:08:00      |           4
#   5 |    604509546 |            5 | 2020-09-26    | 19:30:00      |           5
# (5 rows)
# nypd_complaints=# SELECT * FROM locations; 
#  id |  borough  |     latitude      |     longitude      |        setting         | precinct
# ----+-----------+-------------------+--------------------+------------------------+----------
#   1 | MANHATTAN | 40.83730401400004 | -73.94809867999999 | RESIDENCE - APT. HOUSE |       33
#   2 | MANHATTAN | 40.82413968200007 | -73.94097291399999 | STREET                 |       32
#   3 | BRONX     | 40.88144124600007 | -73.83235353999999 | OTHER                  |       47
#   4 | BRONX     | 40.83527732600004 | -73.85403335799998 | RESIDENCE-HOUSE        |       43
#   5 | MANHATTAN | 40.75469651000003 | -73.99535613299997 | STREET                 |       14
#https://data.cityofnewyork.us/Public-Safety/NYPD-Complaint-Map-Year-to-Date-/2fra-mtpn