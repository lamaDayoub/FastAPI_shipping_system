import sqlite3

#Make the Connection
connection = sqlite3.connect('sqlit.db')


#curdor to excute the sql lanaguage commands
cursor = connection.cursor()
#1 creating a table
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
#2 adding a row
# cursor.execute("""
#     INSERT INTO shipment VALUES(
#         12702,'desktop',10,'placed'
#     )
# """)
# connection.commit()

#3 selecting from the table

cursor.execute("""
    SELECT * FROM shipment                            
""")
result = cursor.fetchmany(2)
print(result)

cursor.execute("""
    SELECT * FROM shipment  WHERE id=12701                          
""")
result2 = cursor.fetchone()
print(result2)
#Close the connection when done
connection.close()