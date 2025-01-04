import mysql.connector

sql_user = input("enter mysql username: ")
sql_pass = input("enter mysql password: ")

conn = mysql.connector.connect(
    host='localhost',
    user=sql_user,
    password=sql_pass
)
cursor = conn.cursor()

cursor.execute('''
    DROP DATABASE IF EXISTS reddit_tech;
    CREATE DATABASE reddit_tech;
''')
               
conn = mysql.connector.connect(
    host='localhost',
    user=sql_user,
    password=sql_pass,
    database='reddit_tech'
)

cursor = conn.cursor()

cursor.execute('''
    use reddit_tech;
'''
)
            
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    username VARCHAR(512),
    url VARCHAR(512), 
    upvotes INT,
    comments INT,
    timestamp VARCHAR(255),
    subreddit VARCHAR(255),
    keywords VARCHAR(512)
    )
''')

conn.commit()
conn.close()

