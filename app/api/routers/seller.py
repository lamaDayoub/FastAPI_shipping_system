from fastapi import APIRouter
from app.api.dependencies import SellerServiceDep
from app.api.schemas.seller import SellerRead, SellerCreate



router = APIRouter(prefix='/seller', tags=['Seller'])


@router.post('signup', response_model=SellerRead)
async def register_seller(seller: SellerCreate, service: SellerServiceDep):
    
    return await service.add(seller)