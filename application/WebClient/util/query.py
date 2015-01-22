import sqlite3

def execute(query):
    """Function to execute queries against a local sqlite database"""
    dbPath = 'database.db'
    connection = sqlite3.connect(dbPath)
    cursorobj = connection.cursor()
    try:
        cursorobj.execute(query)
            result = cursorobj.fetchall()
            connection.commit()
    except Exception:
        raise
connection.close()
    return result