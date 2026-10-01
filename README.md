# Moviebox Premium App — option affiliée

Application de découverte et de redirection affiliée. Elle ne fournit pas de films, de liens de streaming, de téléchargements ni de paiement MovieBox dans sa propre infrastructure.

## Fonctionnalités

- Landing page responsive en français
- Redirection vers le lien affilié officiel (`/go/moviebox`)
- Paramètres UTM ajoutés automatiquement
- Catalogue informatif TMDb optionnel (`/api/catalog/search`)
- Documentation FastAPI (`/docs`)
- Endpoint de santé (`/health`)

## Lancer en local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload
```

Ouvre http://127.0.0.1:8000.

## Configuration

```env
MOVIEBOX_AFFILIATE_URL=https://moviebox.ph/?ref=TON_IDENTIFIANT
TMDB_API_KEY=ta_cle_tmdb_optionnelle
APP_NAME=Moviebox Premium App
```

Utilise uniquement un lien fourni par le programme d’affiliation officiel. Le paiement Stripe n’est pas intégré à cette option : MovieBox encaisse directement les abonnements. Stripe ne peut être ajouté pour vendre l’accès à MovieBox qu’avec une autorisation contractuelle explicite de MovieBox et les droits de distribution nécessaires.

## Déploiement

Sur Render, Railway ou Fly.io : configure le dossier de démarrage `backend`, la commande `uvicorn app:app --host 0.0.0.0 --port $PORT`, puis ajoute les variables d’environnement dans le tableau de bord. Ne committe jamais `.env` ou une clé TMDb.

## Conformité

Obtiens une autorisation écrite avant d’utiliser la marque, le catalogue ou les visuels MovieBox. Ajoute une politique de confidentialité, une divulgation d’affiliation et respecte les lois applicables dans les pays ciblés.
