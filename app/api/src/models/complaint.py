from api.src.db import db
import api.src.models as models

class Complaint:
    __table__='complaints'
    columns = ['id','desc_offense', 'level_offense', 'dept_juris']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.columns:
                raise ValueError(f'{key} not in columns: {self.columns}')
        for k, v in kwargs.items():
            setattr(self, k, v)

# select all columns from complaints table where == 'desc_offense' 
    @classmethod
    def find_by_type(self, complaint, cursor):
        query_str = "SELECT * FROM complaints WHERE desc_offense = %s"
        cursor.execute(query_str, (complaint,))
        records = cursor.fetchall()
        return db.build_from_records(models.Complaint, records)
# >>> complaint2 =Complaint.find_by_complaint_type('ASSAULT 3 & RELATED OFFENSES',cursor)  
# >>> complaint2 w/o build from records and return records == tuple
# [(2, 'ASSAULT 3 & RELATED OFFENSES', 'MISDEMEANOR', 'N.Y. POLICE DEPT')]

# >>> complaint = Complaint.find_by_type('ROBBERY', cursor)
# >>> complaint[0].__dict__
# {'id': 3, 'desc_offense': 'ROBBERY', 'level_offense': 'FELONY', 'dept_juris': 'N.Y. POLICE DEPT'}
# >>> complaint[1].__dict__

    @classmethod
    def find_by_dept_jurisdiction(self, dept_juris, cursor):
        query_str = "SELECT * FROM complaints WHERE dept_juris = %s"
        cursor.execute(query_str, (dept_juris,))
        records = cursor.fetchall()
        return db.build_from_records(models.Complaint, records)

# >>> complaint = Complaint.find_by_dept_jurisdiction('N.Y. POLICE DEPT',cursor)
# >>> len(complaint)
# 5
# >>> complaint[0].__dict__
# {'id': 1, 'desc_offense': 'THEFT-FRAUD', 'level_offense': 'FELONY', 'dept_juris': 'N.Y. POLICE DEPT'}
# >>> complaint[1].__dict__
# {'id': 2, 'desc_offense': 'ASSAULT 3 & RELATED OFFENSES', 'level_offense': 'MISDEMEANOR', 'dept_juris': 'N.Y. POLICE DEPT'}
