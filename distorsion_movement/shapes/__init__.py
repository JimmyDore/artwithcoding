"""
Package de formes géométriques.

Ce package contient tous les moteurs de rendu pour différentes formes
géométriques utilisées dans le système de grilles déformées.
"""

from .base_shape import BaseShape
from .square import Square
from .circle import Circle
from .triangle import Triangle
from .hexagon import Hexagon
from .pentagon import Pentagon
from .star import Star
from .diamond import Diamond
from .koch_snowflake import KochSnowflake
from .ring import Ring


# Registre des formes disponibles
SHAPE_REGISTRY = {
    "square": Square.draw,
    "circle": Circle.draw,
    "triangle": Triangle.draw,
    "hexagon": Hexagon.draw,
    "pentagon": Pentagon.draw,
    "star": Star.draw,
    "diamond": Diamond.draw,
    "koch_snowflake": KochSnowflake.draw,
    "ring": Ring.draw,
}


def get_shape_renderer_function(shape_type: str):
    """
    Retourne la fonction de rendu correspondant au type de forme.
    
    Args:
        shape_type: Type de forme (valeur de ShapeType)
        
    Returns:
        Fonction de rendu appropriée
    """
    return SHAPE_REGISTRY.get(shape_type, Square.draw)

__all__ = [
    'BaseShape',
    'Square', 'Circle', 'Triangle', 'Hexagon', 'Pentagon', 
    'Star', 'Diamond', 'KochSnowflake', 'Ring',
    'get_shape_renderer_function',
    'SHAPE_REGISTRY'
]