import sqlite3


def select_info(query):
    conn = sqlite3.connect('vacancy.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.close()
    return result


def insert_info(table_name, data):
    columns = ', '.join(data.keys())
    placeholders = ':' + ', :'.join(data.keys())
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
    conn = sqlite3.connect('vacancy.db')
    c = conn.cursor()
#    print(query, data)
    c.execute(query, data)
    conn.commit()
    conn.close()
