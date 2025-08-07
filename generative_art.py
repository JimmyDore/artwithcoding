"""
Générateur d'art génératif - Grille de carrés colorés
"""
import numpy as np
import matplotlib.pyplot as plt
import random
import time


def get_color_scheme(color_scheme):
    """
    Définit les plages de couleurs pour différents schémas.
    
    Args:
        color_scheme (str): Le schéma de couleur choisi
    
    Returns:
        dict: Plages min/max pour chaque canal RGB
    """
    schemes = {
        'random': {'r': (0, 1), 'g': (0, 1), 'b': (0, 1)},
        'reds': {'r': (0.5, 1), 'g': (0, 0.3), 'b': (0, 0.3)},
        'blues': {'r': (0, 0.3), 'g': (0, 0.5), 'b': (0.5, 1)},
        'greens': {'r': (0, 0.3), 'g': (0.5, 1), 'b': (0, 0.4)},
        'purples': {'r': (0.4, 1), 'g': (0, 0.4), 'b': (0.5, 1)},
        'oranges': {'r': (0.7, 1), 'g': (0.3, 0.8), 'b': (0, 0.3)},
        'yellows': {'r': (0.8, 1), 'g': (0.8, 1), 'b': (0, 0.4)},
        'cyans': {'r': (0, 0.3), 'g': (0.6, 1), 'b': (0.6, 1)},
        'magentas': {'r': (0.6, 1), 'g': (0, 0.4), 'b': (0.6, 1)},
        'warm': {'r': (0.5, 1), 'g': (0.3, 0.8), 'b': (0, 0.4)},
        'cool': {'r': (0, 0.4), 'g': (0.3, 0.8), 'b': (0.5, 1)},
        'pastels': {'r': (0.7, 1), 'g': (0.7, 1), 'b': (0.7, 1)},
        'darks': {'r': (0, 0.4), 'g': (0, 0.4), 'b': (0, 0.4)},
        'monochrome': {'r': (0, 1), 'g': (0, 1), 'b': (0, 1)},  # Spécial : même valeur pour R, G, B
    }
    
    return schemes.get(color_scheme.lower(), schemes['random'])


def generate_color_grid(dimension, color_scheme='random'):
    """
    Génère une grille de carrés colorés aléatoirement selon un schéma de couleur.
    
    Args:
        dimension (int): Taille de la grille (dimension x dimension)
        color_scheme (str): Schéma de couleur ('random', 'reds', 'blues', etc.)
    
    Returns:
        numpy.ndarray: Grille de couleurs RGB de forme (dimension, dimension, 3)
    """
    # Créer une grille vide pour stocker les couleurs RGB
    grid = np.zeros((dimension, dimension, 3))
    
    # Obtenir le schéma de couleur
    scheme = get_color_scheme(color_scheme)
    
    # Remplir chaque pixel avec une couleur aléatoire selon le schéma
    for i in range(dimension):
        for j in range(dimension):
            if color_scheme.lower() == 'monochrome':
                # Pour monochrome, utiliser la même valeur pour R, G, B
                gray_value = random.uniform(scheme['r'][0], scheme['r'][1])
                grid[i, j] = [gray_value, gray_value, gray_value]
            else:
                # Générer des valeurs RGB dans les plages définies
                r = random.uniform(scheme['r'][0], scheme['r'][1])
                g = random.uniform(scheme['g'][0], scheme['g'][1])
                b = random.uniform(scheme['b'][0], scheme['b'][1])
                grid[i, j] = [r, g, b]
    
    return grid


def display_grid(grid, title="Grille de carrés colorés", figsize=(10, 10), auto_close=True):
    """
    Affiche la grille de couleurs dans une fenêtre graphique.
    
    Args:
        grid (numpy.ndarray): Grille de couleurs RGB
        title (str): Titre de la fenêtre
        figsize (tuple): Taille de la figure (largeur, hauteur)
        auto_close (bool): Ferme automatiquement la fenêtre après 1 seconde
    """
    plt.figure(figsize=figsize)
    plt.imshow(grid, interpolation='nearest')
    plt.title(title, fontsize=16)
    plt.axis('off')  # Masquer les axes pour un rendu plus propre
    plt.tight_layout()
    
    if auto_close:
        plt.show(block=False)
        plt.pause(1)  # Affiche pendant 1 seconde
        plt.close()
    else:
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


def generate_color_grid_vectorized(dimension, color_scheme='random'):
    """
    Version optimisée utilisant numpy pour générer la grille selon un schéma de couleur.
    Plus rapide pour des dimensions importantes.
    
    Args:
        dimension (int): Taille de la grille (dimension x dimension)
        color_scheme (str): Schéma de couleur ('random', 'reds', 'blues', etc.)
    
    Returns:
        numpy.ndarray: Grille de couleurs RGB de forme (dimension, dimension, 3)
    """
    # Obtenir le schéma de couleur
    scheme = get_color_scheme(color_scheme)
    
    if color_scheme.lower() == 'monochrome':
        # Pour monochrome, générer une seule valeur et l'appliquer aux 3 canaux
        gray_values = np.random.uniform(scheme['r'][0], scheme['r'][1], (dimension, dimension, 1))
        return np.repeat(gray_values, 3, axis=2)
    else:
        # Générer des valeurs pour chaque canal dans les plages définies
        r_channel = np.random.uniform(scheme['r'][0], scheme['r'][1], (dimension, dimension))
        g_channel = np.random.uniform(scheme['g'][0], scheme['g'][1], (dimension, dimension))
        b_channel = np.random.uniform(scheme['b'][0], scheme['b'][1], (dimension, dimension))
        
        return np.stack([r_channel, g_channel, b_channel], axis=2)


def display_multiple_grids(dimensions, color_scheme='random', figsize=(20, 12), auto_close=True):
    """
    Affiche plusieurs grilles de différentes dimensions sur la même vue.
    
    Args:
        dimensions (list): Liste des dimensions à afficher
        color_scheme (str): Schéma de couleur à utiliser
        figsize (tuple): Taille de la figure globale
        auto_close (bool): Ferme automatiquement la fenêtre après 1 seconde
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
        
        print(f"Génération de la grille {dimension}x{dimension} ({color_scheme})...")
        grid = generate_color_grid_vectorized(dimension, color_scheme)
        
        ax = axes[row, col]
        ax.imshow(grid, interpolation='nearest')
        ax.set_title(f'{dimension}×{dimension}', fontsize=14, fontweight='bold')
        ax.axis('off')
    
    # Masquer les axes inutilisés
    for i in range(num_grids, rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col].axis('off')
    
    plt.suptitle(f'Art Génératif - {color_scheme.title()} - Comparaison de Résolutions', 
                 fontsize=18, fontweight='bold')
    plt.tight_layout()
    
    if auto_close:
        plt.show(block=False)
        plt.pause(1)  # Affiche pendant 1 seconde
        plt.close()
    else:
        plt.show()


def save_multiple_grids(dimensions, color_scheme='random', filename="generative_art_comparison.png", figsize=(20, 12), dpi=300):
    """
    Sauvegarde plusieurs grilles de différentes dimensions dans un fichier.
    
    Args:
        dimensions (list): Liste des dimensions à afficher
        color_scheme (str): Schéma de couleur à utiliser
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
        
        grid = generate_color_grid_vectorized(dimension, color_scheme)
        
        ax = axes[row, col]
        ax.imshow(grid, interpolation='nearest')
        ax.set_title(f'{dimension}×{dimension}', fontsize=14, fontweight='bold')
        ax.axis('off')
    
    # Masquer les axes inutilisés
    for i in range(num_grids, rows * cols):
        row = i // cols
        col = i % cols
        axes[row, col].axis('off')
    
    plt.suptitle(f'Art Génératif - {color_scheme.title()} - Comparaison de Résolutions', 
                 fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"Comparaison sauvegardée sous {filename}")


def display_color_schemes_comparison(dimension=64, auto_close=True):
    """
    Affiche une comparaison de différents schémas de couleur sur une même dimension.
    
    Args:
        dimension (int): Dimension de la grille à utiliser pour la comparaison
        auto_close (bool): Ferme automatiquement la fenêtre après 1 seconde
    """
    color_schemes = ['random', 'reds', 'blues', 'greens', 'purples', 'oranges', 
                    'yellows', 'cyans', 'warm', 'cool', 'pastels', 'monochrome']
    
    num_schemes = len(color_schemes)
    cols = 4
    rows = (num_schemes + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(16, 12))
    axes = axes.flatten()
    
    grids = []
    for i, scheme in enumerate(color_schemes):
        print(f"Génération {scheme}...")
        grid = generate_color_grid_vectorized(dimension, scheme)
        grids.append(grid)
        
        axes[i].imshow(grid, interpolation='nearest')
        axes[i].set_title(f'{scheme.title()}', fontsize=12, fontweight='bold')
        axes[i].axis('off')
    
    # Masquer les axes inutilisés
    for i in range(num_schemes, len(axes)):
        axes[i].axis('off')
    
    plt.suptitle(f'Comparaison des Schémas de Couleur ({dimension}×{dimension})', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    if auto_close:
        plt.show(block=False)
        plt.pause(1)  # Affiche pendant 1 seconde
        plt.close()
    else:
        plt.show()

    return grids[0]  # Return the first grid for compatibility


if __name__ == "__main__":
    print("=== Art Génératif avec Contrôle des Couleurs ===\n")

    # 0. Multiples grilles de base
    print("0. Multiples grilles de base...")
    dimensions = [16, 32, 64, 128, 256, 512]
    display_multiple_grids(dimensions)
    save_multiple_grids(dimensions, "comparaison_base.png")

    # 1. Comparaison des schémas de couleur
    print("1. Comparaison des différents schémas de couleur...")
    grid = display_color_schemes_comparison(64)
    save_grid(grid, "comparaison_color_schemes.png")

    
    # 2. Exemple avec des rouges sur différentes résolutions
    print("\n2. Génération de grilles ROUGES - Comparaison de résolutions...")
    dimensions = [16, 32, 64, 128, 256, 512]
    display_multiple_grids(dimensions, color_scheme='reds')
    save_multiple_grids(dimensions, 'reds', "comparaison_reds.png")
    
    # 3. Exemple avec des bleus
    print("\n3. Génération de grilles BLEUES - Comparaison de résolutions...")
    display_multiple_grids(dimensions, color_scheme='blues')
    save_multiple_grids(dimensions, 'blues', "comparaison_blues.png")
    
    # 4. Exemple avec des tons chauds
    print("\n4. Génération de grilles TONS CHAUDS...")
    display_multiple_grids(dimensions, color_scheme='warm')
    save_multiple_grids(dimensions, 'warm', "comparaison_warm.png")
    
    # 5. Grille haute résolution en monochrome
    print("\n5. Grille haute résolution en MONOCHROME...")
    mono_grid = generate_color_grid_vectorized(256, 'monochrome')
    display_grid(mono_grid, "Art Génératif - Monochrome 256x256", figsize=(10, 10))
    save_grid(mono_grid, "monochrome_256x256.png")


    print("\n=== Exemples d'utilisation ===")
    print("Pour utiliser un schéma de couleur spécifique :")
    print("  grid = generate_color_grid_vectorized(64, 'reds')")
    print("  display_grid(grid, 'Mon art en rouge')")
    print("\nSchémas disponibles :")
    schemes = ['random', 'reds', 'blues', 'greens', 'purples', 'oranges', 
              'yellows', 'cyans', 'magentas', 'warm', 'cool', 'pastels', 'darks', 'monochrome']
    print("  " + ", ".join(schemes))