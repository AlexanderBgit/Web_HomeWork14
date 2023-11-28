from fastapi import FastAPI, Request, Depends
import time
import redis.asyncio as redis
import uvicorn

import logging

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from fastapi_limiter import FastAPILimiter #connect
from fastapi_limiter.depends import RateLimiter #speed limit
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users
# from src.routes.contacts import contacts

from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app,
    like database connections or external services.
    
    :return: A list of tasks, so we need to wait for them
    :doc-author: Trelent
    """
    r = await redis.Redis(host=os.environ['REDIS_HOST'], 
                          port=os.environ['REDIS_PORT'], 
                          db=0, 
                          encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)




# Cross-Origin Resource Sharing 
@app.middleware("http") 
async def add_process_time_header(request: Request, call_next):
    """
    The add_process_time_header function adds a header to the response called My-Process-Time.
    The value of this header is the time it took for the request to be processed by all middleware and routes.
    
    :param request: Request: Access the request object
    :param call_next: Pass the request to the next function in the pipeline
    :return: A response object
    :doc-author: Trelent
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response

origins = [ 
    "http://localhost:3000",
    "'127.0.0.1:6379"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# for test if error
# app.include_router(auth.router, prefix='/api')
# app.include_router(contacts.router, prefix='/api') 

app.include_router(auth.router, prefix='/api', 
                   dependencies=[Depends(RateLimiter(times=2, seconds=5))])
app.include_router(contacts.router, prefix='/api', 
                   dependencies=[Depends(RateLimiter(times=2, seconds=5))])
app.include_router(users.router, prefix='/api')



# @app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
# async def index():
#     return {"msg": "Hello World"}


@app.get("/")
def read_root():
    return {"message": "That's root"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=8000)  
    # uvicorn app:app --host localhost --port 8000 --reload