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
                        audio_reactive: bool = False,
                        fullscreen: bool = False) -> DeformedGrid:
    """
    Crée une grille déformée avec des paramètres simples.
    
    Args:
        dimension: Nombre de cellules par ligne/colonne
        cell_size: Taille moyenne d'un carré en pixels  
        distortion_strength: Intensité de la déformation (0.0 à 1.0)
        distortion_fn: Type de distorsion ("random", "sine", "perlin", "circular")
        color_scheme: Schéma de couleurs ("monochrome", "gradient", "rainbow", etc.)
        color_animation: Si True, les couleurs sont animées
        audio_reactive: Si True, réagit à l'audio en temps réel
        fullscreen: Si True, démarre directement en plein écran
    
    Returns:
        Instance de DeformedGrid configurée
    """
    if fullscreen:
        # Pour le plein écran, utiliser une taille de fenêtre temporaire
        canvas_size = (1200, 900)
    else:
        canvas_size = (dimension * cell_size + 100, dimension * cell_size + 100)
    
    grid = DeformedGrid(
        dimension=dimension,
        cell_size=cell_size,
        canvas_size=canvas_size,
        distortion_strength=distortion_strength,
        distortion_fn=distortion_fn,
        color_scheme=color_scheme,
        color_animation=color_animation,
        audio_reactive=audio_reactive
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
    """Démonstration en plein écran"""
    grid = create_deformed_grid(dimension=80, cell_size=20, distortion_strength=1, 
                               color_scheme="neon", color_animation=True, fullscreen=True)
    grid.run_interactive()


def audio_reactive_demo():
    """Démonstration avec réactivité audio - PARFAIT POUR LA MUSIQUE! 🎵"""
    grid = create_deformed_grid(
        dimension=64, 
        cell_size=18, 
        distortion_strength=1,  # Distorsion de base plus faible (l'audio l'augmente)
        distortion_fn="sine",
        color_scheme="neon", 
        color_animation=True, 
        audio_reactive=True,
        fullscreen=True
    )
    print("\n🎵 MODE AUDIO-RÉACTIF ACTIVÉ!")
    print("🎧 Lancez votre musique préférée et regardez l'art danser!")
    print("🔊 Plus la musique est forte, plus les effets sont intenses!")
    grid.run_interactive()


if __name__ == "__main__":
    # Choisir la démo à lancer
    print("🎨 Démonstrations disponibles:")
    print("1. quick_demo() - Démonstration rapide")
    print("2. fullscreen_demo() - Démonstration plein écran")
    print("3. audio_reactive_demo() - Démonstration audio-réactive")
    print("\nLancement de la démonstration plein écran...")
    fullscreen_demo()