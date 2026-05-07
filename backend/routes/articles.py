from fastapi import APIRouter, Query, HTTPException
from typing import List
from db import articles_collection

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.get("/")
def get_articles(
    domain: str = Query(None, description="Filtrer par domaine (genetics, oncology...)"),
    source: str = Query(None, description="Filtrer par source (pubmed, semantic_scholar)"),
    year: int = Query(None, description="Filtrer par année exacte"),
    limit: int = Query(20, ge=1, le=200, description="Nombre max de résultats (1-200)"),
    skip: int = Query(0, ge=0, description="Pagination : ignorer N premiers résultats"),
):
    """
    Récupère une liste d'articles avec filtres optionnels.
    Utilisé par le dashboard pour afficher le tableau d'articles.
    """
    query = {}
    if domain:
        query["domain"] = domain
    if source:
        query["source"] = source
    if year:
        query["year"] = year

    results = list(
        articles_collection.find(query, {"_id": 0})
        .skip(skip)
        .limit(limit)
    )
    return results


@router.get("/count")
def count_articles(
    domain: str = Query(None),
    source: str = Query(None),
    year: int = Query(None),
):
    """Retourne le nombre d'articles correspondant aux filtres."""
    query = {}
    if domain:
        query["domain"] = domain
    if source:
        query["source"] = source
    if year:
        query["year"] = year

    total = articles_collection.count_documents(query)
    return {"count": total}


@router.get("/search")
def search_articles(
    q: str = Query(..., min_length=2, description="Mot-clé à rechercher"),
    limit: int = Query(10, ge=1, le=50),
):
    """
    Recherche plein-texte dans le titre et l'abstract.
    Requiert l'index texte créé par create_indexes.py.
    """
    try:
        results = list(
            articles_collection.find(
                {"$text": {"$search": q}},
                {"_id": 0, "score": {"$meta": "textScore"}}
            )
            .sort([("score", {"$meta": "textScore"})])
            .limit(limit)
        )
        return results
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de recherche. L'index texte est-il créé ? ({e})"
        )


@router.get("/domains")
def list_domains():
    """Retourne la liste des domaines distincts présents en base."""
    domains = articles_collection.distinct("domain")
    return sorted([d for d in domains if d])


@router.get("/sources")
def list_sources():
    """Retourne la liste des sources distinctes présentes en base."""
    sources = articles_collection.distinct("source")
    return sorted([s for s in sources if s])


@router.post("/import")
def import_articles(articles: List[dict]):
    """
    Importe une liste d'articles dans MongoDB.
    - Accepte un tableau JSON d'articles
    - Ignore les doublons (même DOI)
    - Retourne le nombre d'articles insérés et ignorés
    """
    if not articles:
        raise HTTPException(status_code=400, detail="Liste d'articles vide.")

    inserted = 0
    skipped = 0

    for article in articles:
        # Retirer _id si présent pour éviter les conflits MongoDB
        article.pop("_id", None)

        doi = article.get("doi", "").strip()

        # Vérifier doublon par DOI si disponible
        if doi and articles_collection.find_one({"doi": doi}):
            skipped += 1
            continue

        articles_collection.insert_one(article)
        inserted += 1

    return {
        "inserted": inserted,
        "skipped": skipped,
        "total": len(articles)
    }