import math
import pygame
from typing import Tuple
from .base_shape import BaseShape


class Ellipsis(BaseShape):
    """Moteur de rendu pour une ellipse (cercle étiré) avec rotation."""

    @staticmethod
    def _invert_color(c: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r, g, b = c
        return (255 - r, 255 - g, 255 - b)

    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine une ellipse centrée en (x, y).

        Args:
            surface: Surface pygame où dessiner.
            x, y: Position du centre.
            rotation: Rotation en radians.
            size: Axe majeur (diamètre principal) de l’ellipse.
            color: Couleur de remplissage (RGB).
        """
        try:
            major = max(2, int(size))   # axe majeur
            # Ratio d’aspect (minor/major). 1.0 = cercle, 0.6 = ellipse aplatie
            # Si ton moteur a un système d'extras (ex: BaseShape.extras.get("aspect")),
            # tu peux le brancher ici.
            aspect = 0.6
            minor = max(1, int(major * aspect))

            # surface temporaire pile à la taille de l'ellipse
            temp = pygame.Surface((major, minor), pygame.SRCALPHA).convert_alpha()

            # ellipse pleine
            rect = pygame.Rect(0, 0, major, minor)
            pygame.draw.ellipse(temp, color, rect)

            # (optionnel) léger contour anti-alias pour un bord plus net
            outline = Ellipsis._invert_color(color)
            pygame.draw.ellipse(temp, outline, rect, width=1)

            # rotation + blit centré
            deg = math.degrees(rotation or 0.0)
            rotated = pygame.transform.rotozoom(temp, -deg, 1.0)
            rect_out = rotated.get_rect(center=(int(x), int(y)))
            surface.blit(rotated, rect_out.topleft)

        except (TypeError, ValueError):
            Ellipsis._draw_fallback(surface, x, y, color)
