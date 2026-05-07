from fastapi import APIRouter
from db import articles_collection

router = APIRouter(prefix="/stats", tags=["Statistiques"])


@router.get("/by-year")
def stats_by_year():
    """
    Nombre d'articles groupés par année.
    Retourne : [{"_id": 2023, "count": 142}, ...]
    Utilisé par le graphique en barres du dashboard.
    """
    pipeline = [
        {"$match": {"year": {"$gt": 0}}},
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    return list(articles_collection.aggregate(pipeline))


@router.get("/by-domain")
def stats_by_domain():
    """
    Nombre d'articles groupés par domaine.
    Retourne : [{"_id": "oncology", "count": 312}, ...]
    Utilisé par le graphique camembert du dashboard.
    """
    pipeline = [
        {"$group": {"_id": "$domain", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    return list(articles_collection.aggregate(pipeline))


@router.get("/by-source")
def stats_by_source():
    """Nombre d'articles groupés par source (pubmed, semantic_scholar...)."""
    pipeline = [
        {"$group": {"_id": "$source", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]
    return list(articles_collection.aggregate(pipeline))


@router.get("/by-journal")
def stats_by_journal(top: int = 10):
    """Top N journaux les plus représentés dans le corpus."""
    pipeline = [
        {"$match": {"journal": {"$exists": True, "$ne": ""}}},
        {"$group": {"_id": "$journal", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": top},
    ]
    return list(articles_collection.aggregate(pipeline))


@router.get("/summary")
def summary():
    """
    Résumé global du corpus.
    Retourne toutes les métriques clés en un seul appel.
    Utilisé pour les cartes de métriques en haut du dashboard.
    """
    total = articles_collection.count_documents({})
    domains = len(articles_collection.distinct("domain"))
    sources = len(articles_collection.distinct("source"))
    journals = len(articles_collection.distinct("journal"))

    # Année min et max
    year_range_pipeline = [
        {"$match": {"year": {"$gt": 0}}},
        {"$group": {
            "_id": None,
            "min_year": {"$min": "$year"},
            "max_year": {"$max": "$year"},
        }}
    ]
    year_result = list(articles_collection.aggregate(year_range_pipeline))
    min_year = year_result[0]["min_year"] if year_result else None
    max_year = year_result[0]["max_year"] if year_result else None

    return {
        "total_articles": total,
        "total_domains": domains,
        "total_sources": sources,
        "total_journals": journals,
        "year_range": {"min": min_year, "max": max_year},
    }
