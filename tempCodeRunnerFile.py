from pymongo import MongoClient
from dotenv import load_dotenv
import os, ssl

load_dotenv()

client = MongoClient(
    os.getenv('MONGO_URI'),
    tls=True,
    tlsAllowInvalidCertificates=True
)

collection = client['biomedical_corpus']['articles']

collection.create_index('domain')
collection.create_index('publication_date')
collection.create_index('year')
collection.create_index('source')
collection.create_index([('title', 'text'), ('abstract', 'text')])

print("✅ Index créés avec succès")

for index in collection.list_indexes():
    print(" -", index['name'])
    