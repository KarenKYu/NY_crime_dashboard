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

# # select all columns from incidents table where complaint_id== a type of complaint aka incidents by type of complaint
#     def incidents(self, cursor):
#         query_str = "SELECT * FROM incidents WHERE complaint_id = %s"
#         cursor.execute(query_str, (self.id,))
#         records = cursor.fetchall()
#         return db.build_from_records(models.Complaint, records)

# select all columns from complaints table where == 'desc_offense' 
    @classmethod
    def find_by_complaint_type(self, complaint, cursor):
        query_str = "SELECT * FROM complaints WHERE desc_offense = %s"
        cursor.execute(query_str, (complaint,))
        records = cursor.fetchall()
        return records

    # select all columns from complaints table where == 'desc_offense' 
    @classmethod
    def find_by_dept_jurisdiction(self, dept_juris, cursor):
        query_str = "SELECT * FROM complaints WHERE dept_juris = %s"
        cursor.execute(query_str, (dept_juris,))
        records = cursor.fetchall()
        return db.build_from_records(models.Complaint, records)


