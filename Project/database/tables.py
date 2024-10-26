import mysql.connector

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "ims"
)

cur = conn.cursor()

try:

    # Employee

    cur.execute("create table if not exists employee(eid int(20) not null primary key auto_increment, name varchar(255), email varchar(255), gender varchar(255), contact varchar(255), dob varchar(255), doj varchar(255), password varchar(255), utype varchar(255), address varchar(255), salary varchar(255))")
    conn.commit()

    # Supplier

    cur.execute("create table if not exists supplier(invoice int(20) not null primary key auto_increment, name varchar(255), contact varchar(255), descr text(1000))")
    conn.commit()

    # Category

    cur.execute("create table if not exists category(cid int(20) not null primary key auto_increment, name varchar(255))")
    conn.commit()

    # Product

    cur.execute("create table if not exists product(pid int(20) not null primary key auto_increment, category varchar(255), supplier varchar (255), name varchar(255), price varchar(255), qty varchar(255), status varchar(255))")
    conn.commit()

except:
    conn.rollback()

conn.close()