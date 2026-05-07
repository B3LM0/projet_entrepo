from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
collection = client['biomedical_corpus']['articles']

# 1. Récupérer les articles par domaine
def get_articles_by_domain(domain, limit=20):
    return list(collection.find({'domain': domain}, {'_id': 0}).limit(limit))

# 2. Compter les articles par année
def count_by_year():
    pipeline = [
        {'$group': {'_id': '$year', 'count': {'$sum': 1}}},
        {'$sort': {'_id': 1}}
    ]
    return list(collection.aggregate(pipeline))

# 3. Compter les articles par domaine
def count_by_domain():
    pipeline = [
        {'$group': {'_id': '$domain', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ]
    return list(collection.aggregate(pipeline))

# 4. Recherche par mot-clé
def search_text(query):
    return list(collection.find(
        {'$text': {'$search': query}},
        {'_id': 0}
    ).limit(10))

# 5. Total articles
def count_total():
    return collection.count_documents({})

# 6. Articles par source
def count_by_source():
    pipeline = [
        {'$group': {'_id': '$source', 'count': {'$sum': 1}}}
    ]
    return list(collection.aggregate(pipeline))


# ─── TEST ──────────────────────────────────────────────────────
if __name__ == '__main__':
    print("📊 Total articles      :", count_total())
    print("📅 Par année           :", count_by_year())
    print("🧬 Par domaine         :", count_by_domain())
    print("🔍 Recherche 'cancer'  :", len(search_text('cancer')), "résultats")
    print("📡 Par source          :", count_by_source())
    print("\n✅ Toutes les fonctions marchent — prêt pour Membre 3 !")