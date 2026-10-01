# Moviebox Premium App — option affiliée

Application de redirection affiliée vers MovieBox, sans héberger, revendre ou débloquer de films.

## Fonctionnement

- Le catalogue et les fiches peuvent utiliser une source autorisée comme TMDb.
- Le bouton **Accéder à MovieBox** redirige vers le site officiel avec ton lien affilié.
- Les paiements et abonnements sont réalisés directement par MovieBox.
- L'application ne collecte pas de paiement pour MovieBox et ne fournit aucun lien de téléchargement ou de streaming non autorisé.

## Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload
```

Ouvre ensuite http://127.0.0.1:8000.

## Configuration

Dans `.env`, remplace `MOVIEBOX_AFFILIATE_URL` uniquement par une URL fournie par le programme affilié officiel MovieBox. Ne mets jamais une clé secrète dans le dépôt.

```env
MOVIEBOX_AFFILIATE_URL=https://moviebox.ph/
APP_NAME=Moviebox Premium App
```

## Important

Tu dois obtenir l'autorisation écrite de MovieBox avant d'utiliser leur marque, leur catalogue ou de recevoir une commission. Vérifie également les conditions du programme affilié et les obligations de divulgation publicitaire applicables dans ton pays.
