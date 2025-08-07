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

## Grille de carrés déformés géométriquement

Le fichier `deformed_grid.py` implémente une nouvelle fonctionnalité d'art génératif : des grilles de carrés déformés géométriquement.

### Utilisation rapide

```python
from deformed_grid import create_deformed_grid

# Créer une grille déformée
grid = create_deformed_grid(
    dimension=48,           # Grille 48x48
    cell_size=12,          # Carrés de 12 pixels
    distortion_strength=0.4, # Intensité de déformation
    distortion_fn="sine"    # Type de distorsion
)

# Lancer l'interface interactive
grid.run_interactive()
```

### Types de distorsion disponibles

- **`"random"`** : Déformation aléatoire statique
- **`"sine"`** : Distorsion sinusoïdale animée (effet de vague)
- **`"perlin"`** : Bruit de Perlin pour un effet organique
- **`"circular"`** : Ondes circulaires depuis le centre

### Contrôles interactifs

- **ESC** : Quitter
- **SPACE** : Changer le type de distorsion
- **+/-** : Ajuster l'intensité de distorsion
- **R** : Régénérer les paramètres aléatoires
- **S** : Sauvegarder l'image courante

### Démonstrations

Lancez le script de démonstration pour explorer différents exemples :

```bash
python demo_deformed_grid.py
```

Le script propose 8 démonstrations différentes :
1. Démonstration basique (distorsion aléatoire)
2. Animation sinusoïdale
3. Effet organique (Perlin)
4. Ondes circulaires
5. Haute densité (grille fine)
6. Couleurs personnalisées
7. Tremblement minimal (effet subtil)
8. Export en lot (génération d'images)

### Paramètres avancés

```python
from deformed_grid import DeformedGrid

grid = DeformedGrid(
    dimension=64,                           # Nombre de cellules par ligne/colonne
    cell_size=8,                           # Taille moyenne des carrés
    canvas_size=(800, 600),                # Taille de la fenêtre
    distortion_strength=0.3,               # Intensité (0.0 à 1.0)
    distortion_fn="random",                # Type de distorsion
    background_color=(20, 20, 30),         # Couleur de fond RGB
    square_color=(255, 255, 255)           # Couleur des carrés RGB
)
```

## Idées d'extensions

- Patterns géométriques
- Gradients de couleur
- Formes autres que des carrés
- Animation temporelle
- Interaction utilisateur


## Other ideas:

🎲 1. Grille avec règles de propagation (style “contagion”)
	•	Concept : Un carré coloré “contamine” ses voisins avec une certaine couleur ou un effet au fil du temps.
	•	Résultat : Une sorte d’onde ou de tache de couleur qui se propage dans la grille.
	•	Originalité : Tu définis tes propres règles de propagation (aléatoire, influence de la couleur voisine, etc.)

⸻

🧠 2. Influence d’un bruit de Perlin ou Simplex
	•	Concept : Tu utilises du bruit (comme une texture mathématique douce) pour moduler la couleur, la taille, la rotation des carrés.
	•	Résultat : Des effets très organiques, qui rappellent des structures naturelles.
	•	Originalité : Tu mélanges hasard contrôlé + structure.

⸻

🎨 3. Palette limitée avec contrainte esthétique
	•	Concept : Tu choisis une palette (genre 4 couleurs de Kandinsky, ou le style Bauhaus) et tu forces les carrés à suivre un pattern (pas plus de 2 couleurs côte à côte, pas 3 fois la même de suite, etc.)
	•	Résultat : Ça donne des rythmes visuels intéressants.
	•	Originalité : Le code impose des contraintes artistiques.

⸻

🧩 4. Grille à déformation géométrique
	•	Concept : Au lieu d’un carré fixe, chaque cellule est légèrement déformée (distorsion de position, taille, perspective).
	•	Résultat : Un effet d’illusion ou d’espace qui tremble.
	•	Originalité : L’ordre apparent de la grille est bousculé.

⸻

🌱 5. Évolution générationnelle
	•	Concept : Tu fais tourner la grille dans le temps : à chaque tick, la grille change (un peu comme une vie cellulaire type “Game of Life”).
	•	Résultat : Une œuvre animée, auto-évolutive.
	•	Originalité : Tu n’affiches pas qu’un état, mais un processus.

⸻

🧵 6. Tissage de motifs / glitch
	•	Concept : Chaque carré devient une “maille” dans un tissage visuel. Tu peux “glitcher” aléatoirement des sections (inversion de couleurs, rotations, miroir).
	•	Résultat : Un mix entre géométrie stricte et chaos visuel.
	•	Originalité : Belle tension entre contrôle et rupture.

⸻

👁️ 7. Œil qui regarde
	•	Concept : Un carré sur la grille suit la souris (ou une zone chaude), les couleurs autour réagissent à sa position.
	•	Résultat : Une grille “vivante”, qui semble te regarder ou réagir à toi.
	•	Originalité : Une œuvre interactive minimaliste.