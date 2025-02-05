from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin123@cluster0.dd5kr.mongodb.net/fleet_management?retryWrites=true&w=majority")

db = client['fleet_management']
collection = db['obd_data']

def clear_data():
    collection.delete_many({})
    print("All OBD data cleared.")

clear_data()

client.close()
