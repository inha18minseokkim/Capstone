from typing import Union

from fastapi import FastAPI, Request, HTTPException
from fastapi import Header
import nest_asyncio
import Start
import StrategyLoop

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    nest_asyncio.apply()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/getRatio",status_code = 200)
async def getRatio(request: Request):
    #필요한 정보 : stklist, strategy
    try:
        stklist = request.headers['stklist']
        print(stklist)
    except:
        raise HTTPException(status_code=422,detail="stklist Argument form not correct")
    try:
        strategy = int(request.headers['strategy'])
        print(strategy)
    except:
        raise HTTPException(status_code=422,detail="strategy Argument form not correct")
    try:
        period = int(request.headers['period'])
        print(period)
    except:
        raise HTTPException(status_code=422,detail="period Argument form not correct")
    #여기서 구현
    starter = Start.Starter(stklist,strategy,period)
    se = StrategyLoop.StrategyExecutor()
    executor = se.bindStrategy(starter)
    res = executor.process()
    return res

