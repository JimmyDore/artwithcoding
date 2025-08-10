"""
Package de schémas de couleurs.

Ce package contient tous les générateurs de couleurs pour différents schémas
utilisés dans le système de grilles déformées.
"""

from .base_color import BaseColor
from .monochrome import Monochrome
from .black_white_radial import BlackWhiteRadial
from .black_white_alternating import BlackWhiteAlternating
from .gradient import Gradient
from .rainbow import Rainbow
from .complementary import Complementary
from .temperature import Temperature
from .pastel import Pastel
from .neon import Neon
from .ocean import Ocean
from .fire import Fire
from .forest import Forest
from .analogous import Analogous
from .cyberpunk import Cyberpunk
from .aurora_borealis import AuroraBorealis
from .infrared_thermal import InfraredThermal
from .duotone_accent import DuotoneAccent
from .desert import Desert
from .metallics import Metallics
from .reggae import Reggae
from .sunset import Sunset
from .pop_art import PopArt
from .vaporwave import Vaporwave
from .candy_shop import CandyShop


# Registre des schémas de couleurs disponibles
COLOR_SCHEME_REGISTRY = {
    "monochrome": Monochrome.get_color_for_position,
    "black_white_radial": BlackWhiteRadial.get_color_for_position,
    "black_white_alternating": BlackWhiteAlternating.get_color_for_position,
    "gradient": Gradient.get_color_for_position,
    "rainbow": Rainbow.get_color_for_position,
    "complementary": Complementary.get_color_for_position,
    "temperature": Temperature.get_color_for_position,
    "pastel": Pastel.get_color_for_position,
    "neon": Neon.get_color_for_position,
    "ocean": Ocean.get_color_for_position,
    "fire": Fire.get_color_for_position,
    "forest": Forest.get_color_for_position,
    "analogous": Analogous.get_color_for_position,
    "cyberpunk": Cyberpunk.get_color_for_position,
    "aurora_borealis": AuroraBorealis.get_color_for_position,
    "infrared_thermal": InfraredThermal.get_color_for_position,
    "duotone_accent": DuotoneAccent.get_color_for_position,
    "desert": Desert.get_color_for_position,
    "metallics": Metallics.get_color_for_position,
    "reggae": Reggae.get_color_for_position,
    "sunset": Sunset.get_color_for_position,
    "pop_art": PopArt.get_color_for_position,
    "vaporwave": Vaporwave.get_color_for_position,
    "candy_shop": CandyShop.get_color_for_position,
}


def get_color_scheme_function(color_scheme: str):
    """
    Retourne la fonction de génération de couleur correspondant au schéma de couleur.
    
    Args:
        color_scheme: Nom du schéma de couleur
        
    Returns:
        Fonction de génération de couleur appropriée
    """
    return COLOR_SCHEME_REGISTRY.get(color_scheme, Monochrome.get_color_for_position)


class ColorGenerator:
    """
    Générateur de couleurs selon différents schémas - version refactorisée.
    
    Cette classe sert de point d'entrée principal pour maintenir la compatibilité
    avec l'ancienne interface tout en utilisant la nouvelle architecture modulaire.
    """
    
    @staticmethod
    def get_color_for_position(color_scheme: str, square_color, 
                              x_norm: float, y_norm: float, 
                              distance_to_center: float, index: int,
                              dimension: int):
        """
        Génère une couleur pour une position donnée selon le schéma de couleur actuel.
        
        Cette méthode maintient la compatibilité avec l'ancienne interface
        tout en utilisant la nouvelle architecture modulaire.
        
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
        color_function = get_color_scheme_function(color_scheme)
        return color_function(
            square_color, x_norm, y_norm, distance_to_center, index, dimension
        )
    
    @staticmethod
    def get_animated_color(base_color, position_index: int, time: float, color_animation: bool):
        """
        Applique une animation de couleur si activée.
        
        Cette méthode reste inchangée pour maintenir la compatibilité.
        
        Args:
            base_color: Couleur de base du carré
            position_index: Index de position pour variation
            time: Temps actuel pour l'animation
            color_animation: Si l'animation normale est activée
            
        Returns:
            Couleur animée ou couleur de base si animation désactivée
        """
        import math
        
        # Si aucune animation n'est activée, retourner la couleur de base
        if not color_animation:
            return base_color
        
        r, g, b = base_color
        
        # Appliquer l'animation normale seulement si color_animation est True
        if color_animation:
            pulse = math.sin(time * 2 + position_index * 0.1) * 0.2 + 1.0
            pulse = max(0.5, min(1.5, pulse))
            r = int(min(255, r * pulse))
            g = int(min(255, g * pulse))
            b = int(min(255, b * pulse))
            return (r, g, b)


__all__ = [
    'BaseColor',
    'Monochrome', 'BlackWhiteRadial', 'BlackWhiteAlternating', 'Gradient', 'Rainbow',
    'Complementary', 'Temperature', 'Pastel', 'Neon', 'Ocean', 'Fire', 'Forest',
    'Analogous', 'Cyberpunk', 'AuroraBorealis', 'InfraredThermal', 'DuotoneAccent',
    'Desert', 'Metallics', 'Reggae', 'Sunset', 'PopArt', 'Vaporwave', 'CandyShop',
    'ColorGenerator',
    'get_color_scheme_function',
    'COLOR_SCHEME_REGISTRY'
]