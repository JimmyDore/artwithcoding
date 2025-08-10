"""
Rendu de flocon de Koch.
"""

import pygame
import math
from typing import Tuple
from .base_shape import BaseShape


class KochSnowflake(BaseShape):
    """Moteur de rendu pour les flocons de Koch."""
    
    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int], depth: int = 3):
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
        rotated = KochSnowflake._rotate_points(pts, rotation, x, y)

        # Dessin : polyligne fermée (contour 1 px)
        try:
            if len(rotated) >= 2:
                pygame.draw.lines(surface, color, True, rotated, 1)
            else:
                KochSnowflake._draw_fallback(surface, x, y, color)
        except (TypeError, ValueError):
            KochSnowflake._draw_fallback(surface, x, y, color)