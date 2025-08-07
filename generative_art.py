"""
Générateur d'art génératif - Grille de carrés colorés
"""
import numpy as np
import matplotlib.pyplot as plt
import random


def generate_color_grid(dimension):
    """
    Génère une grille de carrés colorés aléatoirement.
    
    Args:
        dimension (int): Taille de la grille (dimension x dimension)
    
    Returns:
        numpy.ndarray: Grille de couleurs RGB de forme (dimension, dimension, 3)
    """
    # Créer une grille vide pour stocker les couleurs RGB
    grid = np.zeros((dimension, dimension, 3))
    
    # Remplir chaque pixel avec une couleur aléatoire
    for i in range(dimension):
        for j in range(dimension):
            # Générer des valeurs RGB aléatoires entre 0 et 1
            r = random.random()
            g = random.random()
            b = random.random()
            grid[i, j] = [r, g, b]
    
    return grid


def display_grid(grid, title="Grille de carrés colorés", figsize=(10, 10)):
    """
    Affiche la grille de couleurs dans une fenêtre graphique.
    
    Args:
        grid (numpy.ndarray): Grille de couleurs RGB
        title (str): Titre de la fenêtre
        figsize (tuple): Taille de la figure (largeur, hauteur)
    """
    plt.figure(figsize=figsize)
    plt.imshow(grid, interpolation='nearest')
    plt.title(title, fontsize=16)
    plt.axis('off')  # Masquer les axes pour un rendu plus propre
    plt.tight_layout()
    plt.show()


def save_grid(grid, filename="generative_art.png", dpi=300):
    """
    Sauvegarde la grille de couleurs dans un fichier image.
    
    Args:
        grid (numpy.ndarray): Grille de couleurs RGB
        filename (str): Nom du fichier de sortie
        dpi (int): Résolution de l'image
    """
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, interpolation='nearest')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0)
    plt.close()
    print(f"Image sauvegardée sous {filename}")


def generate_color_grid_vectorized(dimension):
    """
    Version optimisée utilisant numpy pour générer la grille.
    Plus rapide pour des dimensions importantes.
    
    Args:
        dimension (int): Taille de la grille (dimension x dimension)
    
    Returns:
        numpy.ndarray: Grille de couleurs RGB de forme (dimension, dimension, 3)
    """
    return np.random.rand(dimension, dimension, 3)


if __name__ == "__main__":
    # Exemple d'utilisation avec une grille 64x64
    print("Génération d'une grille 64x64 de carrés colorés...")
    
    # Générer la grille
    color_grid = generate_color_grid_vectorized(64)
    
    # Afficher la grille
    display_grid(color_grid, "Art Génératif - Grille 64x64")
    
    # Optionnel : sauvegarder l'image
    save_grid(color_grid, "art_generatif_64x64.png")
    
    # Exemple avec une grille plus petite pour voir les détails
    print("\nGénération d'une grille 16x16 pour voir les détails...")
    small_grid = generate_color_grid(16)
    display_grid(small_grid, "Art Génératif - Grille 16x16 (détaillée)", figsize=(8, 8))