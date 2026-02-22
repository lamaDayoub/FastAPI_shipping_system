import sqlite3

#Make the Connection
connection = sqlite3.connect('sqlit.db')


#curdor to excute the sql lanaguage commands
cursor = connection.cursor()
#1creating a table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS shipment(
        id INT PRIMARY KEY,
        content TEXT,
        weight REAL,
        status TEXT
    )
    """
)
# adding a row
# cursor.execute("""
#     INSERT INTO shipment VALUES(
#         12701,'desktop',10,'placed'
#     )
# """)
# connection.commit()
#updating
cursor.execute("""
        UPDATE shipment SET status = 'delivered'
        WHERE id = 12701
               """)
connection.commit()
#  selecting from the table

# cursor.execute("""
#     SELECT * FROM shipment                            
# """)
# result = cursor.fetchmany(2)
# print(result)

# cursor.execute("""
#     SELECT * FROM shipment  WHERE id=12701                          
# """)
# result2 = cursor.fetchone()
# print(result2)
# delete the table
# cursor.execute("DROP TABLE shipment")
# connection.commit()
connection.close()