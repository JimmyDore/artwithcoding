"""
Package de génération d'art génératif avec grilles déformées.

Ce package contient tous les modules nécessaires pour créer et afficher
des grilles de carrés déformés géométriquement avec différents effets visuels
et audio-réactifs.
"""

from distorsion_movement.deformed_grid import DeformedGrid
from distorsion_movement.enums import DistortionType, ColorScheme
from distorsion_movement.audio_analyzer import AudioAnalyzer
from distorsion_movement.colors import ColorGenerator
from distorsion_movement.distortions import DistortionEngine
from distorsion_movement.demos import create_deformed_grid, quick_demo, fullscreen_demo, audio_reactive_demo

__all__ = [
    'DeformedGrid',
    'DistortionType',
    'ColorScheme', 
    'AudioAnalyzer',
    'ColorGenerator',
    'DistortionEngine',
    'create_deformed_grid',
    'quick_demo',
    'fullscreen_demo',
    'audio_reactive_demo'
]