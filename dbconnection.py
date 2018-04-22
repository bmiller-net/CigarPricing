import pyodbc

def open_connection(host, db):
    connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+host+";DATABASE="+db)
    return connection
    
def execute_query(connection, statement):
    cursor = connection.cursor()
    cursor.execute(statement)
    results = []
    row = cursor.fetchone()
    while row:
        results.append(row)
        row = cursor.fetchone()
    return results