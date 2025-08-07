# Structure Modulaire - Grille Déformée

Le code a été refactorisé en plusieurs modules pour une meilleure organisation et maintenabilité.

## Structure des Modules

```
distorsion_movement/
├── __init__.py              # Point d'entrée du package
├── deformed_grid.py         # Classe principale DeformedGrid (290 lignes)
├── enums.py                 # Énumérations (DistortionType, ColorScheme)
├── audio_analyzer.py        # Analyseur audio temps réel
├── colors.py                # Générateur de couleurs
├── distortions.py           # Moteur de distorsions géométriques
├── demos.py                 # Fonctions de démonstration
├── test_modules.py          # Script de test
└── README_modules.md        # Cette documentation
```

## Avantages de la Structure Modulaire

### 🎯 **Séparation des Responsabilités**
- **`enums.py`**: Définitions des types (24 lignes)
- **`audio_analyzer.py`**: Traitement audio isolé (160 lignes)
- **`colors.py`**: Génération de couleurs pure (140 lignes)
- **`distortions.py`**: Calculs géométriques séparés (180 lignes)
- **`deformed_grid.py`**: Logique principale allégée (290 lignes)

### 📦 **Facilité d'Import**
```python
# Import simple
from distorsion_movement import DeformedGrid, create_deformed_grid

# Import sélectif
from distorsion_movement.colors import ColorGenerator
from distorsion_movement.distortions import DistortionEngine
```

### 🔧 **Maintenance Simplifiée**
- Chaque module a une responsabilité claire
- Tests unitaires possibles par module
- Modifications isolées sans impact sur les autres parties

### 🚀 **Extensibilité**
- Ajouter de nouveaux schémas de couleurs dans `colors.py`
- Créer de nouvelles distorsions dans `distortions.py`
- Améliorer l'audio dans `audio_analyzer.py`

## Utilisation

### Démarrage Rapide
```python
# Méthode 1: Import direct
from distorsion_movement import quick_demo
quick_demo()

# Méthode 2: Module en ligne de commande
python -m distorsion_movement.demos
```

### Utilisation Avancée
```python
from distorsion_movement import DeformedGrid, DistortionType, ColorScheme

# Création personnalisée
grid = DeformedGrid(
    dimension=64,
    cell_size=12,
    distortion_strength=0.7,
    distortion_fn=DistortionType.SINE.value,
    color_scheme=ColorScheme.NEON.value,
    audio_reactive=True
)

grid.run_interactive()
```

## Compatibilité

✅ **Rétro-compatible**: Toutes les fonctionnalités existantes sont préservées  
✅ **API identique**: Les interfaces publiques n'ont pas changé  
✅ **Performance**: Aucune perte de performance, structure plus efficace  

## Tests

Exécuter les tests pour vérifier l'intégrité:
```bash
cd distorsion_movement
python test_modules.py
```

## Migration depuis l'Ancien Code

Si vous utilisiez l'ancien `deformed_grid.py` monolithique:

```python
# Avant (ancien)
from deformed_grid import DeformedGrid, quick_demo

# Après (nouveau)
from distorsion_movement import DeformedGrid, quick_demo
```

Le reste du code reste identique! 🎉