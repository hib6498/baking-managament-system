import mysql.connector as conn

c = conn.connect(
    host = "localhost",
    user = "root",
    password = "c012"
)

query = c.cursor()
query.execute("use bank")

query.execute('''select * from admin where username = "sample"''')
credentials = query.fetchone()

print(credentials)
