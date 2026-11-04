DEVINE MON SECRET ! VERSION WEB AVEC IA
=====================================

OBJECTIF : publier le jeu une seule fois. Ensuite, ouvrir une simple URL pour jouer.

ÉTAPE 1 — Compte GitHub (gratuit) : https://github.com/
  • Crée un nouveau dépôt (repository) nommé devine-mon-secret.
  • Décompresse le ZIP du jeu.
  • Dans ton dépôt, clique Add file > Upload files.
  • Ajoute index.html, vercel.json et le DOSSIER api (avec ask.py et status.py).
  • Clique Commit changes.
  • Ne publie JAMAIS ta clé API dans GitHub.

ÉTAPE 2 — Compte Vercel : https://vercel.com/new
  • Inscris-toi (connexion GitHub possible).
  • Clique Import sur le dépôt devine-mon-secret.
  • Choisis Other (aucun framework nécessaire) et garde le dossier racine.
  • Dans « Environment Variables », ajoute :
      OPENAI_API_KEY = ta clé API OpenAI
      GAME_ACCESS_CODE = un code personnel de ton choix (long, difficile à deviner)
  • Ces variables doivent être enregistrées pour Production.
  • Clique Deploy. La page de succès te donnera une URL du genre :
      https://devine-mon-secret-xxxxx.vercel.app

ÉTAPE 3 — JOUER
  • Ouvre ton URL. Le site doit dire « IA connectée ».
  • Pose une question. Au premier message, saisis ton GAME_ACCESS_CODE.
  • Le code est gardé seulement pour l'onglet/la session en cours.
  • Partage ton écran sur Zoom, sans donner le code aux élèves.
  • Plus besoin de Terminal à chaque utilisation !

SI LE MODE IA EST GRISÉ :
  • Vérifie les variables dans Vercel > Project > Settings > Environment Variables.
  • Redéploie après une modification (Deployments > Redeploy).
  • Assure-toi que la facturation API OpenAI est active.

ATTENTION : ChatGPT Plus n'inclut pas les crédits API.
  • Les appels à l'API sont facturés séparément.
  • Ne partage ni la clé API ni ton code d'accès.
  • Un code n'est pas un système complet de quotas ni une authentification pour un site public très fréquenté.
  • Pour un usage important, ajoute limitation de débit, protection Vercel et plafond budgétaire côté OpenAI.
  • Les réponses de l'IA peuvent parfois être inexactes.

Le mode classique reste disponible si l'IA n'est pas connectée.
