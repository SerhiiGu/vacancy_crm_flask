import sqlite3


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect('vacancy.db')
        self.c = self.conn.cursor()
        return self

    def query(self, query):
        self.c.execute(query)
        result = self.c.fetchall()
        return result

    def insert(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ':' + ', :'.join(data.keys())
        query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
    #    print(query, data)
        self.c.execute(query, data)
        self.conn.commit()

    def update(self, query):
        print(query)
        self.c.execute(query)
        self.conn.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.c.close()
        self.conn.close()
