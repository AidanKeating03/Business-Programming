import mysql.connector


def create_conn():
    conn = mysql.connector.connect(
        host="128.198.162.191",
        # host = "localhost",
        # or "localhost" if working in XAMPP
        user="infs3070",
        # user = os.environ.get('3070user'), 
        password="pydev",
        # password = os.environ.get('3070pass'),
        database="infs3070"
    )
    return conn