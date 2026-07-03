def get_connector():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "Varun@2003",
        database = "cleanmydata"
    )
