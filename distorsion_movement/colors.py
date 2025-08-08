"""
Générateurs de couleurs pour les différents schémas disponibles.
"""

import math
import colorsys
from typing import Tuple

from distorsion_movement.enums import ColorScheme


class ColorGenerator:
    """
    Générateur de couleurs selon différents schémas.
    """
    
    @staticmethod
    def get_color_for_position(color_scheme: str, square_color: Tuple[int, int, int],
                              x_norm: float, y_norm: float, 
                              distance_to_center: float, index: int,
                              dimension: int) -> Tuple[int, int, int]:
        """
        Génère une couleur pour une position donnée selon le schéma de couleur actuel.
        
        Args:
            color_scheme: Nom du schéma de couleur
            square_color: Couleur de base pour le schéma monochrome
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            dimension: Dimension de la grille (pour calculs)
            
        Returns:
            Tuple RGB (r, g, b)
        """
        if color_scheme == "monochrome":
            return square_color
            
        elif color_scheme == "black_white_radial":
            # Noir et blanc radial - distribution basée sur la distance au centre
            # Les formes au centre tendent vers le blanc, celles aux bords vers le noir
            if distance_to_center < 0.3:
                return (255, 255, 255)  # Blanc au centre
            elif distance_to_center > 0.7:
                return (0, 0, 0)  # Noir aux bords
            else:
                # Zone intermédiaire : alternance selon l'index
                return (255, 255, 255) if (index % 2 == 0) else (0, 0, 0)
        
        elif color_scheme == "black_white_alternating":
            # Noir et blanc alternance claire - damier/checkerboard pattern
            row = index // dimension
            col = index % dimension
            # Pattern damier classique
            is_white = (row + col) % 2 == 0
            return (255, 255, 255) if is_white else (0, 0, 0)
            
        elif color_scheme == "gradient":
            # Gradient diagonal du coin supérieur gauche au coin inférieur droit
            t = (x_norm + y_norm) / 2.0
            r = int(50 + t * 205)
            g = int(100 + t * 155)
            b = int(200 - t * 100)
            return (r, g, b)
            
        elif color_scheme == "rainbow":
            # Arc-en-ciel basé sur la position
            hue = (x_norm + y_norm * 0.5) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif color_scheme == "complementary":
            # Couleurs complémentaires alternées
            if (index + (index // dimension)) % 2 == 0:
                return (255, 100, 50)  # Orange
            else:
                return (50, 150, 255)  # Bleu
                
        elif color_scheme == "temperature":
            # Couleurs chaudes au centre, froides aux bords
            temp = 1.0 - distance_to_center
            if temp > 0.7:
                # Très chaud - rouge/jaune
                r, g, b = colorsys.hsv_to_rgb(0.1, 0.8, 1.0)
            elif temp > 0.4:
                # Chaud - orange/rouge
                r, g, b = colorsys.hsv_to_rgb(0.05, 0.9, 0.9)
            else:
                # Froid - bleu/violet
                r, g, b = colorsys.hsv_to_rgb(0.6 + temp * 0.2, 0.7, 0.8)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif color_scheme == "pastel":
            # Couleurs pastel douces
            hue = (x_norm * 0.3 + y_norm * 0.7) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.3, 0.9)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif color_scheme == "neon":
            # Couleurs néon vives
            hue = (distance_to_center + x_norm * 0.5) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif color_scheme == "ocean":
            # Thème océan - bleus et verts
            depth = distance_to_center
            if depth < 0.3:
                # Eau peu profonde - turquoise
                return (64, 224, 208)
            elif depth < 0.7:
                # Eau moyenne - bleu océan
                return (0, 119, 190)
            else:
                # Eau profonde - bleu foncé
                return (25, 25, 112)
                
        elif color_scheme == "fire":
            # Thème feu - rouges, oranges, jaunes
            intensity = 1.0 - distance_to_center + y_norm * 0.3
            if intensity > 0.8:
                return (255, 255, 100)  # Jaune chaud
            elif intensity > 0.5:
                return (255, 140, 0)    # Orange
            else:
                return (220, 20, 60)    # Rouge foncé
                
        elif color_scheme == "forest":
            # Thème forêt - verts variés
            green_intensity = 0.3 + distance_to_center * 0.7 + x_norm * 0.2
            if green_intensity > 0.8:
                return (144, 238, 144)  # Vert clair
            elif green_intensity > 0.5:
                return (34, 139, 34)    # Vert forêt
            else:
                return (0, 100, 0)      # Vert foncé

        elif color_scheme == "analogous":
            base_hue = 0.3  # green-ish
            hue_shift = (x_norm - 0.5) * 0.3 + (y_norm - 0.5) * 0.3  # ±0.3 spread
            sat = 0.5 + 0.5 * (0.5 - distance_to_center)  # more saturated near center
            val = 0.7 + 0.3 * math.sin(index * 0.1)  # subtle brightness wave
            r, g, b = colorsys.hsv_to_rgb((base_hue + hue_shift) % 1.0, sat, val)
            return (int(r*255), int(g*255), int(b*255))

        
        # Par défaut, retourner blanc
        return (255, 255, 255)
    
    @staticmethod
    def get_animated_color(base_color: Tuple[int, int, int], 
                          position_index: int,
                          time: float,
                          color_animation: bool,
                          audio_reactive: bool,
                          audio_analyzer=None) -> Tuple[int, int, int]:
        """
        Applique une animation de couleur si activée.
        
        Args:
            base_color: Couleur de base du carré
            position_index: Index de position pour variation
            time: Temps actuel pour l'animation
            color_animation: Si l'animation normale est activée
            audio_reactive: Si l'animation audio-réactive est activée
            audio_analyzer: Instance de l'analyseur audio (optionnel)
            
        Returns:
            Couleur animée ou couleur de base si animation désactivée
        """
        # Si aucune animation n'est activée, retourner la couleur de base
        if not color_animation and not audio_reactive:
            return base_color
        
        r, g, b = base_color
        
        # Appliquer l'animation normale seulement si color_animation est True
        if color_animation and (not audio_reactive or not audio_analyzer):
            pulse = math.sin(time * 2 + position_index * 0.1) * 0.2 + 1.0
            pulse = max(0.5, min(1.5, pulse))
            r = int(min(255, r * pulse))
            g = int(min(255, g * pulse))
            b = int(min(255, b * pulse))
            return (r, g, b)
        
        # Si seul audio_reactive est activé (mais pas color_animation)
        if audio_reactive and audio_analyzer and not color_animation:
            # Ne pas appliquer l'animation normale, aller directement à l'audio
            pass
        # Si les deux sont activés, appliquer d'abord l'animation normale
        elif color_animation and audio_reactive and audio_analyzer:
            pulse = math.sin(time * 2 + position_index * 0.1) * 0.2 + 1.0
            pulse = max(0.5, min(1.5, pulse))
            r = int(min(255, r * pulse))
            g = int(min(255, g * pulse))
            b = int(min(255, b * pulse))
        # Si ni l'un ni l'autre ne s'applique, retourner la couleur de base
        elif not audio_reactive or not audio_analyzer:
            return base_color
        
        # Animation réactive à l'audio
        audio_features = audio_analyzer.get_audio_features()
        
        # Beat detection - flash blanc sur les beats
        if audio_features['beat_detected']:
            flash_intensity = 0.7
            r = int(min(255, r + (255 - r) * flash_intensity))
            g = int(min(255, g + (255 - g) * flash_intensity))
            b = int(min(255, b + (255 - b) * flash_intensity))
        
        # Hautes fréquences - augmentent la luminosité
        high_boost = 1.0 + audio_features['high_level'] * 0.5
        r = int(min(255, r * high_boost))
        g = int(min(255, g * high_boost))
        b = int(min(255, b * high_boost))
        
        # Moyennes fréquences - rotation de teinte
        if audio_features['mid_level'] > 0.1:
            # Convertir en HSV pour rotation de teinte
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + audio_features['mid_level'] * 0.3) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        return (r, g, b)