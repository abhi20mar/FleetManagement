from pymongo import MongoClient
import ssl

uri = "mongodb+srv://admin:admin@cluster0.dd5kr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

# Access the database and collection
db = client['fleet_management']
collection = db['obd_data']

def clear_data():
    try:
        count_before = collection.count_documents({})
        collection.delete_many({})
        count_after = collection.count_documents({})

        print(f"Deleted {count_before - count_after} documents.")
        print("All OBD data cleared.")
    except Exception as e:
        print(f"Error clearing data: {e}")

clear_data()

# Close the client connection
client.close()
