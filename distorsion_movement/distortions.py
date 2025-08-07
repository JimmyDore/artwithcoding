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
    def apply_distortion_mouse_attraction(base_pos: Tuple[float, float],
                                        params: dict,
                                        cell_size: int,
                                        distortion_strength: float,
                                        time: float,
                                        mouse_engine) -> Tuple[float, float, float]:
        """
        Applique une distorsion d'attraction basée sur la souris.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
            mouse_engine: Instance du moteur d'interaction souris
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        if mouse_engine is None:
            return (base_pos[0], base_pos[1], 0)
        
        # Obtenir la force de la souris
        mouse_force = mouse_engine.calculate_mouse_force(base_pos)
        
        # Appliquer la force avec l'intensité de distorsion
        force_multiplier = cell_size * distortion_strength * 10.0  # Facteur d'échelle
        dx = mouse_force[0] * force_multiplier
        dy = mouse_force[1] * force_multiplier
        
        # Rotation basée sur l'intensité de la force
        force_magnitude = math.sqrt(mouse_force[0]**2 + mouse_force[1]**2)
        rotation = force_magnitude * distortion_strength * 0.5
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    @staticmethod
    def apply_distortion_mouse_repulsion(base_pos: Tuple[float, float],
                                       params: dict,
                                       cell_size: int,
                                       distortion_strength: float,
                                       time: float,
                                       mouse_engine) -> Tuple[float, float, float]:
        """
        Applique une distorsion de répulsion basée sur la souris.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
            mouse_engine: Instance du moteur d'interaction souris
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        if mouse_engine is None:
            return (base_pos[0], base_pos[1], 0)
        
        # Changer temporairement le type d'interaction pour la répulsion
        original_type = mouse_engine.interaction_type
        from distorsion_movement.enums import MouseInteractionType
        mouse_engine.interaction_type = MouseInteractionType.REPULSION
        
        # Obtenir la force de répulsion
        mouse_force = mouse_engine.calculate_mouse_force(base_pos)
        
        # Restaurer le type original
        mouse_engine.interaction_type = original_type
        
        # Appliquer la force avec l'intensité de distorsion
        force_multiplier = cell_size * distortion_strength * 10.0  # Facteur d'échelle
        dx = mouse_force[0] * force_multiplier
        dy = mouse_force[1] * force_multiplier
        
        # Rotation basée sur l'intensité de la force
        force_magnitude = math.sqrt(mouse_force[0]**2 + mouse_force[1]**2)
        rotation = force_magnitude * distortion_strength * 0.5
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    @staticmethod
    def apply_mouse_distortion(base_pos: Tuple[float, float],
                             params: dict,
                             cell_size: int,
                             distortion_strength: float,
                             time: float,
                             mouse_engine,
                             interaction_type: str = "attraction") -> Tuple[float, float, float]:
        """
        Dispatcher générique pour les distorsions de souris.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
            mouse_engine: Instance du moteur d'interaction souris
            interaction_type: Type d'interaction ("attraction" ou "repulsion")
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        if interaction_type == "repulsion":
            return DistortionEngine.apply_distortion_mouse_repulsion(
                base_pos, params, cell_size, distortion_strength, time, mouse_engine
            )
        else:
            return DistortionEngine.apply_distortion_mouse_attraction(
                base_pos, params, cell_size, distortion_strength, time, mouse_engine
            )
    
    @staticmethod
    def get_distorted_positions(base_positions: List[Tuple[float, float]],
                               distortion_params: List[dict],
                               distortion_fn: str,
                               cell_size: int,
                               distortion_strength: float,
                               time: float,
                               canvas_size: Tuple[int, int],
                               mouse_engine=None) -> List[Tuple[float, float, float]]:
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
            mouse_engine: Instance du moteur d'interaction souris (optionnel)
        
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
            elif distortion_fn == DistortionType.MOUSE_ATTRACTION.value:
                pos = DistortionEngine.apply_distortion_mouse_attraction(
                    base_pos, params, cell_size, distortion_strength, time, mouse_engine
                )
            elif distortion_fn == DistortionType.MOUSE_REPULSION.value:
                pos = DistortionEngine.apply_distortion_mouse_repulsion(
                    base_pos, params, cell_size, distortion_strength, time, mouse_engine
                )
            else:
                pos = DistortionEngine.apply_distortion_random(
                    base_pos, params, cell_size, distortion_strength
                )
            
            positions.append(pos)
        
        return positions