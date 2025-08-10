"""
Schéma de couleur duotone avec accent.
"""

from typing import Tuple
from .base_color import BaseColor


class DuotoneAccent(BaseColor):
    """Deux couleurs principales avec un accent rare."""
    
    @staticmethod
    def get_color_for_position(
        square_color: Tuple[int, int, int],
        x_norm: float, 
        y_norm: float, 
        distance_to_center: float, 
        index: int,
        dimension: int
    ) -> Tuple[int, int, int]:
        """
        Génère un duotone avec accent rare.
        
        Args:
            square_color: Couleur de base (non utilisée)
            x_norm: Position X normalisée (non utilisée)
            y_norm: Position Y normalisée (non utilisée)
            distance_to_center: Distance au centre (non utilisée)
            index: Index du carré dans la grille
            dimension: Dimension de la grille
            
        Returns:
            Couleur duotone avec accent occasionnel
        """
        color_a = (30, 144, 255)   # Dodger blue
        color_b = (255, 105, 180)  # Hot pink
        accent   = (255, 255, 0)   # Bright yellow pop

        row = index // dimension
        col = index % dimension
        
        # Use pseudo-random function based on position for unpredictable accent placement
        # This creates a deterministic but seemingly random pattern
        seed = (row * 73 + col * 151 + row * col * 23) % 997  # Large prime for better distribution
        
        # Rare accent: approximately 1 in 20-25 cells (4-5% chance)
        if seed < 40:  # 40/997 ≈ 4% chance
            return accent
        
        # More interesting duotone pattern: use Perlin-like noise for organic distribution
        # Combine multiple pattern scales for visual complexity
        pattern1 = (row // 2 + col // 2) % 2  # Larger checkerboard
        pattern2 = (row + col) % 3            # Diagonal stripes
        pattern3 = ((row * 3) % 7 + (col * 2) % 5) % 2  # Irregular pattern
        
        # Combine patterns for more organic distribution
        combined_pattern = (pattern1 + pattern2 + pattern3) % 2
        
        if combined_pattern == 0:
            return color_a
        else:
            return color_b