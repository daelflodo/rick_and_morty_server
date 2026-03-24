from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

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


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def landing() -> str:
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rick &amp; Morty API</title>
  <style>
    *{margin:0;padding:0;box-sizing:border-box}
    body{font-family:'Segoe UI','Roboto',sans-serif;background:#0a0f1e;color:#f0f0f0;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px}
    .portal{width:90px;height:90px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#c8f06e,#97ce4c 45%,#3a7d0a 100%);box-shadow:0 0 30px rgba(151,206,76,.8),0 0 70px rgba(151,206,76,.3);animation:pulse 3s ease-in-out infinite;margin-bottom:28px}
    @keyframes pulse{0%,100%{box-shadow:0 0 30px rgba(151,206,76,.8),0 0 70px rgba(151,206,76,.3)}50%{box-shadow:0 0 50px rgba(151,206,76,1),0 0 110px rgba(151,206,76,.5)}}
    h1{font-size:2.4rem;font-weight:900;letter-spacing:1px;margin-bottom:6px}
    .version{display:inline-block;background:rgba(151,206,76,.15);border:1px solid rgba(151,206,76,.4);color:#97ce4c;font-size:.75rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;padding:4px 14px;border-radius:20px;margin-bottom:16px}
    .desc{color:rgba(240,240,240,.6);font-size:1rem;max-width:520px;text-align:center;line-height:1.7;margin-bottom:40px}
    .endpoints{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;max-width:760px;width:100%;margin-bottom:40px}
    .ep{background:rgba(255,255,255,.04);border:1px solid rgba(151,206,76,.18);border-radius:12px;padding:16px 20px;display:flex;flex-direction:column;gap:6px}
    .ep-method{font-size:.65rem;font-weight:800;letter-spacing:2px;text-transform:uppercase;padding:2px 10px;border-radius:20px;display:inline-block;width:fit-content}
    .get{background:rgba(46,204,113,.15);color:#2ecc71}
    .post{background:rgba(52,152,219,.15);color:#3498db}
    .ep-path{font-size:.9rem;font-weight:600;color:#f0f0f0;font-family:'Courier New',monospace}
    .ep-desc{font-size:.78rem;color:rgba(240,240,240,.45)}
    .actions{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}
    .btn-primary{padding:14px 36px;border-radius:12px;border:none;background:linear-gradient(135deg,#97ce4c,#3a7d0a);color:#0a0f1e;font-size:1rem;font-weight:800;cursor:pointer;text-decoration:none;transition:opacity .2s,transform .15s}
    .btn-primary:hover{opacity:.88;transform:translateY(-2px)}
    .btn-outline{padding:14px 36px;border-radius:12px;border:2px solid rgba(151,206,76,.5);background:transparent;color:#97ce4c;font-size:1rem;font-weight:700;cursor:pointer;text-decoration:none;transition:background .2s,transform .15s}
    .btn-outline:hover{background:rgba(151,206,76,.08);transform:translateY(-2px)}
    footer{margin-top:56px;font-size:.75rem;color:rgba(240,240,240,.25);text-align:center}
  </style>
</head>
<body>
  <div class="portal"></div>
  <h1>Rick &amp; Morty API</h1>
  <span class="version">v1.0.0</span>
  <p class="desc">REST API para explorar el multiverso de Rick &amp; Morty. Autenticación JWT, favoritos, personajes personalizados e integración con la API oficial.</p>

  <div class="endpoints">
    <div class="ep">
      <span class="ep-method post">POST</span>
      <span class="ep-path">/api/auth/register</span>
      <span class="ep-desc">Registrar nuevo usuario</span>
    </div>
    <div class="ep">
      <span class="ep-method post">POST</span>
      <span class="ep-path">/api/auth/login</span>
      <span class="ep-desc">Iniciar sesión · devuelve JWT</span>
    </div>
    <div class="ep">
      <span class="ep-method get">GET</span>
      <span class="ep-path">/api/characters/random</span>
      <span class="ep-desc">10 personajes aleatorios</span>
    </div>
    <div class="ep">
      <span class="ep-method get">GET</span>
      <span class="ep-path">/api/characters/search</span>
      <span class="ep-desc">Buscar con filtros</span>
    </div>
    <div class="ep">
      <span class="ep-method get">GET</span>
      <span class="ep-path">/api/favorites</span>
      <span class="ep-desc">Ver favoritos del usuario</span>
    </div>
    <div class="ep">
      <span class="ep-method post">POST</span>
      <span class="ep-path">/api/favorites</span>
      <span class="ep-desc">Agregar a favoritos</span>
    </div>
    <div class="ep">
      <span class="ep-method get">GET</span>
      <span class="ep-path">/api/custom-characters</span>
      <span class="ep-desc">Listar personajes propios</span>
    </div>
    <div class="ep">
      <span class="ep-method post">POST</span>
      <span class="ep-path">/api/custom-characters</span>
      <span class="ep-desc">Crear personaje propio</span>
    </div>
  </div>

  <div class="actions">
    <a class="btn-primary" href="/docs">Ver Documentación →</a>

  </div>

  <footer>FastAPI · SQLAlchemy · PostgreSQL · Docker · Render &nbsp;|&nbsp; Rick &amp; Morty Universe API</footer>
</body>
</html>"""
