
import sqlite3
from .schemas import ShipmentCreate,ShipmentUpdate
from typing import Any
class Database():
    def __init__(self):
        #Make the Connection
        self.conn = sqlite3.connect('sqlit.db',check_same_thread=False)
        #curdor to excute the sql lanaguage commands
        self.cur =self. conn.cursor()
        self.create_table()
                
    def create_table(self):
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS shipment(
                id INT PRIMARY KEY,
                content TEXT,
                weight REAL,
                status TEXT
            )
            """
        )
        
    def create(self, shipment : ShipmentCreate):
        self.cur.execute("SELECT MAX(id) FROM shipment")
        result = self.cur.fetchone()
        last_id = result[0] if result[0] is not None else -1
        new_id = last_id + 1
        
        self.cur.execute("""
            INSERT INTO shipment VALUES(
                :id, :content , :weight , :status
            )
        """,
            {
                "id":new_id,
                **shipment.model_dump(),
                "status":'placed'
            }
        )
        self.conn.commit()
        return new_id
        
    def get(self, id:int) -> dict[str :Any] |None:
        self.cur.execute("""
        SELECT * FROM shipment  WHERE id=?                          
        """,(id,))
        row = self.cur.fetchone()
        return{
            "id":row[0],
            "content":row[1],
            "weight":row[2],
            "status":row[3]
        } if row else None

    def update(self,id: int , shipment:ShipmentUpdate)-> dict[str,Any]:
        
        self.cur.execute("""
            UPDATE shipment SET status = :status
            WHERE id = :id
            """,
                {
                    "id":id,
                    **shipment.model_dump()
                    
                }
            )
        self.conn.commit()
        return self.get(id)
        
    def delete(self , id:int):
        self.cur.execute("DELETE FROM shipment WHERE id = ?",(id,))
        self.conn.commit()
        
    def close(self):
        self.conn.close()





