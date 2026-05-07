import gzip
import json
import xml.etree.ElementTree as ET
from datetime import date

# Domaines détectés automatiquement par mots-clés
DOMAIN_KEYWORDS = {
    "genetics":     ["gene", "genetic", "genome", "dna", "rna", "crispr", "mutation", "sequencing"],
    "neuroscience": ["neuro", "brain", "alzheimer", "parkinson", "neuron", "cognitive", "neural"],
    "immunology":   ["immun", "antibody", "vaccine", "t-cell", "cytokine", "autoimmune"],
    "oncology":     ["cancer", "tumor", "oncol", "carcinoma", "metastasis", "chemotherapy"],
    "cardiology":   ["cardiac", "heart", "cardiovascular", "myocardial", "coronary", "artery"],
}

def detect_domain(title, abstract):
    text = (title + " " + abstract).lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return domain
    return "other"

def parse_pubmed_xml(filepath):
    articles = []

    # Ouvrir .gz ou .xml directement
    if filepath.endswith('.gz'):
        f = gzip.open(filepath, 'rb')
    else:
        f = open(filepath, 'rb')

    tree = ET.parse(f)
    f.close()
    root = tree.getroot()

    for article in root.findall('.//PubmedArticle'):
        try:
            medline = article.find('MedlineCitation')
            art = medline.find('Article')

            # Titre
            title_el = art.find('ArticleTitle')
            title = title_el.text or "" if title_el is not None else ""

            # Abstract
            abstract_el = art.find('Abstract/AbstractText')
            abstract = abstract_el.text or "" if abstract_el is not None else ""

            # Auteurs
            authors = []
            for author in art.findall('AuthorList/Author'):
                last = author.findtext('LastName', '')
                fore = author.findtext('ForeName', '')
                initials = author.findtext('Initials', '')
                if last:
                    authors.append(f"{last} {initials}".strip())

            # Journal
            journal = art.findtext('Journal/Title', '')

            # Date de publication
            pub_date = art.find('Journal/JournalIssue/PubDate')
            year, month, day = "0000", "01", "01"
            if pub_date is not None:
                year  = pub_date.findtext('Year', '0000')
                month = pub_date.findtext('Month', '01').zfill(2)
                day   = pub_date.findtext('Day', '01').zfill(2)
                # Convertir mois littéral (Jan, Feb...) en numéro
                months_map = {
                    'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
                    'May':'05','Jun':'06','Jul':'07','Aug':'08',
                    'Sep':'09','Oct':'10','Nov':'11','Dec':'12'
                }
                month = months_map.get(month, month)

            publication_date = f"{year}-{month}-{day}"

            # DOI
            doi = ""
            for id_el in article.findall('.//ArticleId'):
                if id_el.get('IdType') == 'doi':
                    doi = id_el.text or ""
                    break

            # Domaine auto-détecté
            domain = detect_domain(title, abstract)

            articles.append({
                "title":            title,
                "authors":          authors,
                "abstract":         abstract,
                "doi":              doi,
                "journal":          journal,
                "year":             int(year) if year.isdigit() else 0,
                "publication_date": publication_date,
                "domain":           domain,
                "source":           "pubmed",
                "citation_count":   0,
                "collected_at":     str(date.today())
            })

        except Exception as e:
            print(f"⚠️ Article ignoré : {e}")
            continue

    return articles


# ─── UTILISATION ───────────────────────────────────────────────
# Remplace par le nom de ton fichier téléchargé depuis le FTP
INPUT_FILE  = "pubmed26n0001.xml.gz"   # ou .xml si déjà décompressé
OUTPUT_FILE = "articles_clean1.json"
LIMIT       = 5000                     # nb max d'articles à garder

articles = parse_pubmed_xml(INPUT_FILE)
articles = articles[:LIMIT]

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"✅ {len(articles)} articles exportés dans {OUTPUT_FILE}")