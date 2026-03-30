from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.api.dependencies import DeleviryPartnerDep, DeliveryPartnerServiceDep, ServiceDep

from app.api.schemas import shipment
from app.api.schemas.shipment import Shipment, ShipmentCreate, ShipmentReview, ShipmentUpdate
from app.api.dependencies import sellerDep
from app.database.models import TagName
from app.utils import TEMPLATE_DIR
from app.config import app_settings
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


@router.get('/tag', response_model=Shipment)
async def add_tag_to_shipment(
    id:UUID,
    tag_name:TagName,
    service: ServiceDep
):
    return await service.add_tag(id, tag_name)
    
@router.delete('/tag', response_model=Shipment)
async def remove_tag_from_shipment(
    id:UUID,
    tag_name:TagName,
    service: ServiceDep
):
    return await service.remove_tag(id, tag_name)
    

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
    
    
@router.get('/review')
async def submit_review(request : Request, token:str):
        
    return templates.TemplateResponse(
        request = request ,
        name= "review.html",
        context ={
            "review_url":f"http://{app_settings.APP_DOMAIN}/shipment/review?token={token}"
        }
        
    )
    
@router.post('/review')
async def submit_review(
    token:str,
    rating:Annotated[int,Form( ge = 1 , le = 5 )],
    service:ServiceDep,
    comment: Annotated[str | None, Form()] = None,
):
    await service.rate(token, rating, comment)
    return{"detail": "review submitted "}