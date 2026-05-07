from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.articles import router as articles_router
from routes.stats import router as stats_router

# ─── Initialisation de l'application ──────────────────────────
app = FastAPI(
    title="Biomedical Corpus API",
    description="API REST pour explorer le corpus d'articles biomédicaux (PubMed, Semantic Scholar).",
    version="1.0.0",
)

# ─── CORS : autorise Streamlit (localhost:8501) à appeler l'API ─
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ─── Enregistrement des routes ─────────────────────────────────
app.include_router(articles_router)
app.include_router(stats_router)


# ─── Route racine ──────────────────────────────────────────────
@app.get("/", tags=["Santé"])
def root():
    return {
        "message": "Biomedical Corpus API opérationnelle ✅",
        "docs": "/docs",
        "endpoints": [
            "GET /articles/",
            "GET /articles/count",
            "GET /articles/search?q=...",
            "GET /articles/domains",
            "GET /articles/sources",
            "GET /stats/summary",
            "GET /stats/by-year",
            "GET /stats/by-domain",
            "GET /stats/by-source",
            "GET /stats/by-journal",
        ]
    }


# ─── Lancement direct ──────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
