import dbconnection
import os
import configparser

def escape_string(input_string):
    return input_string.replace("'", "''")

def insert_prices(prices):
    db_settings = get_database_settings()
    conn = dbconnection.open_connection(db_settings["host"], db_settings["db"])
        
    query = "INSERT INTO [Prices] ([Brand], [Name], [Quantity], [Source], [Price], [IsInStock]) VALUES (?,?,?,?,?,?)"
    cursor = conn.cursor()
    results = cursor.executemany(query, prices)
    cursor.commit()
    cursor.close()
    del cursor
    conn.close()
    return results
    
def get_database_settings():
    settings_file = 'settings.ini'
    root_node = 'DATABASE'
    
    if not os.path.exists(settings_file):
        return
    config = configparser.ConfigParser()
    config.read(settings_file)
    if root_node not in config:
        return
    database_settings = config[root_node]
    return database_settings