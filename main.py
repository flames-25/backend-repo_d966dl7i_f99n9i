import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Fragrance, Review, BlogPost, ContactMessage

app = FastAPI(title="Biodegradable Deodorants API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Biodegradable Deodorants API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Seed default 5 fragrances if collection empty
@app.post("/seed")
def seed_data():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    col = db["fragrance"]
    if col.count_documents({}) > 0:
        return {"status": "exists", "count": col.count_documents({})}
    seed = [
        {
            "slug": "rosa-delicata",
            "name": "Rosa Delicata",
            "tagline": "Petali vellutati, eleganza quotidiana",
            "color": "#E9A6B6",
            "description": "Una carezza floreale ispirata ai giardini di rose all'alba.",
            "notes_top": ["bergamotto", "peonia"],
            "notes_heart": ["rosa damascena", "geranio"],
            "notes_base": ["muschi bianchi", "legno di cedro"],
            "ingredients": ["alcol bio", "acqua", "estratto di rosa", "glicerina vegetale"],
            "hero_image": None,
            "pack_image": None,
            "is_active": True,
        },
        {
            "slug": "mandarino-fresco",
            "name": "Mandarino Fresco",
            "tagline": "Solarità agrumata che mette di buon umore",
            "color": "#F7B267",
            "description": "Spensierato e luminoso, come una mattina d'estate.",
            "notes_top": ["mandarino", "lime"],
            "notes_heart": ["fiori d'arancio", "neroli"],
            "notes_base": ["legni chiari", "ambra leggera"],
            "ingredients": ["alcol bio", "acqua", "olio essenziale di mandarino", "triethyl citrate"],
            "hero_image": None,
            "pack_image": None,
            "is_active": True,
        },
        {
            "slug": "zenzero-puro",
            "name": "Zenzero Puro",
            "tagline": "Energia speziata, pulizia cristallina",
            "color": "#E0C879",
            "description": "Vivace e dinamico, con una scia pulita e moderna.",
            "notes_top": ["zenzero fresco", "limone"],
            "notes_heart": ["tè verde", "cardamomo"],
            "notes_base": ["vetiver", "cedro"],
            "ingredients": ["alcol bio", "acqua", "estratto di zenzero", "triethyl citrate"],
            "hero_image": None,
            "pack_image": None,
            "is_active": True,
        },
        {
            "slug": "bosco-morbido",
            "name": "Bosco Morbido",
            "tagline": "Verde avvolgente, calma e profondità",
            "color": "#9BC1A3",
            "description": "Racconta passeggiate tra muschi e felci dopo la pioggia.",
            "notes_top": ["menta", "foglie di fico"],
            "notes_heart": ["muschio di quercia", "salvia"],
            "notes_base": ["patchouli leggero", "legno di sandalo"],
            "ingredients": ["alcol bio", "acqua", "assoluta di muschio di quercia", "glicerina vegetale"],
            "hero_image": None,
            "pack_image": None,
            "is_active": True,
        },
        {
            "slug": "vaniglia-setosa",
            "name": "Vaniglia Setosa",
            "tagline": "Dolcezza pulita, comfort avvolgente",
            "color": "#EED8C9",
            "description": "Coccola i sensi con note cremoso-vanigliate e luminose.",
            "notes_top": ["vaniglia tahitiana", "latte di mandorla"],
            "notes_heart": ["orchidea", "eliotropio"],
            "notes_base": ["fava tonka", "muschio"],
            "ingredients": ["alcol bio", "acqua", "estratto di vaniglia", "triethyl citrate"],
            "hero_image": None,
            "pack_image": None,
            "is_active": True,
        },
    ]
    db["fragrance"].insert_many(seed)
    return {"status": "seeded", "count": len(seed)}

# Fragrances endpoints
@app.get("/fragrances", response_model=List[Fragrance])
def list_fragrances():
    docs = get_documents("fragrance", {"is_active": True})
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/fragrances/{slug}", response_model=Fragrance)
def get_fragrance(slug: str):
    doc = db["fragrance"].find_one({"slug": slug})
    if not doc:
        raise HTTPException(status_code=404, detail="Fragrance not found")
    doc.pop("_id", None)
    return doc

@app.get("/fragrances/{slug}/reviews", response_model=List[Review])
def get_reviews(slug: str):
    docs = get_documents("review", {"fragrance_slug": slug})
    for d in docs:
        d.pop("_id", None)
    return docs

@app.post("/fragrances/{slug}/reviews")
def add_review(slug: str, review: Review):
    # Ensure fragrance exists
    if not db["fragrance"].find_one({"slug": slug}):
        raise HTTPException(status_code=404, detail="Fragrance not found")
    create_document("review", review)
    return {"status": "ok"}

# Blog endpoints
@app.get("/blog", response_model=List[BlogPost])
def list_posts():
    docs = get_documents("blogpost", {"is_published": True})
    for d in docs:
        d.pop("_id", None)
    return docs

@app.get("/blog/{slug}", response_model=BlogPost)
def get_post(slug: str):
    doc = db["blogpost"].find_one({"slug": slug, "is_published": True})
    if not doc:
        raise HTTPException(status_code=404, detail="Post not found")
    doc.pop("_id", None)
    return doc

# Contact endpoint
@app.post("/contact")
def contact(message: ContactMessage):
    create_document("contactmessage", message)
    return {"status": "received"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
