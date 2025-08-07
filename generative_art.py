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


def display_multiple_grids(dimensions, figsize=(20, 12)):
    """
    Affiche plusieurs grilles de différentes dimensions sur la même vue.
    
    Args:
        dimensions (list): Liste des dimensions à afficher
        figsize (tuple): Taille de la figure globale
    """
    num_grids = len(dimensions)
    
    # Calculer le nombre de colonnes (3 par ligne max pour une bonne lisibilité)
    cols = min(3, num_grids)
    rows = (num_grids + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    
    # S'assurer que axes est toujours un tableau 2D
    if rows == 1 and cols == 1:
        axes = np.array([[axes]])
    elif rows == 1:
        axes = axes.reshape(1, -1)
    elif cols == 1:
        axes = axes.reshape(-1, 1)
    
    for i, dimension in enumerate(dimensions):
        row = i // cols
        col = i % cols
        
        print(f"Génération de la grille {dimension}x{dimension}...")
        grid = generate_color_grid_vectorized(dimension)
        
        ax = axes[row, col]
        ax.imshow(grid, interpolation='nearest')
        ax.set_title(f'{dimension}×{dimension}', fontsize=14, fontweight='bold')
        ax.axis('off')
    
    # Masquer les axes inutilisés
    for i in range(num_grids, rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col].axis('off')
    
    plt.suptitle('Art Génératif - Comparaison de Résolutions', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.show()


def save_multiple_grids(dimensions, filename="generative_art_comparison.png", figsize=(20, 12), dpi=300):
    """
    Sauvegarde plusieurs grilles de différentes dimensions dans un fichier.
    
    Args:
        dimensions (list): Liste des dimensions à afficher
        filename (str): Nom du fichier de sortie
        figsize (tuple): Taille de la figure globale
        dpi (int): Résolution de l'image
    """
    num_grids = len(dimensions)
    cols = min(3, num_grids)
    rows = (num_grids + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    
    # S'assurer que axes est toujours un tableau 2D
    if rows == 1 and cols == 1:
        axes = np.array([[axes]])
    elif rows == 1:
        axes = axes.reshape(1, -1)
    elif cols == 1:
        axes = axes.reshape(-1, 1)
    
    for i, dimension in enumerate(dimensions):
        row = i // cols
        col = i % cols
        
        grid = generate_color_grid_vectorized(dimension)
        
        ax = axes[row, col]
        ax.imshow(grid, interpolation='nearest')
        ax.set_title(f'{dimension}×{dimension}', fontsize=14, fontweight='bold')
        ax.axis('off')
    
    # Masquer les axes inutilisés
    for i in range(num_grids, rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col].axis('off')
    
    plt.suptitle('Art Génératif - Comparaison de Résolutions', fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"Comparaison sauvegardée sous {filename}")


if __name__ == "__main__":
    # Affichage de plusieurs grilles de dimensions croissantes
    print("Génération de grilles de carrés colorés - Comparaison de résolutions...")
    
    # Dimensions demandées : 16, 32, 64, 128, 256, 512
    dimensions = [16, 32, 64, 128, 256, 512]
    
    # Afficher toutes les grilles sur la même vue
    display_multiple_grids(dimensions)
    
    # Sauvegarder la comparaison
    save_multiple_grids(dimensions, "comparaison_resolutions.png")
    
    print("\nComparaison terminée ! Vous pouvez voir l'évolution de la résolution.")
    print("Plus la dimension augmente, plus les détails deviennent fins.")
    
    # Exemple optionnel : affichage d'une seule grille haute résolution
    print("\nGénération d'une grille haute résolution 512x512...")
    high_res_grid = generate_color_grid_vectorized(512)
    display_grid(high_res_grid, "Art Génératif - Haute Résolution 512x512", figsize=(12, 12))