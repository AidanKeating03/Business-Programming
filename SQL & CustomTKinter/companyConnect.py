import mysql.connector as mariadb

def create_conn():
    conn = mariadb.connect(
        host="128.198.162.191",
        user="infscompany",
        password="yeadata",
        database="company"
    )
    return conn