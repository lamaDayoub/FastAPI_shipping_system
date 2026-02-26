from datetime import datetime, timedelta

from fastapi import  FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference


from app.database.models import Shipment, ShipmentStatus
from .schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

from contextlib import asynccontextmanager
from app.database.session import create_db_tables, SessionDep

@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    create_db_tables()
    yield
    
    

app = FastAPI(lifespan=lifespan_handler)

# db=Database()

###  a shipment by id
@app.get("/shipment", response_model=ShipmentRead)
def get_shipment(id: int, session:SessionDep):
    # Check for shipment with given id
    shipment= session.get(Shipment, id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment



@app.post("/shipment", response_model=None)
def submit_shipment(shipment: ShipmentCreate,session:SessionDep) -> dict[str, int]:
    
    new_shipment = Shipment(
        **shipment.model_dump(),
        status = ShipmentStatus.placed,
        estimated_delivery = datetime.now()+ timedelta(days = 3) 
    )
    session.add (new_shipment)
    session.commit()
    session.refresh(new_shipment)
   
    return {"id": new_shipment.id}


### Update fields of a shipment
@app.patch("/shipment", response_model=ShipmentRead)
def update_shipment(id: int, updated_shipment: ShipmentUpdate,session:SessionDep):
    shipment = session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = 'the shipment with the provided id id not exsist'
        )
    update = updated_shipment.model_dump(exclude_none = True)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No Data provided to update'
        )
    shipment.sqlmodel_update(update)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
    return shipment


### Delete a shipment by id
@app.delete("/shipment")
def delete_shipment(id: int,session:SessionDep) -> dict[str, str]:
    shipment=session.get(Shipment,id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'the shipment with the provided id is not exist'
        )
    session.delete(
        session.get(Shipment,id)
    )
    session.commit()
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
        

    