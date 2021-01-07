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
            venue_categories = CategoryBuilder().run(incident_details, incident, conn, cursor)
            return {'incident': incident, 'location': location, 'complaint_type': incident.complaint_type} #**** check on this

class IncidentBuilder:
    attributes = ['cmplnt_num', 'cmplnt_fr_dt','cmplnt_fr_tm']

    def select_attributes(self, incident_details):
        incident_date = incident_details.get('incident_date', '')
        if incident_date:
            incident_num,incident_date,incident_time = incident_details['cmplnt_num'], incident_details['cmplnt_fr_dt'], incident_details['cmplnt_fr_tm']
            likes = venue_details.get('likes', {}).get('count', None)
        return dict(zip(self.attributes, [incident_num,incident_date,incident_time]))

    def run(self, incident_details, conn, cursor):
        selected = self.select_attributes(incident_details)
        incident_num, = selected['cmplnt_num']
        incident = models.Incident.find_by_incident_num(incident_num, cursor)
        if incident:
            incident.exists = True
            return incident
        else:
            incident = db.save(models.Incident(**selected), conn, cursor)
            incident.exists = False
            return incident

class LocationBuilder:
    attributes = ['id','latitude','longitude','boro_nm','addr_pct_cd','prem_typ_desc']
    
    def select_attributes(self, incident_details):
        lat = incident_details['latitude']
        lon = incident_details['longitude']
        boro = incident_details['borough']
        prec = incident_details['precinct']
        setting = incident_details['setting']
        reduced_dict = {k:v for k,v in location.items() if k in self.attributes}
        return reduced_dict

    def run(self, venue_details, venue, conn, cursor):
        location_attributes = self.select_attributes(incident_details)
        location = self.build_location_city_state_zip(location_attributes, conn, cursor)
        location.venue_id = venue.id
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

class CategoryBuilder:
    def select_attributes(self, venue_details):
        categories = [category['name'] for category in venue_details['categories']]
        return categories

    def find_or_create_categories(self, category_names, conn, cursor):
        if not isinstance(category_names, list): raise TypeError('category_names must be list')
        categories = []
        for name in category_names:
            category = db.find_or_create_by_name(models.Category, 
                name, conn, cursor)
            categories.append(category)
        return categories

    def create_venue_categories(self, venue, categories, conn, cursor):
        categories = [models.VenueCategory(venue_id = venue.id, category_id = category.id)
                for category in categories]
        return [db.save(category, conn, cursor) for category in categories]

    def run(self, venue_details, venue, conn, cursor):
        category_names = self.select_attributes(venue_details)
        categories = self.find_or_create_categories(category_names, conn, cursor)
        venue_categories = self.create_venue_categories(venue, categories, conn, cursor)
        return venue_categories