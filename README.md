ProcessGuardian

(simple, clair : protège ton système en fermant uniquement ce que tu veux et en blacklistant tout le reste)

README.md
# ProcessGuardian

ProcessGuardian est un outil Python pour Windows permettant de fermer proprement les applications utilisateur tout en protégeant les processus critiques du système.  
Il inclut une **blacklist intégrée**, une gestion des **PID système** et une interface simple pour confirmer ou ajouter des applications à la blacklist.

## Fonctionnalités

- Vérifie et demande automatiquement les droits administrateur.
- Affiche les applications détectées avec leur PID.
- Propose trois options pour chaque application :
  - `o` : fermer l'application
  - `n` : ignorer
  - `b` : ajouter à la blacklist pour ne plus jamais proposer de la fermer
- Regroupe automatiquement les processus multiples d’une même application.
- Les PID système (<1000) sont **marqués en rouge et non fermables**.
- Stocke la blacklist dans un fichier JSON local (compatible PyInstaller).

## Installation

1. Installer les dépendances :  

```bash
pip install psutil colorama


Lancer le script avec Python 3.8+ sur Windows :

python process_guardian.py


(Optionnel) Compiler avec PyInstaller pour créer un exécutable autonome :

pyinstaller --onefile process_guardian.py

Utilisation

Au lancement, le script demande les droits administrateur si nécessaire.

Il scanne tous les processus et affiche les applications détectées.

Pour chaque application, choisissez :

o pour fermer

n pour ignorer

b pour ajouter à la blacklist

Le script ferme proprement les applications sélectionnées et gère les processus en arrière-plan restants.

Sécurité

Ne jamais fermer : antivirus, services Windows critiques, pilotes graphiques, processus système (PID < 1000).

Les applications ajoutées à la blacklist ne seront jamais proposées pour fermeture ultérieure.

Contribuer

Contributions bienvenues ! Merci de vérifier que toute modification ne met pas en danger les processus critiques du système.
