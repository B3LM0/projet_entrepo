from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ MONGO_URI non défini dans le fichier .env")
    sys.exit(1)

client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,  # à retirer en production
    serverSelectionTimeoutMS=5000
)

db = client["biomedical_corpus"]
articles_collection = db["articles"]
