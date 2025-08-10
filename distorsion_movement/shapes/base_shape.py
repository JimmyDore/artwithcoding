"""
Module de base pour les formes géométriques.

Ce module contient les fonctionnalités communes à toutes les formes,
notamment la rotation des points et les fonctions utilitaires.
"""

import pygame
import math
from typing import Tuple, List


class BaseShape:
    """Classe de base pour toutes les formes géométriques."""
    
    @staticmethod
    def _rotate_points(points: List[Tuple[float, float]], rotation: float, 
                      center_x: float, center_y: float) -> List[Tuple[int, int]]:
        """
        Applique une rotation à une liste de points autour d'un centre.
        
        Args:
            points: Liste de tuples (x, y) relatifs au centre
            rotation: Angle de rotation en radians
            center_x, center_y: Centre de rotation
            
        Returns:
            Liste de points rotés en coordonnées absolues (entiers)
        """
        rotated_points = []
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        
        for point_x, point_y in points:
            new_x = point_x * cos_r - point_y * sin_r + center_x
            new_y = point_x * sin_r + point_y * cos_r + center_y
            
            # Validation des coordonnées (éviter NaN/Inf)
            if math.isfinite(new_x) and math.isfinite(new_y):
                rotated_points.append((int(new_x), int(new_y)))
            else:
                # Fallback vers la position centrale si coordonnées invalides
                rotated_points.append((int(center_x), int(center_y)))
        
        return rotated_points
    
    @staticmethod
    def _draw_fallback(surface, x: float, y: float, color: Tuple[int, int, int]):
        """
        Dessine un petit rectangle comme fallback en cas d'erreur.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            color: Couleur RGB
        """
        rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
        pygame.draw.rect(surface, color, rect)