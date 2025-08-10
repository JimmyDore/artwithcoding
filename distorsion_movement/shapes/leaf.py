import math
import pygame
from typing import Tuple
from .base_shape import BaseShape


class Leaf(BaseShape):
    """Feuille = intersection (vesica) de deux disques identiques."""

    @staticmethod
    def _invert_color(c: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r, g, b = c
        return (255 - r, 255 - g, 255 - b)

    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        try:
            diameter = max(6, int(size))
            R = diameter / 2.0
            cx = cy = R

            # finesse: 0.35 (ronde) → 0.75 (pointue). Doit rester < 1.0
            offset_ratio = 0.55
            d = R * offset_ratio

            # 1) deux surfaces alpha avec cercles pleins
            s1 = pygame.Surface((diameter, diameter), pygame.SRCALPHA).convert_alpha()
            s2 = pygame.Surface((diameter, diameter), pygame.SRCALPHA).convert_alpha()

            pygame.draw.circle(s1, (255, 255, 255, 255), (int(cx - d), int(cy)), int(R))
            pygame.draw.circle(s2, (255, 255, 255, 255), (int(cx + d), int(cy)), int(R))

            # 2) conversion en masques + intersection
            m1 = pygame.mask.from_surface(s1)
            m2 = pygame.mask.from_surface(s2)
            inter = m1.overlap_mask(m2, (0, 0))  # même surface: offset (0,0)

            # 3) rendre le masque d’intersection sur une surface colorée
            temp = pygame.Surface((diameter, diameter), pygame.SRCALPHA).convert_alpha()
            leaf_surface = inter.to_surface(setcolor=color + (255,), unsetcolor=(0, 0, 0, 0))
            temp.blit(leaf_surface, (0, 0))

            # 4) (optionnel) petite nervure centrale & contour anti-alias
            pygame.draw.aaline(temp, Leaf._invert_color(color), (cx, cy - R), (cx, cy + R))
            outline_pts = inter.outline()  # liste de points bord du masque
            if len(outline_pts) > 2:
                pygame.draw.aalines(temp, Leaf._invert_color(color), True, outline_pts)

            # 5) rotation + blit
            deg = math.degrees(rotation or 0.0)
            rotated = pygame.transform.rotozoom(temp, -deg, 1.0)
            rect = rotated.get_rect(center=(int(x), int(y)))
            surface.blit(rotated, rect.topleft)

        except (TypeError, ValueError):
            Leaf._draw_fallback(surface, x, y, color)
