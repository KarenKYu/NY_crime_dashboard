import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters
import psycopg2

#incident_details == list of dictionaries
class Builder:
    def run(self, incident_details, conn, cursor):
        incident = IncidentBuilder().run(incident_details, conn, cursor)
        print(incident.__dict__)
        if incident.exists:
            # {'incident': incident}#, 'location': incident.location(cursor), 
                    #'complaint_type': incident.complaint_type(cursor)}
            location = LocationBuilder().run(incident_details, conn, cursor)
            complaint = ComplaintBuilder().run(incident_details, conn, cursor)
            incident.location_id = location.id
            incident.complaint_id = complaint.id
            incident = db.save(incident, conn, cursor)
            return {'incident': incident, 'location': location, 'complaint_type': incident.complaint_type}

class IncidentBuilder:
    attributes = ['incident_num', 'incident_date','incident_time']

    def select_attributes(self, incident_details):
        for incident in incident_details:
            incident_num = incident['cmplnt_num']
            incident_date = incident['cmplnt_fr_dt']
            incident_time = incident['cmplnt_fr_tm'] 
            return dict(zip(self.attributes, [incident_num, incident_date, incident_time]))

    def run(self, incident_details, conn, cursor):
        selected = self.select_attributes(incident_details)
        incident = models.Incident(**selected)
        if incident:
            incident.exists = True
            return incident         
        else:
            incident.exists = False
            return incident

class LocationBuilder:
    attributes = ['latitude','longitude','borough','precinct','setting']

    def select_attributes(self, incident_details):
        latitude = incident_details[0]['latitude']
        longitude = incident_details[0]['longitude']
        borough = incident_details[0]['boro_nm']
        precinct = incident_details[0]['addr_pct_cd']
        setting = incident_details[0]['prem_typ_desc']
        return dict(zip(self.attributes,[latitude,longitude,borough,precinct,setting]))

    def run(self, incident_details, conn, cursor):
        location_attributes = self.select_attributes(incident_details)
        location = models.Location(**location_attributes)
        location = db.save(location, conn, cursor)
        return location

class ComplaintBuilder:
    attributes= ['desc_offense', 'level_offense', 'dept_juris'] 
   
    def select_attributes(self, incident_details):
        desc_offense, level_offense, dept_juris = incident_details[0]['ofns_desc'],incident_details[0]['law_cat_cd'],incident_details[0]['juris_desc']
        return dict(zip(self.attributes,[desc_offense, level_offense, dept_juris]))

    def run(self, incident_details, conn, cursor):
        complaint_attributes = self.select_attributes(incident_details)
        complaint = models.Complaint(**complaint_attributes)
        complaint = db.save(complaint, conn, cursor)
        return complaint

   
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