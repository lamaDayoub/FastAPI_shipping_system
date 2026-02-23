from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from .database import Database

app = FastAPI()

db=Database()

###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int):
    # Check for shipment with given id
    shipment= db.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment


### Create a new shipment with content and weight
@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate) -> dict[str, int]:
    # Create and assign shipment a new id
    new_id = db.create(shipment)
    return {"id": new_id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, body: ShipmentUpdate):
    shipment= db.update(id, body)
    return shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int) -> dict[str, str]:
    db.delete(id)
    return {"detail": f"Shipment with id #{id} is deleted!"}


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )














































# from typing import Callable,Any
# from fastapi import HTTPException
# routes :dict[str,Callable[[Any],Any]]={}

# def rout(path:str):
#     def register_rout(func):
#         routes[path]=func
#         return func
#     return register_rout

# @rout('\shipment')
# def get_shipment():
#     return 'shipment is arrived'

# request:str=""
# while request!='quit':
#     request =input('>  ')
    
#     if request in routes:
#         response=routes[request]()
#         print(response,end='\n\n')
#     else:
#         print('not found')
        

    