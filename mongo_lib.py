import os
import pymongo


mongo_host = os.environ.get('MONGO_HOST', 'localhost')
dbname = 'vacancy_crm'
colname = 'contacts'
client = pymongo.MongoClient(f'mongodb://root:qwe123@{mongo_host}:27017')
mydb = client[dbname]
mycol = mydb[colname]
dblist = client.list_database_names()
if dbname not in dblist:
    mycol.insert_one({"name": "One", "email": "TWO"}).inserted_id
    mycol.delete_one({"name": "One", "email": "TWO"})


class MongoLib:
    def __init__(self, dbname=dbname, colname=colname):
        self.dbname = dbname
        self.colname = colname

    def m_find_one(self, find_dict):
        data = mycol.find_one(find_dict)
        return data

    def m_insert_one(self, ins_dict):
        contact_id = mycol.insert_one(ins_dict).inserted_id
        return contact_id

    def update_one(self, query, updates):
        mycol.update_one(query, updates)

    def delete_one(self, obj):
        mycol.delete_one(obj)
