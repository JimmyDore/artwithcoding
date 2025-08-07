"""
Art Génératif avec Palette Limitée et Contraintes Esthétiques

Ce script implémente l'idée #3 : palette limitée avec contrainte esthétique.
Concept : Choisir une palette (4-6 couleurs inspirées d'artistes) et imposer 
des contraintes pour créer des rythmes visuels intéressants.

Contraintes implémentées :
- Pas plus de 2 couleurs identiques côte à côte
- Pas 3 fois la même couleur de suite dans une ligne/colonne
- Distribution équilibrée des couleurs
- Patterns rythmiques basés sur des règles esthétiques
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List, Tuple, Dict
from enum import Enum

class PaletteStyle(Enum):
    KANDINSKY = "kandinsky"
    BAUHAUS = "bauhaus" 
    MONDRIAN = "mondrian"
    KLEE = "klee"
    ROTHKO = "rothko"
    MATISSE = "matisse"

def get_artistic_palette(style: PaletteStyle) -> Dict[str, Tuple[float, float, float]]:
    """
    Définit des palettes de couleurs inspirées d'artistes célèbres.
    
    Args:
        style (PaletteStyle): Style artistique choisi
    
    Returns:
        Dict[str, Tuple[float, float, float]]: Dictionnaire des couleurs RGB normalisées
    """
    palettes = {
        PaletteStyle.KANDINSKY: {
            "rouge_vif": (0.8, 0.1, 0.1),
            "bleu_profond": (0.1, 0.2, 0.7),
            "jaune_pur": (0.9, 0.9, 0.1),
            "noir": (0.1, 0.1, 0.1),
            "blanc": (0.95, 0.95, 0.95)
        },
        
        PaletteStyle.BAUHAUS: {
            "rouge_bauhaus": (0.75, 0.15, 0.15),
            "bleu_bauhaus": (0.15, 0.35, 0.65),
            "jaune_bauhaus": (0.85, 0.75, 0.15),
            "gris_moyen": (0.5, 0.5, 0.5),
            "blanc_casse": (0.9, 0.9, 0.85)
        },
        
        PaletteStyle.MONDRIAN: {
            "rouge_primaire": (0.85, 0.2, 0.2),
            "bleu_primaire": (0.2, 0.3, 0.8),
            "jaune_primaire": (0.9, 0.85, 0.2),
            "noir_structure": (0.05, 0.05, 0.05),
            "blanc_pur": (0.98, 0.98, 0.98)
        },
        
        PaletteStyle.KLEE: {
            "orange_terre": (0.8, 0.5, 0.2),
            "vert_olive": (0.4, 0.6, 0.3),
            "brun_chaud": (0.5, 0.3, 0.2),
            "bleu_gris": (0.3, 0.4, 0.5),
            "ocre_clair": (0.8, 0.7, 0.4)
        },
        
        PaletteStyle.ROTHKO: {
            "rouge_sombre": (0.6, 0.2, 0.2),
            "orange_brule": (0.7, 0.4, 0.2),
            "marron_profond": (0.3, 0.2, 0.15),
            "rouge_cadmium": (0.8, 0.3, 0.2),
            "noir_velours": (0.15, 0.1, 0.1)
        },
        
        PaletteStyle.MATISSE: {
            "bleu_cobalt": (0.2, 0.4, 0.8),
            "rouge_vermillon": (0.9, 0.3, 0.2),
            "vert_emeraude": (0.2, 0.7, 0.4),
            "jaune_chrome": (0.9, 0.8, 0.2),
            "violet_outremer": (0.5, 0.2, 0.6)
        }
    }
    
    return palettes[style]

class ConstraintValidator:
    """Classe pour valider les contraintes esthétiques"""
    
    @staticmethod
    def check_adjacent_constraint(grid: np.ndarray, row: int, col: int, color_idx: int) -> bool:
        """
        Vérifie qu'il n'y a pas plus de 2 couleurs identiques adjacentes.
        
        Args:
            grid: Grille actuelle
            row, col: Position à vérifier
            color_idx: Index de la couleur à placer
            
        Returns:
            bool: True si la contrainte est respectée
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # droite, gauche, bas, haut
        
        for dr, dc in directions:
            # Compter les couleurs identiques dans cette direction
            count = 0
            r, c = row + dr, col + dc
            
            while (0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and 
                   grid[r, c] == color_idx):
                count += 1
                r, c = r + dr, c + dc
            
            if count >= 2:  # Déjà 2 couleurs identiques dans cette direction
                return False
                
        return True
    
    @staticmethod
    def check_line_constraint(grid: np.ndarray, row: int, col: int, color_idx: int) -> bool:
        """
        Vérifie qu'il n'y a pas 3 couleurs identiques de suite dans une ligne/colonne.
        
        Args:
            grid: Grille actuelle
            row, col: Position à vérifier
            color_idx: Index de la couleur à placer
            
        Returns:
            bool: True si la contrainte est respectée
        """
        # Vérifier ligne horizontale
        if col >= 2:
            if grid[row, col-1] == color_idx and grid[row, col-2] == color_idx:
                return False
        
        if col >= 1 and col < grid.shape[1] - 1:
            if grid[row, col-1] == color_idx and grid[row, col+1] == color_idx:
                return False
                
        if col <= grid.shape[1] - 3:
            if grid[row, col+1] == color_idx and grid[row, col+2] == color_idx:
                return False
        
        # Vérifier colonne verticale
        if row >= 2:
            if grid[row-1, col] == color_idx and grid[row-2, col] == color_idx:
                return False
        
        if row >= 1 and row < grid.shape[0] - 1:
            if grid[row-1, col] == color_idx and grid[row+1, col] == color_idx:
                return False
                
        if row <= grid.shape[0] - 3:
            if grid[row+1, col] == color_idx and grid[row+2, col] == color_idx:
                return False
        
        return True

def generate_constrained_grid(dimension: int, style: PaletteStyle, 
                            max_attempts: int = 1000) -> Tuple[np.ndarray, Dict[str, Tuple[float, float, float]]]:
    """
    Génère une grille avec contraintes esthétiques selon une palette artistique.
    
    Args:
        dimension: Taille de la grille
        style: Style artistique de la palette
        max_attempts: Nombre maximum de tentatives pour placer une couleur
        
    Returns:
        Tuple[np.ndarray, Dict]: Grille d'indices de couleurs et palette utilisée
    """
    palette = get_artistic_palette(style)
    color_names = list(palette.keys())
    num_colors = len(color_names)
    
    # Grille d'indices de couleurs (-1 = pas encore assigné)
    grid = np.full((dimension, dimension), -1, dtype=int)
    validator = ConstraintValidator()
    
    # Remplir la grille pixel par pixel
    for i in range(dimension):
        for j in range(dimension):
            attempts = 0
            placed = False
            
            # Mélanger l'ordre des couleurs pour plus de variété
            color_indices = np.random.permutation(num_colors).tolist()
            
            for color_idx in color_indices:
                if attempts >= max_attempts:
                    break
                    
                # Vérifier les contraintes
                if (validator.check_adjacent_constraint(grid, i, j, color_idx) and
                    validator.check_line_constraint(grid, i, j, color_idx)):
                    grid[i, j] = color_idx
                    placed = True
                    break
                    
                attempts += 1
            
            # Si aucune couleur ne respecte les contraintes, prendre une couleur aléatoire
            if not placed:
                grid[i, j] = random.randint(0, num_colors - 1)
    
    return grid, palette

def grid_to_rgb(grid: np.ndarray, palette: Dict[str, Tuple[float, float, float]]) -> np.ndarray:
    """
    Convertit une grille d'indices de couleurs en grille RGB.
    
    Args:
        grid: Grille d'indices de couleurs
        palette: Dictionnaire des couleurs RGB
        
    Returns:
        np.ndarray: Grille RGB de forme (dimension, dimension, 3)
    """
    color_values = list(palette.values())
    dimension = grid.shape[0]
    rgb_grid = np.zeros((dimension, dimension, 3))
    
    for i in range(dimension):
        for j in range(dimension):
            color_idx = grid[i, j]
            if 0 <= color_idx < len(color_values):
                rgb_grid[i, j] = color_values[color_idx]
    
    return rgb_grid

def display_constrained_grid(grid: np.ndarray, palette: Dict[str, Tuple[float, float, float]], 
                           style: PaletteStyle, title: str = None, figsize: Tuple[int, int] = (12, 10)):
    """
    Affiche une grille avec contraintes avec la légende des couleurs.
    
    Args:
        grid: Grille d'indices de couleurs
        palette: Dictionnaire des couleurs
        style: Style artistique utilisé
        title: Titre personnalisé
        figsize: Taille de la figure
    """
    rgb_grid = grid_to_rgb(grid, palette)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, 
                                   gridspec_kw={'width_ratios': [4, 1]})
    
    # Afficher la grille principale
    ax1.imshow(rgb_grid, interpolation='nearest')
    if title is None:
        title = f"Art Génératif - Style {style.value.title()} ({grid.shape[0]}×{grid.shape[1]})"
    ax1.set_title(title, fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Afficher la légende des couleurs
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, len(palette))
    ax2.set_title("Palette", fontsize=12, fontweight='bold')
    
    for i, (name, color) in enumerate(palette.items()):
        # Rectangle de couleur
        rect = plt.Rectangle((0.1, i + 0.1), 0.3, 0.8, facecolor=color, edgecolor='black', linewidth=1)
        ax2.add_patch(rect)
        # Nom de la couleur
        ax2.text(0.5, i + 0.5, name.replace('_', ' ').title(), 
                fontsize=10, va='center', ha='left')
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, len(palette))
    ax2.axis('off')
    
    plt.tight_layout()
    plt.show()

def save_constrained_grid(grid: np.ndarray, palette: Dict[str, Tuple[float, float, float]], 
                         style: PaletteStyle, filename: str = None, dpi: int = 300):
    """
    Sauvegarde une grille avec contraintes.
    
    Args:
        grid: Grille d'indices de couleurs
        palette: Dictionnaire des couleurs
        style: Style artistique utilisé
        filename: Nom du fichier (optionnel)
        dpi: Résolution de l'image
    """
    if filename is None:
        filename = f"palette_constraints_{style.value}_{grid.shape[0]}x{grid.shape[1]}.png"
    
    rgb_grid = grid_to_rgb(grid, palette)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 10), 
                                   gridspec_kw={'width_ratios': [4, 1]})
    
    # Grille principale
    ax1.imshow(rgb_grid, interpolation='nearest')
    ax1.set_title(f"Art Génératif - Style {style.value.title()} ({grid.shape[0]}×{grid.shape[1]})", 
                  fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Légende
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, len(palette))
    ax2.set_title("Palette", fontsize=12, fontweight='bold')
    
    for i, (name, color) in enumerate(palette.items()):
        rect = plt.Rectangle((0.1, i + 0.1), 0.3, 0.8, facecolor=color, edgecolor='black', linewidth=1)
        ax2.add_patch(rect)
        ax2.text(0.5, i + 0.5, name.replace('_', ' ').title(), 
                fontsize=10, va='center', ha='left')
    
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, len(palette))
    ax2.axis('off')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi, bbox_inches='tight', pad_inches=0.2)
    plt.close()
    print(f"Grille avec contraintes sauvegardée sous {filename}")

def compare_styles(dimension: int = 32, figsize: Tuple[int, int] = (20, 15)):
    """
    Compare tous les styles artistiques disponibles.
    
    Args:
        dimension: Taille des grilles à générer
        figsize: Taille de la figure globale
    """
    styles = list(PaletteStyle)
    num_styles = len(styles)
    cols = 3
    rows = (num_styles + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    axes = axes.flatten() if num_styles > 1 else [axes]
    
    for i, style in enumerate(styles):
        print(f"Génération du style {style.value}...")
        grid, palette = generate_constrained_grid(dimension, style)
        rgb_grid = grid_to_rgb(grid, palette)
        
        axes[i].imshow(rgb_grid, interpolation='nearest')
        axes[i].set_title(f'{style.value.title()}', fontsize=12, fontweight='bold')
        axes[i].axis('off')
    
    # Masquer les axes inutilisés
    for i in range(num_styles, len(axes)):
        axes[i].axis('off')
    
    plt.suptitle(f'Comparaison des Styles Artistiques avec Contraintes ({dimension}×{dimension})', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def analyze_constraints_effectiveness(dimension: int = 64, style: PaletteStyle = PaletteStyle.KANDINSKY):
    """
    Analyse l'efficacité des contraintes en comparant avec/sans contraintes.
    
    Args:
        dimension: Taille de la grille
        style: Style artistique à utiliser
    """
    # Avec contraintes
    print("Génération avec contraintes...")
    constrained_grid, palette = generate_constrained_grid(dimension, style)
    
    # Sans contraintes (placement aléatoire)
    print("Génération sans contraintes...")
    color_names = list(palette.keys())
    random_grid = np.random.randint(0, len(color_names), (dimension, dimension))
    
    # Affichage comparatif
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Avec contraintes
    rgb_constrained = grid_to_rgb(constrained_grid, palette)
    ax1.imshow(rgb_constrained, interpolation='nearest')
    ax1.set_title(f'AVEC Contraintes\n{style.value.title()}', fontsize=14, fontweight='bold')
    ax1.axis('off')
    
    # Sans contraintes
    rgb_random = grid_to_rgb(random_grid, palette)
    ax2.imshow(rgb_random, interpolation='nearest')
    ax2.set_title(f'SANS Contraintes\n{style.value.title()}', fontsize=14, fontweight='bold')
    ax2.axis('off')
    
    plt.suptitle(f'Efficacité des Contraintes Esthétiques ({dimension}×{dimension})', 
                 fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    return constrained_grid, random_grid, palette

if __name__ == "__main__":
    print("=== Art Génératif avec Palette Limitée et Contraintes Esthétiques ===\n")
    
    # 1. Exemple avec le style Kandinsky
    print("1. Génération style Kandinsky avec contraintes...")
    grid_kandinsky, palette_kandinsky = generate_constrained_grid(64, PaletteStyle.KANDINSKY)
    display_constrained_grid(grid_kandinsky, palette_kandinsky, PaletteStyle.KANDINSKY)
    save_constrained_grid(grid_kandinsky, palette_kandinsky, PaletteStyle.KANDINSKY)
    
    # 2. Comparaison de tous les styles
    print("\n2. Comparaison de tous les styles artistiques...")
    compare_styles(32)
    
    # 3. Analyse de l'efficacité des contraintes
    print("\n3. Analyse de l'efficacité des contraintes...")
    constrained, random, palette = analyze_constraints_effectiveness(48, PaletteStyle.BAUHAUS)
    
    # 4. Exemples haute résolution
    print("\n4. Exemples haute résolution...")
    for style in [PaletteStyle.MONDRIAN, PaletteStyle.MATISSE]:
        print(f"   Génération {style.value}...")
        grid, palette = generate_constrained_grid(128, style)
        save_constrained_grid(grid, palette, style)
    
    print("\n=== Exemples d'utilisation ===")
    print("Pour générer une grille avec contraintes :")
    print("  grid, palette = generate_constrained_grid(64, PaletteStyle.KANDINSKY)")
    print("  display_constrained_grid(grid, palette, PaletteStyle.KANDINSKY)")
    print("\nStyles disponibles :")
    for style in PaletteStyle:
        print(f"  PaletteStyle.{style.name}")