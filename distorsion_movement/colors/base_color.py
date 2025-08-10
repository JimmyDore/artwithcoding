"""
Module de base pour les schémas de couleurs.

Ce module contient la classe de base et les fonctionnalités communes
à tous les schémas de couleurs utilisés dans le système de grilles déformées.
"""

import math
import colorsys
from typing import Tuple


class BaseColor:
    """Classe de base pour tous les schémas de couleurs."""
    
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
        Génère une couleur pour une position donnée selon le schéma de couleur.
        
        Cette méthode doit être implémentée par chaque schéma de couleur spécifique.
        
        Args:
            square_color: Couleur de base pour le schéma monochrome
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            dimension: Dimension de la grille (pour calculs)
            
        Returns:
            Tuple RGB (r, g, b)
        """
        raise NotImplementedError("Chaque schéma de couleur doit implémenter cette méthode")
    
    @staticmethod
    def _clamp_rgb(r: float, g: float, b: float) -> Tuple[int, int, int]:
        """
        Assure que les valeurs RGB sont dans la plage valide [0, 255].
        
        Args:
            r, g, b: Valeurs RGB (peuvent être des floats)
            
        Returns:
            Tuple RGB avec valeurs entières clampées
        """
        return (
            max(0, min(255, int(r))),
            max(0, min(255, int(g))),
            max(0, min(255, int(b)))
        )
    
    @staticmethod
    def _blend_colors(color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
                     blend: float) -> Tuple[int, int, int]:
        """
        Mélange deux couleurs selon un facteur de mélange.
        
        Args:
            color1: Première couleur RGB
            color2: Deuxième couleur RGB
            blend: Facteur de mélange (0.0 = color1, 1.0 = color2)
            
        Returns:
            Couleur mélangée RGB
        """
        blend = max(0.0, min(1.0, blend))  # Clamp blend factor
        r = color1[0] + (color2[0] - color1[0]) * blend
        g = color1[1] + (color2[1] - color1[1]) * blend
        b = color1[2] + (color2[2] - color1[2]) * blend
        return BaseColor._clamp_rgb(r, g, b)
    
    @staticmethod
    def _hsv_to_rgb_clamped(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """
        Convertit HSV en RGB avec clamping automatique.
        
        Args:
            h: Hue (0.0 à 1.0)
            s: Saturation (0.0 à 1.0)
            v: Value/Brightness (0.0 à 1.0)
            
        Returns:
            Tuple RGB avec valeurs entières clampées
        """
        # Clamp input values
        h = h % 1.0  # Wrap hue
        s = max(0.0, min(1.0, s))
        v = max(0.0, min(1.0, v))
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return BaseColor._clamp_rgb(r * 255, g * 255, b * 255)