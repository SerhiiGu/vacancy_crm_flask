import os
import pymongo


class MongoLib:
    def __init__(self, dbname, colname):
        self.dbname = dbname
        self.colname = colname
        mongo_host = os.environ.get('MONGO_HOST', 'localhost')
        self.client = pymongo.MongoClient(f'mongodb://root:qwe123@{mongo_host}:27017')
        self.mydb = self.client[self.dbname]
        self.mycol = self.mydb[self.colname]

    def check_create_db(self):
        dblist = self.client.list_database_names()
        if self.dbname not in dblist:
            self.mycol.insert_one({"name": "One", "email": "TWO"}).inserted_id
            self.mycol.delete_one({"name": "One", "email": "TWO"})

    def m_find_one(self, find_dict):
        data = self.mycol.find_one(find_dict)
        return data

    def m_insert_one(self, ins_dict):
        contact_id = self.mycol.insert_one(ins_dict).inserted_id
        return contact_id
