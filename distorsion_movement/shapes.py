"""
Moteur de rendu pour différents types de formes géométriques.

Ce module fournit des fonctions pour dessiner diverses formes géométriques
avec support de la rotation, du dimensionnement et du positionnement.
"""

import pygame
import math
import numpy as np
from typing import Tuple, List


class ShapeRenderer:
    """Moteur de rendu pour différentes formes géométriques."""
    
    @staticmethod
    def draw_square(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un carré avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du carré
            color: Couleur RGB
        """
        half_size = size // 2
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        
        rotated_corners = ShapeRenderer._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback: dessiner un petit rectangle centré
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
    @staticmethod
    def draw_circle(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un cercle (la rotation n'affecte pas un cercle parfait).
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians (ignorée pour les cercles)
            size: Diamètre du cercle
            color: Couleur RGB
        """
        try:
            radius = max(1, size // 2)
            pygame.draw.circle(surface, color, (int(x), int(y)), radius)
        except (TypeError, ValueError):
            # Fallback: dessiner un petit rectangle centré
            rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
            pygame.draw.rect(surface, color, rect)
    
    @staticmethod
    def draw_triangle(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un triangle équilatéral avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du triangle (rayon du cercle circonscrit)
            color: Couleur RGB
        """
        radius = size // 2
        # Triangle équilatéral avec un sommet vers le haut
        corners = []
        for i in range(3):
            angle = (2 * math.pi * i / 3) - math.pi/2  # Commencer par le haut
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = ShapeRenderer._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
    @staticmethod
    def draw_hexagon(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un hexagone régulier avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille de l'hexagone (rayon du cercle circonscrit)
            color: Couleur RGB
        """
        radius = size // 2
        corners = []
        for i in range(6):
            angle = 2 * math.pi * i / 6
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = ShapeRenderer._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
    @staticmethod
    def draw_pentagon(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un pentagone régulier avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du pentagone (rayon du cercle circonscrit)
            color: Couleur RGB
        """
        radius = size // 2
        corners = []
        for i in range(5):
            angle = (2 * math.pi * i / 5) - math.pi/2  # Commencer par le haut
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = ShapeRenderer._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
    @staticmethod
    def draw_star(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine une étoile à 5 branches avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille de l'étoile (rayon du cercle circonscrit externe)
            color: Couleur RGB
        """
        outer_radius = size // 2
        inner_radius = outer_radius * 0.4  # Rayon interne plus petit
        
        corners = []
        for i in range(10):  # 5 points externes + 5 points internes
            angle = (2 * math.pi * i / 10) - math.pi/2  # Commencer par le haut
            if i % 2 == 0:  # Points externes
                radius = outer_radius
            else:  # Points internes
                radius = inner_radius
            
            corner_x = radius * math.cos(angle)
            corner_y = radius * math.sin(angle)
            corners.append((corner_x, corner_y))
        
        rotated_corners = ShapeRenderer._rotate_points(corners, rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
    @staticmethod
    def draw_diamond(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un losange (carré à 45°) avec rotation.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians
            size: Taille du losange
            color: Couleur RGB
        """
        half_size = size // 2
        # Losange = carré tourné de 45°
        base_rotation = math.pi / 4  # 45 degrés
        total_rotation = rotation + base_rotation
        
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        
        rotated_corners = ShapeRenderer._rotate_points(corners, total_rotation, x, y)
        
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
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
    def draw_koch_snowflake(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int], depth: int = 3):
        """
        Dessine un flocon de Koch (contour) autour d'un triangle équilatéral.

        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre
            rotation: Rotation en radians (appliquée à la forme finale)
            size: Taille (rayon du cercle circonscrit du triangle de base)
            color: Couleur RGB
            depth: Profondeur de récursion (0-6 recommandé)
        """
        # Sécurité / limites
        depth = max(0, min(int(depth), 6))  # profondeur raisonnable pour éviter trop de points
        radius = max(2, size // 2)

        # Triangle équilatéral centré, pointant vers le haut (comme vos autres formes)
        base_angles = [
            -math.pi / 2,
            -math.pi / 2 + 2 * math.pi / 3,
            -math.pi / 2 + 4 * math.pi / 3,
        ]
        base_pts = [(radius * math.cos(a), radius * math.sin(a)) for a in base_angles]

        # Génère la courbe de Koch pour chaque côté du triangle
        def koch_curve(p1, p2, d):
            if d == 0:
                return [p1, p2]
            # points 1/3 et 2/3 sur le segment
            x1, y1 = p1
            x2, y2 = p2
            dx, dy = (x2 - x1), (y2 - y1)
            pA = (x1 + dx / 3.0, y1 + dy / 3.0)
            pB = (x1 + 2.0 * dx / 3.0, y1 + 2.0 * dy / 3.0)
            # sommet du "pic" (équilateral) : rotation +60° du segment pA->pB
            angle60 = math.pi / 3.0
            ux, uy = (pB[0] - pA[0]), (pB[1] - pA[1])
            # rotation (ux,uy) de +60°
            vx = ux * math.cos(angle60) - uy * math.sin(angle60)
            vy = ux * math.sin(angle60) + uy * math.cos(angle60)
            pC = (pA[0] + vx, pA[1] + vy)

            # récurse sur 4 segments
            seg1 = koch_curve(p1, pA, d - 1)
            seg2 = koch_curve(pA, pC, d - 1)
            seg3 = koch_curve(pC, pB, d - 1)
            seg4 = koch_curve(pB, p2, d - 1)

            # concaténer en évitant de dupliquer les points de jonction
            return seg1[:-1] + seg2[:-1] + seg3[:-1] + seg4

        # Construire la liste de points pour le flocon (fermé)
        pts = []
        for i in range(3):
            p1 = base_pts[i]
            p2 = base_pts[(i + 1) % 3]
            edge_pts = koch_curve(p1, p2, depth)
            if i < 2:
                pts += edge_pts[:-1]  # éviter duplication du dernier point
            else:
                pts += edge_pts  # dernier côté garde le dernier point pour fermer

        # Appliquer rotation et translation via votre helper
        rotated = ShapeRenderer._rotate_points(pts, rotation, x, y)

        # Dessin : polyligne fermée (contour 1 px)
        try:
            if len(rotated) >= 2:
                pygame.draw.lines(surface, color, True, rotated, 1)
            else:
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
        except (TypeError, ValueError):
            rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
            pygame.draw.rect(surface, color, rect)


def get_shape_renderer_function(shape_type: str):
    """
    Retourne la fonction de rendu correspondant au type de forme.
    
    Args:
        shape_type: Type de forme (valeur de ShapeType)
        
    Returns:
        Fonction de rendu appropriée
    """
    shape_functions = {
        "square": ShapeRenderer.draw_square,
        "circle": ShapeRenderer.draw_circle,
        "triangle": ShapeRenderer.draw_triangle,
        "hexagon": ShapeRenderer.draw_hexagon,
        "pentagon": ShapeRenderer.draw_pentagon,
        "star": ShapeRenderer.draw_star,
        "diamond": ShapeRenderer.draw_diamond,
        "koch_snowflake": ShapeRenderer.draw_koch_snowflake,
    }
    
    return shape_functions.get(shape_type, ShapeRenderer.draw_square)