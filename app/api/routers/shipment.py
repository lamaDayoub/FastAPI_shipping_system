from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.dependencies import DeleviryPartnerDep, DeliveryPartnerServiceDep, ServiceDep

from app.api.schemas import shipment
from app.api.schemas.shipment import Shipment, ShipmentCreate, ShipmentUpdate
from app.api.dependencies import sellerDep
from app.utils import TEMPLATE_DIR

router = APIRouter(prefix='/shipment', tags=['Shipment'])
templates = Jinja2Templates(TEMPLATE_DIR)

###  a shipment by id add:, _:sellerDep
@router.get("/", response_model=Shipment)
async def get_shipment(id: UUID, _:sellerDep, service : ServiceDep):
    # Check for shipment with given id
    shipment= await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Given id doesn't exist!",
        )

    return shipment

#TRACKING DETAILS OF A SHIPMENT
@router.get("/track")
async def get_tracking(request: Request, id:UUID,  service : ServiceDep ):
    shipment = await service.get(id)
    context = shipment.model_dump()
    context["status"]= shipment.status
    context["partner"]= shipment.delivery_partner.name
    context["timeline"]= shipment.timeline
    context["timeline"].reverse()
    
    return templates.TemplateResponse(
        request = request,
        name = "track.html",
        context=context
        
    )

@router.post("/")
async def submit_shipment(shipment: ShipmentCreate,service : ServiceDep  , seller:sellerDep ) -> Shipment:
    return await service.add(shipment, seller )



### Update fields of a shipment
@router.patch("/", response_model=Shipment)
async def update_shipment(
    id: UUID, 
    updated_shipment: ShipmentUpdate,
    partner:DeleviryPartnerDep,
    service : ServiceDep
):
   
    updating = updated_shipment.model_dump(exclude_none = True)
    if not updating:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No Data provided to update'
        )
    updated_ship= await service.update(id, updated_shipment, partner )
    return updated_ship


### Delete a shipment by id
@router.get("/cancel", response_model =Shipment)
async def cancel_shipment(
    id: UUID,
    seller: sellerDep,
    service : ServiceDep
) -> dict[str, str]:
    shipment=await service.get(id)
    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= 'the shipment with the provided id is not exist'
        )
    return await service.cancel(id, seller)
    
    
