"""
Fonctions de démonstration pour tester les différentes configurations de la grille déformée.
"""

import sys
import os
# Add parent directory to path so we can import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from distorsion_movement.deformed_grid import DeformedGrid


def create_deformed_grid(dimension: int = 64, 
                        cell_size: int = 8,
                        distortion_strength: float = 0.0,
                        distortion_fn: str = "random",
                        color_scheme: str = "rainbow",
                        color_animation: bool = False,
                        fullscreen: bool = False,
                        shape_type: str = "square",
                        mixed_shapes: bool = False) -> DeformedGrid:
    """
    Crée une grille déformée avec des paramètres simples.
    
    Args:
        dimension: Nombre de cellules par ligne/colonne
        cell_size: Taille moyenne d'un carré en pixels  
        distortion_strength: Intensité de la déformation (0.0 à 1.0)
        distortion_fn: Type de distorsion ("random", "sine", "perlin", "circular")
        color_scheme: Schéma de couleurs ("monochrome", "gradient", "rainbow", etc.)
        color_animation: Si True, les couleurs sont animées
        fullscreen: Si True, démarre directement en plein écran
        shape_type: Type de forme à utiliser ("square", "circle", "triangle", etc.)
        mixed_shapes: Si True, utilise différentes formes dans la grille
    
    Returns:
        Instance de DeformedGrid configurée
    """
    if fullscreen:
        # Pour le plein écran, utiliser une taille de fenêtre temporaire
        canvas_size = (900, 900)
    else:
        grow_factor = 1.3
        canvas_size = (dimension * cell_size * grow_factor, dimension * cell_size * grow_factor)
    
    grid = DeformedGrid(
        dimension=dimension,
        cell_size=cell_size,
        canvas_size=canvas_size,
        distortion_strength=distortion_strength,
        distortion_fn=distortion_fn,
        color_scheme=color_scheme,
        color_animation=color_animation,
        shape_type=shape_type,
        mixed_shapes=mixed_shapes
    )
    
    # Si plein écran demandé, l'activer immédiatement
    if fullscreen:
        grid.toggle_fullscreen()
    
    return grid


def quick_demo():
    """Démonstration rapide avec paramètres par défaut"""
    grid = create_deformed_grid(dimension=64, cell_size=16, distortion_strength=0.3, 
                               color_scheme="rainbow", color_animation=True)
    grid.run_interactive()


def fullscreen_demo():
    """Démonstration en plein écran avec formes mixtes - PARFAIT POUR TESTER LES NOUVELLES FORMES! 🔷🔶⭐"""
    grid = create_deformed_grid(
        dimension=32, 
        cell_size=20, 
        distortion_strength=1, 
        distortion_fn="hypno_spiral_pulse",
        color_scheme="candy_shop", 
        color_animation=True,
        fullscreen=False,
        shape_type="square",  # Commencer avec des carrés
        mixed_shapes=False     # Formes mixtes activées
    )
    print("\n🔷 NOUVELLES FORMES DISPONIBLES!")
    print("🎮 Utilisez 'H' pour changer de forme:")
    print("   - Carrés, Cercles, Triangles, Hexagones, Pentagones, Étoiles, Losanges")
    print("🎲 'Shift+H' bascule entre forme unique et formes mixtes")
    print("🎨 Les nouvelles formes réagissent aux couleurs et distorsions!")
    grid.run_interactive()

if __name__ == "__main__":
    # Choisir la démo à lancer
    print("🎨 Démonstrations disponibles:")
    print("1. quick_demo() - Démonstration rapide")
    print("2. fullscreen_demo() - Cercles en plein écran")
    fullscreen_demo()