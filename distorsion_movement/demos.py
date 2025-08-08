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
        audio_reactive: Si True, réagit à l'audio en temps réel
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
        dimension=128, 
        cell_size=20, 
        distortion_strength=1, 
        distortion_fn="lens",
        color_scheme="complementary", 
        color_animation=True, 
        fullscreen=True,
        shape_type="square",  # Commencer avec des carrés
        mixed_shapes=False     # Formes mixtes activées
    )
    print("\n🔷 NOUVELLES FORMES DISPONIBLES!")
    print("🎮 Utilisez 'H' pour changer de forme:")
    print("   - Carrés, Cercles, Triangles, Hexagones, Pentagones, Étoiles, Losanges")
    print("🎲 'Shift+H' bascule entre forme unique et formes mixtes")
    print("🎨 Les nouvelles formes réagissent aux couleurs et distorsions!")
    grid.run_interactive()


def star_demo():
    """Démonstration avec seulement des étoiles - Magique! ⭐"""
    grid = create_deformed_grid(
        dimension=64,
        cell_size=18,
        distortion_strength=0.7,
        distortion_fn="circular",
        color_scheme="fire",
        color_animation=True,
        fullscreen=False,
        shape_type="star",        # SEULEMENT des étoiles
        mixed_shapes=False        # Forme unique
    )
    print("\n⭐ DÉMO ÉTOILES SEULEMENT!")
    print("🌟 Toutes les cellules sont des étoiles dorées")
    print("🎮 Utilisez 'H' pour changer vers d'autres formes")
    grid.run_interactive()


def hexagon_demo():
    """Démonstration avec seulement des hexagones - Géométrique! 🔶"""
    grid = create_deformed_grid(
        dimension=60,
        cell_size=16,
        distortion_strength=0.5,
        distortion_fn="perlin",
        color_scheme="ocean",
        color_animation=True,
        fullscreen=False,
        shape_type="hexagon",     # SEULEMENT des hexagones
        mixed_shapes=False        # Forme unique
    )
    print("\n🔶 DÉMO HEXAGONES SEULEMENT!")
    print("🏯 Pattern géométrique uniforme avec hexagones")
    print("🎮 Utilisez 'H' pour explorer d'autres formes")
    grid.run_interactive()


def triangle_demo():
    """Démonstration avec seulement des triangles - Tribal! 🔺"""
    grid = create_deformed_grid(
        dimension=70,
        cell_size=14,
        distortion_strength=0.9,
        distortion_fn="random",
        color_scheme="complementary",
        color_animation=True,
        fullscreen=False,
        shape_type="triangle",    # SEULEMENT des triangles
        mixed_shapes=False        # Forme unique
    )
    print("\n🔺 DÉMO TRIANGLES SEULEMENT!")
    print("⚡ Style tribal avec triangles dynamiques")
    print("🎮 Utilisez 'H' pour tester autres formes")
    grid.run_interactive()


def shapes_showcase_demo():
    """Démonstration spéciale pour mettre en valeur toutes les formes disponibles 🎭"""
    grid = create_deformed_grid(
        dimension=64,
        cell_size=18,
        distortion_strength=0.6,
        distortion_fn="circular",
        color_scheme="rainbow",
        color_animation=True,
        fullscreen=False,
        shape_type="star",
        mixed_shapes=True
    )
    print("\n🎭 VITRINE DES FORMES!")
    print("🔄 Cette démo affiche toutes les formes en mode mixte")
    print("🎨 Essayez 'H' pour changer de forme principale")
    print("🎲 'Shift+H' pour basculer en mode forme unique")
    print("🌈 Toutes les formes supportent couleurs et animations!")
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
        fullscreen=True,
        shape_type="hexagon",  # Commencer avec des hexagones
        mixed_shapes=False     # Forme unique pour un effet cohérent
    )
    print("\n🎵 MODE AUDIO-RÉACTIF ACTIVÉ!")
    print("🎧 Lancez votre musique préférée et regardez l'art danser!")
    print("🔊 Plus la musique est forte, plus les effets sont intenses!")
    print("🔷 Forme: hexagones (utilisez 'H' pour changer)")
    grid.run_interactive()


if __name__ == "__main__":
    # Choisir la démo à lancer
    print("🎨 Démonstrations disponibles:")
    print("1. quick_demo() - Démonstration rapide")
    print("2. fullscreen_demo() - Cercles en plein écran")
    print("3. star_demo() - Seulement des étoiles ⭐")
    print("4. hexagon_demo() - Seulement des hexagones 🔶")
    print("5. triangle_demo() - Seulement des triangles 🔺")
    print("6. shapes_showcase_demo() - Vitrine formes mixtes")
    print("7. audio_reactive_demo() - Démonstration audio-réactive")
    print("\n🔷 FORMES UNIQUES vs MIXTES:")
    print("   ✨ Démos 2-5: UNE SEULE forme (mixed_shapes=False)")
    print("   🎲 Démo 6: FORMES MIXTES (mixed_shapes=True)")
    print("   🎮 Dans toutes les démos: 'H' change la forme, 'Shift+H' bascule le mode")
    print("\nLancement de la démonstration étoiles...")
    fullscreen_demo()