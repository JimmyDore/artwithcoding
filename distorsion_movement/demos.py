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
                        fullscreen: bool = False,
                        mouse_interactive: bool = True,
                        mouse_strength: float = 0.7,
                        mouse_radius: float = 120.0) -> DeformedGrid:
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
        mouse_interactive: Si True, active les interactions souris
        mouse_strength: Force des interactions souris (0.0 à 1.0)
        mouse_radius: Rayon d'influence de la souris en pixels
    
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
        audio_reactive=audio_reactive,
        mouse_interactive=mouse_interactive,
        mouse_strength=mouse_strength,
        mouse_radius=mouse_radius
    )
    
    # Si plein écran demandé, l'activer immédiatement
    if fullscreen:
        grid.toggle_fullscreen()
    
    return grid


def quick_demo():
    """Démonstration rapide avec interactions souris activées"""
    print("🎮 Quick Demo - Mouse Interactions Enabled!")
    print("🖱️  Move your mouse to see attraction effects")
    print("🎯 Left click: ripple effects, Right click: burst effects")
    print("⌨️  TAB: toggle mouse, SPACE: change distortion, ESC: quit")
    
    grid = create_deformed_grid(
        dimension=48, 
        cell_size=16, 
        distortion_strength=0.3, 
        distortion_fn="sine",
        color_scheme="rainbow", 
        color_animation=True,
        mouse_interactive=True,
        mouse_strength=0.8,
        mouse_radius=140.0
    )
    grid.run_interactive()


def fullscreen_demo():
    """Démonstration en plein écran avec souris"""
    print("🎮 Fullscreen Demo - Immersive Mouse Experience!")
    print("🖱️  Your mouse controls the entire screen!")
    print("🎯 Try different areas - F: toggle fullscreen")
    
    grid = create_deformed_grid(
        dimension=64, 
        cell_size=18, 
        distortion_strength=1, 
        distortion_fn="perlin",
        color_scheme="neon", 
        color_animation=True, 
        fullscreen=True,
        mouse_interactive=False,
        mouse_strength=0.9,
        mouse_radius=60.0
    )
    grid.run_interactive()


def audio_reactive_demo():
    """Démonstration avec réactivité audio + souris - PARFAIT POUR LA MUSIQUE! 🎵"""
    print("\n🎵 AUDIO + MOUSE REACTIVE MODE!")
    print("🎧 Play your favorite music and watch art dance!")
    print("🖱️  Mouse + Music = Amazing visuals!")
    print("🔊 Louder music = more intense effects!")
    print("🎯 Mouse adds extra interactive layer!")
    
    grid = create_deformed_grid(
        dimension=56, 
        cell_size=16, 
        distortion_strength=0.4,  # Lower base distortion (audio + mouse will boost it)
        distortion_fn="sine",
        color_scheme="neon", 
        color_animation=True, 
        audio_reactive=True,
        fullscreen=True,
        mouse_interactive=True,
        mouse_strength=0.7,      # Moderate mouse strength to blend with audio
        mouse_radius=60.0
    )
    grid.run_interactive()


def mouse_demo():
    """Démonstration dédiée aux interactions souris"""
    print("🖱️  MOUSE INTERACTION SHOWCASE!")
    print("=" * 40)
    print("🎯 Features to try:")
    print("   • Move mouse around for attraction effects")
    print("   • Left click: Create ripple effects")
    print("   • Right click: Create burst effects")
    print("   • 1-7: Change mouse interaction types")
    print("   • TAB: Toggle mouse on/off")
    print("   • +/-: Adjust mouse strength")
    print("   • SPACE: Change base distortion")
    print("=" * 40)
    
    grid = create_deformed_grid(
        dimension=40,
        cell_size=18,
        distortion_strength=0.2,  # Low base so mouse effects are prominent
        distortion_fn="circular",
        color_scheme="ocean",
        color_animation=True,
        mouse_interactive=True,
        mouse_strength=1.0,       # Maximum mouse strength for demo
        mouse_radius=60.0        # Large radius for dramatic effects
    )
    grid.run_interactive()


if __name__ == "__main__":
    # Choisir la démo à lancer
    print("🎨 Démonstrations disponibles:")
    print("1. quick_demo() - Démonstration rapide avec souris")
    print("2. fullscreen_demo() - Démonstration plein écran avec souris")
    print("3. audio_reactive_demo() - Démonstration audio + souris")
    print("4. mouse_demo() - Showcase des interactions souris")
    print("\nLancement de la démonstration souris...")
    fullscreen_demo()