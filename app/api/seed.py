import psycopg2
from api.src.db import drop_records, save
from api.src.models import Complaint, Incident, Location


conn = psycopg2.connect(database = 'nypd_complaints', user = 'postgres', password = 'postgres')
cursor = conn.cursor()

drop_records(cursor, conn, 'complaints')
drop_records(cursor, conn, 'locations')
drop_records(cursor, conn, 'incidents')

complaint_one = Complaint(id = '1', desc_offense = 'GRAND LARCENY OF MOTOR VEHICLE', level_offense = 'GRAND LARCENY',
        dept_juris = 'N.Y. POLICE DEPT')
complaint_two = Complaint(id = '2', desc_offense = 'MURDER & NON-NEGL. MANSLAUGHTER', level_offense = 'FELONY',
        dept_juris = 'N.Y. HOUSING POLICE')
save(complaint_one, conn, cursor)
save(complaint_two, conn, cursor)

location_one = Location(id = '123', latitude = -73.91575750399994, longitude = -74.00629428799994, borough = 'MANHATTAN',  precinct = 6, setting = 'STREET')
location_two = Location(id = '456', latitude = 40.69866511400005, longitude = -73.91575750399994, borough = '',  precinct = 18, setting = '')
save(location_one, conn, cursor)
save(location_two, conn, cursor)

incident_one = Incident(id = '900', incident_num = 453437883, complaint_id = '1', incident_date = '09/16/2020', incident_time = '21:20:00', location_id='123')
incident_two = Incident(id = '800', incident_num = 774568604, complaint_id = '2', incident_date = '09/02/2020', incident_time = '12:30:00', location_id='456')
save(incident_one, conn, cursor)
save(incident_two, conn, cursor)

