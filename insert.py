from pymongo import MongoClient
from dotenv import load_dotenv
import os, json

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))

db = client['biomedical_corpus']
collection = db['articles']

# Charger JSON
with open('articles_clean1.json', encoding='utf-8') as f:
    data = json.load(f)


print(f"✅ {len(data)} articles insérés")