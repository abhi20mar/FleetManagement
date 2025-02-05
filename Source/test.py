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
    TIMESTAMP: float
    MARK: str
    CAR_YEAR: float
    MODEL: str
    ENGINE_POWER: str
    AUTOMATIC: str
    VEHICLE_ID: str
    BAROMETRIC_PRESSURE: float
    ENGINE_COOLANT_TEMP: float
    FUEL_LEVEL: str
    ENGINE_LOAD: str
    AMBIENT_AIR_TEMP: float
    ENGINE_RPM: float
    INTAKE_MANIFOLD_PRESSURE: float
    MAF: str
    LONG_TERM_FUEL_TRIM_BANK_2: str
    FUEL_TYPE: str
    AIR_INTAKE_TEMP: float
    FUEL_PRESSURE: float
    SPEED: float
    SHORT_TERM_FUEL_TRIM_BANK_2: str
    SHORT_TERM_FUEL_TRIM_BANK_1: str
    ENGINE_RUNTIME: str
    THROTTLE_POS: str
    DTC_NUMBER: str
    TROUBLE_CODES: str
    TIMING_ADVANCE: str
    EQUIV_RATIO: str
    MIN: float
    HOURS: float
    DAYS_OF_WEEK: float
    MONTHS: float
    YEAR: float

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
