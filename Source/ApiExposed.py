from fastapi import FastAPI
from pymongo import MongoClient
from typing import List
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import ssl

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed (e.g., ['http://localhost'])
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


uri = "mongodb+srv://admin:admin@cluster0.dd5kr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

db = client['fleet_management']
collection = db['obd_data']

class OBDData(BaseModel):
    vehicle_id: int
    speed: int
    fuel_level: float
    engine_temp: int

@app.get("/obd_data/", response_model=List[OBDData])
async def get_obd_data():
    obd_data = collection.find({})
    data = []
    for entry in obd_data:
        entry["_id"] = str(entry["_id"])
        data.append(entry)
    return data

@app.post("/obd_data/")
async def insert_obd_data(obd_data: OBDData):
    obd_data_dict = obd_data.dict()
    collection.insert_one(obd_data_dict)
    return {"message": "OBD data inserted successfully", "data": obd_data_dict}

@app.on_event("shutdown")
def shutdown_db():
    client.close()
