from __future__ import annotations

import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse

load_dotenv()

app = FastAPI(title="Moviebox Affiliate App", version="0.2.0")
TMDB_BASE = "https://api.themoviedb.org/3"


def affiliate_url() -> str:
    raw = os.getenv("MOVIEBOX_AFFILIATE_URL", "https://moviebox.ph/")
    parts = urlsplit(raw)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise RuntimeError("MOVIEBOX_AFFILIATE_URL must be an absolute HTTP(S) URL")
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.setdefault("utm_source", "moviebox-premium-app")
    query.setdefault("utm_medium", "affiliate")
    query.setdefault("utm_campaign", "premium")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def tmdb_key() -> str:
    return os.getenv("TMDB_API_KEY", "").strip()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/config")
def config() -> dict[str, str | bool]:
    return {
        "app_name": os.getenv("APP_NAME", "Moviebox Premium App"),
        "catalog_enabled": bool(tmdb_key()),
        "affiliate_enabled": True,
        "payments": "handled by MovieBox on its official site",
    }


@app.get("/api/catalog/search")
async def catalog_search(q: str = Query(..., min_length=2), page: int = Query(1, ge=1, le=500)):
    key = tmdb_key()
    if not key:
        raise HTTPException(503, "Catalog disabled: configure TMDB_API_KEY")
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            f"{TMDB_BASE}/search/multi",
            params={"api_key": key, "query": q, "language": "fr-FR", "page": page, "include_adult": "false"},
        )
    if response.status_code != 200:
        raise HTTPException(502, "Catalog provider unavailable")
    data = response.json()
    data["results"] = [item for item in data.get("results", []) if item.get("media_type") in {"movie", "tv"}]
    return data


@app.get("/go/moviebox", include_in_schema=False)
def go_to_moviebox() -> RedirectResponse:
    return RedirectResponse(affiliate_url(), status_code=307)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    name = os.getenv("APP_NAME", "Moviebox Premium App")
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name}</title><style>
:root{{--bg:#090b12;--card:#151a27;--muted:#aab2c5;--accent:#ff3864}}*{{box-sizing:border-box}}body{{margin:0;font-family:system-ui;background:radial-gradient(circle at top,#242b45,var(--bg) 55%);color:#fff}}main{{max-width:1080px;margin:auto;padding:64px 22px}}nav{{display:flex;justify-content:space-between;align-items:center;margin-bottom:80px}}.brand{{font-weight:800;font-size:20px}}.pill{{color:#fff;text-decoration:none;border:1px solid #454d63;padding:10px 16px;border-radius:99px}}h1{{font-size:clamp(38px,7vw,76px);line-height:1;margin:0 0 22px;max-width:750px}}p{{color:var(--muted);font-size:18px;line-height:1.6;max-width:650px}}.cta{{display:inline-block;margin-top:22px;background:var(--accent);color:#fff;text-decoration:none;padding:15px 23px;border-radius:10px;font-weight:800}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px;margin-top:76px}}.card{{background:rgba(21,26,39,.85);padding:22px;border:1px solid #293147;border-radius:14px}}.card h3{{margin-top:0}}small{{color:#8993aa;display:block;margin-top:45px;line-height:1.5}}
</style></head><body><main><nav><div class="brand">🎬 {name}</div><a class="pill" href="/docs">API Docs</a></nav><h1>Découvre, puis accède au service officiel.</h1><p>Recherche des films et séries avec notre catalogue informatif, puis visite MovieBox pour créer ton compte et gérer directement ton abonnement.</p><a class="cta" href="/go/moviebox">Visiter MovieBox Premium →</a><section class="grid"><article class="card"><h3>Catalogue</h3><p>Recherche et informations générales grâce à un fournisseur de métadonnées configuré par l’administrateur.</p></article><article class="card"><h3>Paiement sécurisé</h3><p>Le paiement et l’abonnement sont traités directement sur le site officiel MovieBox.</p></article><article class="card"><h3>Transparence</h3><p>Nous sommes un partenaire indépendant. Aucun film n’est hébergé ou redistribué par cette application.</p></article></section><small>Divulgation : ce site peut utiliser un lien affilié. MovieBox est responsable de ses comptes, contenus, paiements et conditions d’utilisation.</small></main></body></html>'''
'''
