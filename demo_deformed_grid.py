#!/usr/bin/env python3
"""
Démonstration du générateur de grilles déformées

Ce script montre différents exemples d'utilisation du module deformed_grid
avec diverses configurations et types de distorsion.
"""

from deformed_grid import DeformedGrid, create_deformed_grid, DistortionType
import time


def demo_basic():
    """Démonstration basique avec distorsion aléatoire"""
    print("=== Démonstration Basique ===")
    print("Grille 32x32 avec distorsion aléatoire")
    
    grid = create_deformed_grid(
        dimension=32,
        cell_size=15,
        distortion_strength=0.3,
        distortion_fn="random"
    )
    grid.run_interactive()


def demo_animated_sine():
    """Démonstration avec animation sinusoïdale"""
    print("=== Démonstration Animation Sinusoïdale ===")
    print("Grille 40x40 avec distorsion sinusoïdale animée")
    
    grid = create_deformed_grid(
        dimension=40,
        cell_size=12,
        distortion_strength=0.5,
        distortion_fn="sine"
    )
    grid.animation_speed = 0.03  # Animation plus rapide
    grid.run_interactive()


def demo_perlin_organic():
    """Démonstration avec effet organique (Perlin)"""
    print("=== Démonstration Effet Organique ===")
    print("Grille 48x48 avec distorsion type Perlin")
    
    grid = create_deformed_grid(
        dimension=48,
        cell_size=10,
        distortion_strength=0.4,
        distortion_fn="perlin"
    )
    grid.animation_speed = 0.015  # Animation lente et fluide
    grid.run_interactive()


def demo_circular_waves():
    """Démonstration avec ondes circulaires"""
    print("=== Démonstration Ondes Circulaires ===")
    print("Grille 50x50 avec distorsion circulaire depuis le centre")
    
    grid = create_deformed_grid(
        dimension=50,
        cell_size=9,
        distortion_strength=0.6,
        distortion_fn="circular"
    )
    grid.animation_speed = 0.04
    grid.run_interactive()


def demo_high_density():
    """Démonstration haute densité"""
    print("=== Démonstration Haute Densité ===")
    print("Grille 80x80 avec petits carrés")
    
    grid = create_deformed_grid(
        dimension=80,
        cell_size=6,
        distortion_strength=0.25,
        distortion_fn="sine"
    )
    grid.run_interactive()


def demo_custom_colors():
    """Démonstration avec couleurs personnalisées"""
    print("=== Démonstration Couleurs Personnalisées ===")
    print("Grille avec palette de couleurs artistique")
    
    grid = DeformedGrid(
        dimension=36,
        cell_size=16,
        canvas_size=(800, 600),
        distortion_strength=0.4,
        distortion_fn="perlin",
        background_color=(15, 25, 35),      # Bleu foncé
        square_color=(255, 200, 100)        # Orange chaud
    )
    grid.run_interactive()


def demo_minimal_tremor():
    """Démonstration avec tremblement minimal"""
    print("=== Démonstration Tremblement Minimal ===")
    print("Effet subtil de tremblement de grille")
    
    grid = create_deformed_grid(
        dimension=60,
        cell_size=8,
        distortion_strength=0.15,  # Distorsion très légère
        distortion_fn="sine"
    )
    grid.animation_speed = 0.01  # Animation très lente
    grid.run_interactive()


def demo_batch_export():
    """Démonstration d'export en lot"""
    print("=== Démonstration Export en Lot ===")
    print("Génération et sauvegarde de plusieurs variations...")
    
    configurations = [
        ("random_low", "random", 0.2),
        ("random_high", "random", 0.7),
        ("sine_medium", "sine", 0.4),
        ("perlin_organic", "perlin", 0.5),
        ("circular_waves", "circular", 0.6),
    ]
    
    for name, distortion_type, strength in configurations:
        print(f"Génération: {name}")
        grid = create_deformed_grid(
            dimension=48,
            cell_size=10,
            distortion_strength=strength,
            distortion_fn=distortion_type
        )
        
        # Rendre une fois pour initialiser
        grid.render()
        
        # Sauvegarder
        filename = f"demo_{name}_48x48.png"
        grid.save_image(filename)
        print(f"  -> {filename}")
        
        # Petite pause pour éviter les conflits
        time.sleep(0.1)
    
    print("Export terminé!")


def main():
    """Menu principal de démonstration"""
    demos = {
        "1": ("Démonstration basique", demo_basic),
        "2": ("Animation sinusoïdale", demo_animated_sine),
        "3": ("Effet organique (Perlin)", demo_perlin_organic),
        "4": ("Ondes circulaires", demo_circular_waves),
        "5": ("Haute densité", demo_high_density),
        "6": ("Couleurs personnalisées", demo_custom_colors),
        "7": ("Tremblement minimal", demo_minimal_tremor),
        "8": ("Export en lot", demo_batch_export),
    }
    
    print("🎨 Démonstrations - Grille Déformée")
    print("=" * 40)
    
    for key, (description, _) in demos.items():
        print(f"{key}. {description}")
    
    print("\nChoisissez une démonstration (1-8) ou 'q' pour quitter:")
    
    while True:
        choice = input("> ").strip().lower()
        
        if choice == 'q':
            print("Au revoir!")
            break
        elif choice in demos:
            _, demo_func = demos[choice]
            try:
                demo_func()
            except KeyboardInterrupt:
                print("\nDémonstration interrompue.")
            except Exception as e:
                print(f"Erreur: {e}")
            
            print("\nChoisissez une autre démonstration ou 'q' pour quitter:")
        else:
            print("Choix invalide. Utilisez 1-8 ou 'q'.")


if __name__ == "__main__":
    main()