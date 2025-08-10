import math
import pygame
from typing import Tuple
from .base_shape import BaseShape


class YinYang(BaseShape):
    """Moteur de rendu pour le symbole Yin-Yang."""

    @staticmethod
    def _invert_color(color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r, g, b = color
        return (255 - r, 255 - g, 255 - b)

    @staticmethod
    def _draw_filled_sector(surf: pygame.Surface, center: Tuple[float, float], radius: float,
                            start_angle: float, end_angle: float, color: Tuple[int, int, int], steps: int = 72):
        """
        Dessine un secteur plein (disque partiel) en reliant des points sur l'arc à son centre.
        Angles en radians (0 = axe +x, sens anti-horaire).
        """
        cx, cy = center
        points = [(cx, cy)]
        # Assurer start < end en gérant les tours complets
        if end_angle < start_angle:
            end_angle += 2 * math.pi
        for i in range(steps + 1):
            t = start_angle + (end_angle - start_angle) * (i / steps)
            x = cx + radius * math.cos(t)
            y = cy + radius * math.sin(t)
            points.append((x, y))
        pygame.draw.polygon(surf, color, points)

    @staticmethod
    def draw(surface, x: float, y: float, rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un Yin-Yang centré en (x, y).
        
        Args:
            surface: Surface pygame où dessiner.
            x, y: Position du centre.
            rotation: Rotation en radians (appliquée à l'ensemble du symbole).
            size: Diamètre du symbole.
            color: Couleur principale (l'autre couleur est son inverse RGB).
        """
        try:
            diameter = max(2, int(size))
            radius = diameter / 2.0

            primary = color
            secondary = YinYang._invert_color(color)

            # Surface temporaire avec alpha pour faciliter la rotation et le clipping circulaire
            temp = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
            temp = temp.convert_alpha()

            center = (radius, radius)

            # 1) Disque extérieur entièrement en 'primary'
            pygame.draw.circle(temp, primary, (int(center[0]), int(center[1])), int(radius))

            # 2) Peindre une demi-disque (gauche) en 'secondary' pour initier la séparation.
            #    Demi-cercle gauche = angles 90° -> 270° (en radians: pi/2 -> 3pi/2)
            YinYang._draw_filled_sector(
                temp, center, radius,
                start_angle=math.pi / 2,
                end_angle=3 * math.pi / 2,
                color=secondary,
                steps=90
            )

            # 3) Les deux lobes (disques de rayon R/2) le long de l'axe vertical :
            #    - lobe haut en 'primary'
            #    - lobe bas en 'secondary'
            lobe_r = radius / 2.0
            top_center = (radius, radius / 2.0)
            bot_center = (radius, radius + radius / 2.0)

            pygame.draw.circle(temp, primary, (int(top_center[0]), int(top_center[1])), int(lobe_r))
            pygame.draw.circle(temp, secondary, (int(bot_center[0]), int(bot_center[1])), int(lobe_r))

            # 4) Les deux petits points (traditionnellement ~R/8)
            dot_r = max(1, int(radius / 8.0))
            # Point dans le lobe haut (couleur opposée = secondary)
            pygame.draw.circle(temp, secondary, (int(top_center[0]), int(top_center[1])), dot_r)
            # Point dans le lobe bas (couleur opposée = primary)
            pygame.draw.circle(temp, primary, (int(bot_center[0]), int(bot_center[1])), dot_r)

            # 5) Re-clipping au disque extérieur pour éviter tout débordement (dessine un "cookie cutter")
            #    (optionnel ici car tout est déjà interne, mais on garantit la propreté des bords)
            mask = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255, 255), (int(center[0]), int(center[1])), int(radius))
            temp.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            # 6) Appliquer la rotation demandée et blitter au centre (x, y)
            deg = math.degrees(rotation or 0.0)
            rotated = pygame.transform.rotozoom(temp, -deg, 1.0)  # pygame: angle positif = sens horaire inversé
            rect = rotated.get_rect(center=(int(x), int(y)))
            surface.blit(rotated, rect.topleft)

        except (TypeError, ValueError):
            # Fallback: petit rectangle centré, comme dans Circle
            YinYang._draw_fallback(surface, x, y, color)
