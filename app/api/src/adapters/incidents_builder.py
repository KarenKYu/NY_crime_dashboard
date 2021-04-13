import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters
import psycopg2

#incident_details == list of dictionaries
class Builder:
    def run(self, incident_details, conn, cursor): #takes in json details for one incident
        incident = IncidentBuilder().run(incident_details, conn, cursor)
        # print(incident.__dict__)
        if incident:
            location = LocationBuilder().run(incident_details, conn, cursor)
            complaint = ComplaintBuilder().run(incident_details, conn, cursor)
            incident.location_id = location.id
            incident.complaint_id = complaint.id
            incident = db.save(incident, conn, cursor)
            return {'incident': incident, 'location': location, 'complaint': complaint}

class IncidentBuilder:
    attributes = ['incident_num', 'incident_date','incident_time']
#gets info you want to hold onto from json file for incident class
    def select_attributes(self, incident_details): 
        for incident in incident_details:
            incident_num = incident['cmplnt_num']
            incident_date = incident['cmplnt_fr_dt']
            incident_time = incident['cmplnt_fr_tm'] 
            return dict(zip(self.attributes, [incident_num, incident_date, incident_time]))

#takes info and assigns to Incident obj instance as attributes
    def run(self, incident_details, conn, cursor):
        selected = self.select_attributes(incident_details)
        incident = models.Incident(**selected)
        return incident
        # if incident:
        #     incident.exists = True
        #     return incident         
        # else:
        #     incident.exists = False
        #     # incident = db.save(incident, conn, cursor)
        #     return incident

class LocationBuilder:
    attributes = ['borough','latitude','longitude','setting','precinct']

    def select_attributes(self, incident_details):
        borough = incident_details[0].get('boro_nm','None')
        latitude = incident_details[0].get('latitude','None')
        longitude = incident_details[0].get('longitude','None')
        setting = incident_details[0].get('prem_typ_desc','None')
        precinct = incident_details[0].get('addr_pct_cd','None')
        return dict(zip(self.attributes,[borough,latitude,longitude,setting,precinct]))

    def run(self, incident_details, conn, cursor):
        location_attributes = self.select_attributes(incident_details)
        location = models.Location(**location_attributes)
        location = db.save(location, conn, cursor)
        return location

class ComplaintBuilder:
    attributes= ['desc_offense', 'level_offense', 'dept_juris'] 
   
    def select_attributes(self, incident_details):
        desc_offense = incident_details[0].get('ofns_desc', 'None')
        level_offense = incident_details[0].get('law_cat_cd', 'None')
        dept_juris = incident_details[0].get('juris_desc', 'None')
        return dict(zip(self.attributes,[desc_offense, level_offense, dept_juris]))

    def run(self, incident_details, conn, cursor):
        complaint_attributes = self.select_attributes(incident_details)
        complaint = models.Complaint(**complaint_attributes)
        complaint = db.save(complaint, conn, cursor)
        return complaint
