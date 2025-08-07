"""
Énumérations pour les types de distorsion, schémas de couleurs et interactions souris.
"""

from enum import Enum


class DistortionType(Enum):
    """Types de distorsion disponibles"""
    RANDOM = "random"
    SINE = "sine" 
    PERLIN = "perlin"
    CIRCULAR = "circular"
    MOUSE_ATTRACTION = "mouse_attraction"
    MOUSE_REPULSION = "mouse_repulsion"


class ColorScheme(Enum):
    """Schémas de couleurs disponibles"""
    MONOCHROME = "monochrome"
    GRADIENT = "gradient"
    RAINBOW = "rainbow"
    COMPLEMENTARY = "complementary"
    TEMPERATURE = "temperature"
    PASTEL = "pastel"
    NEON = "neon"
    OCEAN = "ocean"
    FIRE = "fire"
    FOREST = "forest"


class MouseInteractionType(Enum):
    """Types d'interactions souris disponibles"""
    ATTRACTION = "attraction"
    REPULSION = "repulsion"
    RIPPLE = "ripple"
    BURST = "burst"
    TRAIL = "trail"
    DRAG = "drag"
    NONE = "none"


class MouseMode(Enum):
    """Modes de fonctionnement de la souris"""
    CONTINUOUS = "continuous"      # Effet continu pendant le mouvement
    CLICK_ONLY = "click_only"     # Effet seulement sur clic
    HOVER = "hover"               # Effet au survol
    DISABLED = "disabled"         # Interactions souris désactivées


class MouseButton(Enum):
    """Boutons de souris pour les interactions"""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    WHEEL_UP = "wheel_up"
    WHEEL_DOWN = "wheel_down"