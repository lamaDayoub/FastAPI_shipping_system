from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich import print,panel

@asynccontextmanager
async def lifespan_handler(app:FastAPI):
    print(panel.Panel('server started ...',border_style ='green'))
    yield
    print(panel.Panel('... stopped',border_style ='green'))
    

app = FastAPI(lifespan=lifespan_handler)

app.get('/')
def root():
    return {'message':'Hello World!'}