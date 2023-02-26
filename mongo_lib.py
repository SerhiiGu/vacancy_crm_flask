import os
import pymongo


mongo_host = os.environ.get('MONGO_HOST', 'localhost')
client = pymongo.MongoClient(f'mongodb://root:qwe123@{mongo_host}:27017')
mydb = client['vacancy_crm']
mycol = mydb['contacts']


class MongoLib:
    def __init__(self, dbname='vacancy_crm', colname='contacts'):
        self.dbname = dbname
        self.colname = colname

    def check_create_db(self):
        dblist = client.list_database_names()
        if self.dbname not in dblist:
            mycol.insert_one({"name": "One", "email": "TWO"}).inserted_id
            mycol.delete_one({"name": "One", "email": "TWO"})

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
