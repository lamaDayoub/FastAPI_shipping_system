from datetime import datetime
from time import perf_counter

from fastapi import FastAPI, Request

from h11 import Response
from scalar_fastapi import get_scalar_api_reference
from contextlib import asynccontextmanager
from app.core.exceptions import add_exception_handlers
from app.database.session import create_db_tables
from app.api.router import master_router
from app.worker.tasks import add_log, background_task


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_db_tables()
    yield


app = FastAPI(lifespan=lifespan_handler)
add_exception_handlers(app)
app.include_router(master_router)


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start = perf_counter()

    response: Response = await call_next(request)

    end = perf_counter()
    time_taken = round(end - start, 2)

    add_log.delay(
        f"{request.method} {request.url} ({response.status_code}) {time_taken} s"
    )

    return response


# db=Database()


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )


@app.get("/test")
def test():
    now = datetime.now()
    background_task.delay(
        f"background_task  {now.second}", data={"min": now.minute, "sec": now.second}
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
