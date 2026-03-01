from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status

from app.database.models import ShipmentStatus
from app.database.session import SessionDep
from app.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate
from app.services.shipment import ShipmentService

router = APIRouter()


###  a shipment by id
@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, session:SessionDep):
    # Check for shipment with given id
    shipment= ShipmentService(session).get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment



@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate,session:SessionDep) -> Shipment:
    return await ShipmentService(session).add(shipment)
    


### Update fields of a shipment
@router.patch("/shipment", response_model=Shipment)
async def update_shipment(id: int, updated_shipment: ShipmentUpdate,session:SessionDep):
    shipment = await ShipmentService(session).get(id)
    
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = 'the shipment with the provided id id not exsist'
        )
    updating = updated_shipment.model_dump(exclude_none = True)
    if not updating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No Data provided to update'
        )
    updated_ship= await ShipmentService(session).update(id,updating)
    return updated_ship


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int,session:SessionDep) -> dict[str, str]:
    shipment=await ShipmentService(session).get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'the shipment with the provided id is not exist'
        )
    await ShipmentService(session).delete(id)
    
    return {"detail": f"Shipment with id #{id} is deleted!"}
