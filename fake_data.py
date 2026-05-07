import json

articles_fictifs = [
    {
        "title": "CRISPR-Cas9 gene editing in human cells",
        "authors": ["Doe J", "Smith A"],
        "abstract": "This study explores gene editing using CRISPR technology...",
        "doi": "10.1016/j.cell.2023.01.001",
        "journal": "Cell",
        "year": 2023,
        "publication_date": "2023-03-15",
        "domain": "genetics",
        "source": "pubmed",
        "citation_count": 142,
        "collected_at": "2026-05-01"
    },
    {
        "title": "Memory consolidation during sleep",
        "authors": ["Martin L", "Dupont R"],
        "abstract": "Sleep plays a crucial role in memory consolidation...",
        "doi": "10.1038/neuro.2022.05",
        "journal": "Nature Neuroscience",
        "year": 2022,
        "publication_date": "2022-07-10",
        "domain": "neuroscience",
        "source": "semantic_scholar",
        "citation_count": 87,
        "collected_at": "2026-05-01"
    },
    {
        "title": "Tumor immunotherapy advances",
        "authors": ["Chen W"],
        "abstract": "Recent advances in immunotherapy have transformed cancer treatment...",
        "doi": "10.1016/onco.2023.03.002",
        "journal": "Oncology Letters",
        "year": 2021,
        "publication_date": "2021-05-20",
        "domain": "oncology",
        "source": "pubmed",
        "citation_count": 210,
        "collected_at": "2026-05-01"
    }
]

with open('articles_fake.json', 'w', encoding='utf-8') as f:
    json.dump(articles_fictifs, f, ensure_ascii=False, indent=2)

print("✅ Fichier articles_fake.json créé")