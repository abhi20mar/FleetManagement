
from pymongo.mongo_client import MongoClient
import ssl

uri = "mongodb+srv://admin:admin@cluster0.dd5kr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

