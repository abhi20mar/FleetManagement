from pymongo import MongoClient
from datetime import datetime
import random
import ssl

uri = "mongodb+srv://admin:admin@cluster0.dd5kr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

db = client['fleet_management']
collection = db['obd_data']

def generate_dummy_obd_data():
    obd_data = {
        "vehicle_id": random.randint(1, 10),
        "speed": random.randint(0, 120),
        "fuel_level": round(random.uniform(0, 100), 2),
        "engine_temp": random.randint(70, 120)
    }
    return obd_data

def insert_dummy_data():
    for _ in range(10):
        obd_data = generate_dummy_obd_data()
        collection.insert_one(obd_data)
        print(f"Inserted OBD Data: {obd_data}")

insert_dummy_data()

client.close()
