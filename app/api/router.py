from fastapi import APIRouter, HTTPException, status
from app.api.dependencies import ServiceDep

from app.api.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate


router = APIRouter()


###  a shipment by id
@router.get("/shipment", response_model=Shipment)
async def get_shipment(id: int, service : ServiceDep):
    # Check for shipment with given id
    shipment= await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment



@router.post("/shipment")
async def submit_shipment(shipment: ShipmentCreate,service : ServiceDep) -> Shipment:
    return await service.add(shipment)
    


### Update fields of a shipment
@router.patch("/shipment", response_model=Shipment)
async def update_shipment(id: int, updated_shipment: ShipmentUpdate,service : ServiceDep):
    shipment = await service.get(id)
    
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
    updated_ship= await service.update(id,updating)
    return updated_ship


### Delete a shipment by id
@router.delete("/shipment")
async def delete_shipment(id: int,service : ServiceDep) -> dict[str, str]:
    shipment=await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'the shipment with the provided id is not exist'
        )
    await service.delete(id)
    
    return {"detail": f"Shipment with id #{id} is deleted!"}
