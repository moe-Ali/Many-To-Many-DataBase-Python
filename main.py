import sqlite3
import json

# making connection to the database and using cursor to control it
conn=sqlite3.connect("main.db")
cur=conn.cursor()

# executing SQLite queries
cur.executescript("""
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;

CREATE TABLE User(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Member(
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id,course_id)
);
""")

# opening data file that will be use in database
f=open("data.json")

# reading the json file to get the data
x=json.load(f)

for i in x:
    # saving the data
    user=i[0]
    course=i[1]
    role=int(i[2])

    # executing SQLite queries to save data into User Table
    cur.execute("INSERT OR IGNORE INTO User (name) VALUES (?)",(user,))
    cur.execute("SELECT id FROM User WHERE name = ?",(user,))
    user_id=cur.fetchone()[0]

    # executing SQLite queries to save data into Course Table
    cur.execute("INSERT OR IGNORE INTO Course (name) VALUES (?)",(course,))
    cur.execute("SELECT id FROM Course WHERE name = ?",(course,))
    course_id=cur.fetchone()[0]

    # executing SQLite queries to save data into Member Table
    cur.execute("INSERT OR IGNORE INTO Member (user_id,course_id,role) VALUES (?,?,?)",(user_id,course_id,role))
    
    # commiting the changes to the database
    conn.commit()

# using join to represent the final database
cur.execute("""SELECT User.name,Course.name,Member.role 
                FROM Member JOIN Course JOIN User
                ON user_id=User.id AND course_id=Course.id
                """)
output=cur.fetchall()

# printing the database
for i in output:
    print(i)


