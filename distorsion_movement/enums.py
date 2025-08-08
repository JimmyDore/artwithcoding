"""
Énumérations pour les types de distorsion, schémas de couleurs et formes.
"""

from enum import Enum


class DistortionType(Enum):
    """Types de distorsion disponibles"""
    RANDOM = "random"
    SINE = "sine" 
    PERLIN = "perlin"
    CIRCULAR = "circular"
    SWIRL = "swirl"
    RIPPLE = "ripple"
    FLOW = "flow"
    PULSE = "pulse"


class ColorScheme(Enum):
    """Schémas de couleurs disponibles"""
    MONOCHROME = "monochrome"
    BLACK_WHITE_RADIAL = "black_white_radial"
    BLACK_WHITE_ALTERNATING = "black_white_alternating"
    GRADIENT = "gradient"
    RAINBOW = "rainbow"
    COMPLEMENTARY = "complementary"
    # TEMPERATURE = "temperature"
    PASTEL = "pastel"
    NEON = "neon"
    # OCEAN = "ocean"
    # FIRE = "fire"
    # FOREST = "forest"


class ShapeType(Enum):
    """Types de formes disponibles"""
    SQUARE = "square"
    CIRCLE = "circle"
    TRIANGLE = "triangle"
    HEXAGON = "hexagon"
    STAR = "star"
    PENTAGON = "pentagon"
    DIAMOND = "diamond"