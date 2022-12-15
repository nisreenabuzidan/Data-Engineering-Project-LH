import pandas as pd
from fastapi import FastAPI, HTTPException
from datetime import datetime
import datetime 
from datetime import date
from typing import Optional
from pydantic import BaseModel
from fastapi import Header
from fastapi import Response

from get_latency import get_latency

api = FastAPI (title="Lufthansa Info API",
    description="Lufthansa Info API powered by FastAPI.",
    version="1.0.1",
    )

responses = {
    200: {"description": "OK"},
    400: {"description": "Bad Request"},
    401: {"description": "User Unauthorized"},
    403: {"description": "No enough privileges"},
    404: {"description": "Not found"},
    406: {"description": "Not Acceptable"},
    422: {"description": "Unprocessable Entity"},
    500: {"description": "Internal Server Error"},
}


@api.get("/" , tags=["Get"],responses=responses)
def get_index():
    """ To Ensure That the API works correctly """
    try:
        return {'data': 'hello from general infos of customer flights API'}
    except Exception :
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
            #headers={"X-Error": "There goes my error"},
            )



@api.get("/airport_latency_info",name="Latency in Airport",tags=["Latency"],responses=responses)
def get_latency_in_airport(airport_code:str,start_date:Optional[str]="",end_date:Optional[str]=""):
    
    """ To get all the flights and the delyed flights in the given airport between 2 given days """
    
    if(airport_code == None or airport_code == "" ):
        raise HTTPException(
            status_code=400,
            detail="Airport Code must not be Empty",
            #headers={"X-Error": "There goes my error"},
        )
 
    if(start_date != ""):
        try:
            from_date = datetime.datetime.strptime(start_date,'%Y-%m-%d').date()
        except Exception:
            raise HTTPException(
            status_code=400,
            detail="Error in Start Date format : must be like yyyy-mm-dd",
            #headers={"X-Error": "There goes my error"},
            )
    if(end_date != ""):
        try:
            to_date = datetime.datetime.strptime(end_date,'%Y-%m-%d').date()
        except Exception:
            raise HTTPException(
            status_code=400,
            detail="Error in End Date format : must be like yyyy-mm-dd",
            #headers={"X-Error": "There goes my error"},
            )
    if(start_date > end_date and end_date != ""):
        raise HTTPException(
            status_code=400,
            detail="Start Date must be before End date ",
            #headers={"X-Error": "There goes my error"},
            )
    try:
        df = get_latency(airport_code,start_date,end_date)
        print(df)
        return Response(df.to_json(orient="records"), media_type="application/json")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
            #headers={"X-Error": "There goes my error"},
        )
    
       