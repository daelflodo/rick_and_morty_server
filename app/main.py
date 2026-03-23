from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from app.database import Base, engine
from app.routers import auth, characters, favorites
from app.routers.custom_characters import router as custom_characters_router

with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS rick_and_morty"))
    conn.commit()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rick and Morty API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://rick-and-morty-client-iota.vercel.app",
        "https://rick-and-morty-client-55y4ml432-daelflodos-projects.vercel.app",
    ],
    allow_origin_regex=r"https://rick-and-morty-client.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(characters.router)
app.include_router(favorites.router)
app.include_router(custom_characters_router)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "ok"}
