import api.src.models as models
import api.src.db as db
import api.src.adapters as adapters
import psycopg2

class Builder:
    def run(self, incident_details, conn, cursor):
        incident = IncidentBuilder().run(incident_details, conn, cursor)
        if incident.exists:
            return {'incident': incident, 'location': incident.location(cursor), 
                    'complaint_type': incident.complaint_type(cursor)}
        else:
            location = LocationBuilder().run(incident_details, incident, conn, cursor)
            complaint_type = ComplaintBuilder().run(incident_details, incident, conn, cursor)
            return {'incident': incident, 'location': location, 'complaint_type': incident.complaint_type}

class IncidentBuilder:
    attributes = ['incident_num', 'complaint_id', 'incident_date','incident_time', 'location_id']

    def select_attributes(self, incident_details):
        complaint_id =
        location_id=
        incident_num,incident_date,incident_time = incident_details['cmplnt_num'], incident_details['cmplnt_fr_dt'], incident_details['cmplnt_fr_tm']
        return dict(zip(self.attributes, [incident_num,incident_date,incident_time]))

    def run(self, incident_details, conn, cursor):
        selected = self.select_attributes(incident_details)
        incident_num = selected['cmplnt_num']
        incident = models.Incident.find_by_incident_num(incident_num, cursor)
        if incident:
            incident.exists = True
            return incident
        else:
            incident = db.save(models.Incident(**selected), conn, cursor)
            incident.exists = False
            return incident

class LocationBuilder:]
    attributes = ['latitude','longitude','borough','precinct','setting']

    def select_attributes(self, incident_details):
        latitude = incident_details['latitude']
        longitude = incident_details['longitude']
        borough = incident_details['boro_nm']
        precinct = incident_details['addr_pct_cd']
        setting = incident_details['prem_typ_desc']
        return dict(zip(self.attributes,[latitude,longitude,borough,precinct,setting]))

    def run(self, incident_details, incident, conn, cursor):
        location_attributes = self.select_attributes(incident_details)
        location = self.build_location_city_state_zip(location_attributes, conn, cursor)
        location = db.save(location, conn, cursor)
        return location

    def find_or_create_by_city_state_zip(self, city_name = 'N/A', state_name = 'N/A', code = None, conn = None, cursor = None):
        if not city_name or not state_name: raise KeyError('must provide conn or cursor')
        state = db.find_or_create_by_name(models.State, state_name, conn, cursor)
        city = db.find_by_name(models.City, city_name, cursor)
        zipcode = models.Zipcode.find_by_code(code, cursor)
        if not city:
            city = models.City(name = city_name, state_id = state.id)
            city = db.save(city, conn, cursor)
        if not zipcode:
            zipcode = models.Zipcode(code = code, city_id = city.id)
            zipcode = db.save(zipcode, conn, cursor)
        return city, state, zipcode

    def build_location_city_state_zip(self, location_attr, conn, cursor):
        city_name = location_attr.pop('city', 'N/A')
        state_name = location_attr.pop('state', 'N/A')
        code = location_attr.pop('postalCode', None)
        city, state, zipcode = self.find_or_create_by_city_state_zip(city_name, state_name, code, conn, cursor)
        location = models.Location(latitude = location_attr.get('lat', None),
                longitude = location_attr.get('lng', None),
                address = location_attr.get('address', ''),
                zipcode_id = zipcode.id
                )
        return location

class ComplaintBuilder:
    attributes= ['desc_offense', 'level_offense', 'dept_juris'] 
   
    def select_attributes(self, incident_details):
        desc_offense, level_offense, dept_juris = incident_details['ofns_desc'],[incident_details['law_cat_cd'],[incident_details['juris_desc']
        return dict(zip(self.attributes,[desc_offense, level_offense, dept_juris] ))

    def find_or_create_complaints(self, complaint_name, conn, cursor):
        if not isinstance(complaint_name, list): raise TypeError('complaint description must be list')
        complaints = []
        for name in complaint_name:
            complaint = db.find_or_create_by_name(models.Complaint, 
                name, conn, cursor)
            complaints.append(complaint_name)
        return complaints

    def create_incident_complaints(self, incident, complaints, conn, cursor):
        categories = [models.VenueCategory(venue_id = venue.id, category_id = category.id)
                for category in categories]
        return [db.save(category, conn, cursor) for category in categories]

    def run(self, venue_details, venue, conn, cursor):
        category_names = self.select_attributes(venue_details)
        categories = self.find_or_create_categories(category_names, conn, cursor)
        venue_categories = self.create_venue_categories(venue, categories, conn, cursor)
        return venue_categories