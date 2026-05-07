from pymongo import MongoClient
from dotenv import load_dotenv
import os
import sys

# Charger les variables d'environnement (.env)
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    print("❌ MONGO_URI non défini dans le fichier .env")
    sys.exit(1)

try:
    # Connexion MongoDB (avec options TLS pour éviter erreurs SSL)
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,  # ⚠️ à enlever en production
        serverSelectionTimeoutMS=5000
    )

    # Test de connexion
    client.server_info()
    print("✅ Connexion à MongoDB réussie")

    # Accès à la collection
    db = client["biomedical_corpus"]
    collection = db["articles"]

    # Affichage des index
    print("\n📋 Index existants :")
    indexes = list(collection.list_indexes())

    if not indexes:
        print("⚠️ Aucun index trouvé")
    else:
        for index in indexes:
            print(" -", index["name"])

except Exception as e:
    print("❌ Erreur de connexion MongoDB :")
    print(e)