# Art Génératif avec Code

Ce projet explore l'art génératif en créant des visualisations colorées programmatiques.

## Installation

1. Clonez le repository
2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur macOS/Linux
   # ou
   venv\Scripts\activate     # Sur Windows
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Grille de carrés colorés

Le fichier `generative_art.py` contient une fonction pour générer une grille de carrés colorés aléatoirement :

```python
from generative_art import generate_color_grid_vectorized, display_grid

# Générer une grille 64x64
grid = generate_color_grid_vectorized(64)

# Afficher la grille
display_grid(grid, "Ma grille colorée")
```

### Fonctions disponibles

- `generate_color_grid(dimension)` : Version détaillée avec boucles
- `generate_color_grid_vectorized(dimension)` : Version optimisée avec numpy
- `display_grid(grid, title, figsize)` : Affiche la grille dans une fenêtre
- `save_grid(grid, filename, dpi)` : Sauvegarde la grille en image

### Exemple rapide

```bash
python generative_art.py
```

Cette commande génère et affiche une grille 64x64 de carrés colorés aléatoirement.

## Personnalisation

Le code est conçu pour être facilement modifiable :

- Changez la `dimension` pour des grilles plus grandes ou plus petites
- Modifiez la génération de couleurs dans `generate_color_grid()`
- Ajustez les paramètres d'affichage dans `display_grid()`
- Expérimentez avec différents algorithmes de couleur

## Idées d'extensions

- Patterns géométriques
- Gradients de couleur
- Formes autres que des carrés
- Animation temporelle
- Interaction utilisateur