from __future__ import annotations

import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

load_dotenv()

app = FastAPI(title="Moviebox Affiliate App", version="0.1.0")


def affiliate_url() -> str:
    raw = os.getenv("MOVIEBOX_AFFILIATE_URL", "https://moviebox.ph/")
    parts = urlsplit(raw)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.setdefault("utm_source", "moviebox-premium-app")
    query.setdefault("utm_medium", "affiliate")
    query.setdefault("utm_campaign", "premium")
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/go/moviebox", include_in_schema=False)
def go_to_moviebox() -> RedirectResponse:
    # Redirection transparente : le paiement reste sur le site officiel.
    return RedirectResponse(affiliate_url(), status_code=307)


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    name = os.getenv("APP_NAME", "Moviebox Premium App")
    return f"""<!doctype html>
<html lang=\"fr\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>{name}</title><style>body{{font-family:system-ui;max-width:720px;margin:12vh auto;padding:24px;background:#10131a;color:#fff}}a{{display:inline-block;padding:14px 20px;background:#ff3864;color:#fff;border-radius:10px;text-decoration:none;font-weight:700}}small{{color:#b6bdca}}</style></head>
<body><h1>Accéder à MovieBox Premium</h1>
<p>Découvre le service et souscris directement auprès de MovieBox.</p>
<p><a href=\"/go/moviebox\">Visiter MovieBox</a></p>
<p><small>Ce site est un partenaire indépendant. Les paiements, comptes, abonnements et contenus sont gérés par MovieBox. Nous ne stockons ni ne redistribuons de vidéos.</small></p>
</body></html>"""
