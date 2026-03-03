
from fastapi import  FastAPI
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from app.database.session import create_db_tables
from app.api.router import master_router

@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    await create_db_tables()
    yield
    
    

app = FastAPI(lifespan=lifespan_handler)

app.include_router(master_router)
# db=Database()


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
        

    