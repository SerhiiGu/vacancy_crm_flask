import sqlite3

dbname = input("Введіть назву бази для створення(без .db): ")
dbname = dbname + ".db"

con = sqlite3.connect(dbname)
cur = con.cursor()
cur.execute('''CREATE TABLE "vacancy" (
    "id" INTEGER NOT NULL UNIQUE,
    "creation_date"	TEXT NOT NULL DEFAULT CURRENT_DATE,
    "status" INTEGER NOT NULL DEFAULT 0,
    "company" TEXT NOT NULL,
    "contact_ids" TEXT,
    "description" TEXT NOT NULL,
    "position_name"	TEXT NOT NULL,
    "comment" TEXT,
    "user_id" INTEGER,
    PRIMARY KEY("id" AUTOINCREMENT)
); ''')
cur.execute('''CREATE TABLE "event" (
    "id" INTEGER NOT NULL UNIQUE,
    "vacancy_id" INTEGER NOT NULL,
    "description" TEXT NOT NULL,
    "event_date" TEXT NOT NULL DEFAULT CURRENT_DATE,
    "title"	TEXT NOT NULL,
    "due_to_date" TEXT NOT NULL,
    "status" INTEGER DEFAULT 0,
    PRIMARY KEY("id" AUTOINCREMENT)
); ''')
con.commit()
cur.close()
con.close()
