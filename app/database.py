import sqlite3

#Make the Connection
connection = sqlite3.connect('sqlit.db')


#curdor to excute the sql lanaguage commands
cursor = connection.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shipment(
        id INT,
        content TEXT,
        weight REAL,
        status TEXT
    )
    """
)
cursor.execute("""
    INSERT INTO shipment VALUES(
        12702,'desktop',10,'placed'
    )
""")
connection.commit()
#Close the connection when done
connection.close()