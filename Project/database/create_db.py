import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)

cur = conn.cursor()

try:
    cur.execute("create database ims")

    conn.commit()
    
except:
    conn.rollback()

conn.close()