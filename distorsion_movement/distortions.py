"""
Fonctions de distorsion géométrique pour les carrés de la grille.
"""

import math
import random
from typing import Tuple, List

from distorsion_movement.enums import DistortionType


class DistortionEngine:
    """
    Moteur de distorsion pour appliquer différents types de déformations géométriques.
    """
    
    @staticmethod
    def generate_distortion_params() -> dict:
        """
        Génère des paramètres aléatoires pour les distorsions.
        
        Returns:
            Dict contenant les paramètres de distorsion pour un carré
        """
        return {
            'offset_x': random.uniform(-1, 1),
            'offset_y': random.uniform(-1, 1),
            'phase_x': random.uniform(0, 2 * math.pi),
            'phase_y': random.uniform(0, 2 * math.pi),
            'frequency': random.uniform(0.5, 2.0),
            'rotation_phase': random.uniform(0, 2 * math.pi)
        }
    
    @staticmethod
    def apply_distortion_random(base_pos: Tuple[float, float], 
                               params: dict,
                               cell_size: int,
                               distortion_strength: float) -> Tuple[float, float, float]:
        """
        Applique une distorsion aléatoire statique.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        max_offset = cell_size * distortion_strength
        dx = params['offset_x'] * max_offset
        dy = params['offset_y'] * max_offset
        rotation = params['rotation_phase'] * distortion_strength * 0.2
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    @staticmethod
    def apply_distortion_sine(base_pos: Tuple[float, float], 
                             params: dict,
                             cell_size: int,
                             distortion_strength: float,
                             time: float) -> Tuple[float, float, float]:
        """
        Applique une distorsion sinusoïdale animée.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        max_offset = cell_size * distortion_strength
        
        # Distorsion sinusoïdale avec phases différentes
        dx = math.sin(time * params['frequency'] + params['phase_x']) * max_offset
        dy = math.cos(time * params['frequency'] + params['phase_y']) * max_offset
        rotation = math.sin(time + params['rotation_phase']) * distortion_strength * 0.3
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    @staticmethod
    def apply_distortion_perlin(base_pos: Tuple[float, float], 
                               params: dict,
                               cell_size: int,
                               distortion_strength: float,
                               time: float) -> Tuple[float, float, float]:
        """
        Applique une distorsion basée sur du bruit de Perlin simplifié.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        # Simulation simple de bruit de Perlin avec des sinus multiples
        max_offset = cell_size * distortion_strength
        
        # Utilisation de la position pour créer un bruit cohérent spatialement
        noise_x = (math.sin(base_pos[0] * 0.01 + time) + 
                  math.sin(base_pos[0] * 0.03 + time * 0.5) * 0.5)
        noise_y = (math.cos(base_pos[1] * 0.01 + time) + 
                  math.cos(base_pos[1] * 0.03 + time * 0.5) * 0.5)
        
        dx = noise_x * max_offset * 0.5
        dy = noise_y * max_offset * 0.5
        rotation = noise_x * distortion_strength * 0.2
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    @staticmethod
    def apply_distortion_circular(base_pos: Tuple[float, float], 
                                 params: dict,
                                 cell_size: int,
                                 distortion_strength: float,
                                 time: float,
                                 canvas_size: Tuple[int, int]) -> Tuple[float, float, float]:
        """
        Applique une distorsion circulaire depuis le centre.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
            canvas_size: Taille du canvas (largeur, hauteur)
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        center_x = canvas_size[0] // 2
        center_y = canvas_size[1] // 2
        
        # Distance au centre
        dx_center = base_pos[0] - center_x
        dy_center = base_pos[1] - center_y
        distance = math.sqrt(dx_center**2 + dy_center**2)
        
        if distance == 0:
            return (base_pos[0], base_pos[1], 0)
        
        # Effet d'onde circulaire
        wave = math.sin(distance * 0.02 - time * 2) * distortion_strength
        max_offset = cell_size * wave
        
        # Direction radiale
        dx = (dx_center / distance) * max_offset
        dy = (dy_center / distance) * max_offset
        rotation = wave * 0.5
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    @staticmethod
    def apply_distortion_swirl(base_pos: Tuple[float, float], 
                              params: dict,
                              cell_size: int,
                              distortion_strength: float,
                              time: float,
                              canvas_size: Tuple[int, int]) -> Tuple[float, float, float]:
        """
        Applique une distorsion de tourbillon (swirl) avec des vagues périodiques.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
            canvas_size: Taille du canvas (largeur, hauteur)
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        center_x = canvas_size[0] // 2
        center_y = canvas_size[1] // 2
        
        # Distance au centre
        dx_center = base_pos[0] - center_x
        dy_center = base_pos[1] - center_y
        distance = math.sqrt(dx_center**2 + dy_center**2)
        
        # Gestion du point au centre pour éviter la singularité
        if distance == 0:
            return (base_pos[0], base_pos[1], 0)
        
        # Normalisation de la distance
        max_distance = math.sqrt(center_x**2 + center_y**2)
        normalized_distance = distance / max_distance
        
        # Création de vagues périodiques qui se propagent depuis le centre
        wave_speed = 3.0  # Vitesse de propagation des vagues
        wave_frequency = 0.02  # Fréquence des vagues (plus petit = vagues plus larges)
        wave_period = 4.0  # Période de génération des nouvelles vagues
        
        # Phase de la vague basée sur la distance et le temps
        wave_phase = distance * wave_frequency - time * wave_speed
        
        # Amplitude de la vague avec modulation périodique
        wave_amplitude = math.sin(time * wave_period) * math.sin(wave_phase)
        
        # Atténuation avec la distance pour un effet plus naturel
        distance_attenuation = math.exp(-normalized_distance * 2.0)
        wave_amplitude *= distance_attenuation
        
        # Angle de rotation du tourbillon
        # L'angle dépend de l'amplitude de la vague et de la position
        swirl_angle = wave_amplitude * distortion_strength * 3.0
        
        # Direction tangentielle (perpendiculaire au rayon)
        if distance > 0:
            # Vecteur unitaire radial
            radial_x = dx_center / distance
            radial_y = dy_center / distance
            
            # Vecteur tangentiel (rotation de 90 degrés du vecteur radial)
            tangent_x = -radial_y
            tangent_y = radial_x
            
            # Déplacement tangentiel basé sur l'amplitude de la vague
            max_offset = cell_size * distortion_strength
            displacement_magnitude = wave_amplitude * max_offset
            
            displacement_x = tangent_x * displacement_magnitude
            displacement_y = tangent_y * displacement_magnitude
        else:
            displacement_x = 0
            displacement_y = 0
        
        # Rotation de la forme elle-même
        shape_rotation = swirl_angle * 0.5
        
        return (
            base_pos[0] + displacement_x,
            base_pos[1] + displacement_y,
            shape_rotation
        )
    
    @staticmethod
    def get_distorted_positions(base_positions: List[Tuple[float, float]],
                               distortion_params: List[dict],
                               distortion_fn: str,
                               cell_size: int,
                               distortion_strength: float,
                               time: float,
                               canvas_size: Tuple[int, int]) -> List[Tuple[float, float, float]]:
        """
        Calcule toutes les positions déformées selon la fonction choisie.
        
        Args:
            base_positions: Liste des positions de base
            distortion_params: Liste des paramètres de distorsion
            distortion_fn: Type de fonction de distorsion
            cell_size: Taille des cellules
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
            canvas_size: Taille du canvas
        
        Returns:
            Liste de tuples (x, y, rotation) pour chaque carré
        """
        positions = []
        
        for i, (base_pos, params) in enumerate(zip(base_positions, distortion_params)):
            if distortion_fn == DistortionType.RANDOM.value:
                pos = DistortionEngine.apply_distortion_random(
                    base_pos, params, cell_size, distortion_strength
                )
            elif distortion_fn == DistortionType.SINE.value:
                pos = DistortionEngine.apply_distortion_sine(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.PERLIN.value:
                pos = DistortionEngine.apply_distortion_perlin(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.CIRCULAR.value:
                pos = DistortionEngine.apply_distortion_circular(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.SWIRL.value:
                pos = DistortionEngine.apply_distortion_swirl(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            else:
                pos = DistortionEngine.apply_distortion_random(
                    base_pos, params, cell_size, distortion_strength
                )
            
            positions.append(pos)
        
        return positions