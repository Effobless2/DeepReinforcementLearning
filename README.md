# DeepReinforcementLearning

## Lancement
- `python main.py [fichierDeSauvegarde]`
- Si vous spécifiez un fichier de sauvegarde, ce dernier va recharger la table d'apprentissage contenue dans ce dernier, sinon il initialisera une nouvelle table d'apprentissage

## Commandes
- S permet de sauvegarder l'état de la table d'apprentissage à un instant donné. Elle sera alors sauvegardée dans le fichier 'sokobanTable.json'

### Réflexions
Cas de victoire :
    - Toutes les caisses doivent être sur une case de destination différente

Cas de défaite : 
    - Si la caisse est dans un angle et pas sur une case de destination
    - Si le joueur ne peut pas bouger et que les caisses ne sont pas sur une case de destination

Cas particulier :
    - Deux caisses ne peuvent pas être bougées en même temps si elles sont l'une contre l'autre
    - Une caisse ne peut pas être mise sur les cases mur, joueur, autre caisse
    - Le joueur ne peut pas être sur la même case qu'une caisse

Autre :
    - Le joueur ne peut se déplacer que d'une case à la fois et sur les axes horizontal et vertical
