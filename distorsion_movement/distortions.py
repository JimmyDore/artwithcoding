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
    def apply_distortion_ripple(base_pos: Tuple[float, float], 
                               params: dict,
                               cell_size: int,
                               distortion_strength: float,
                               time: float,
                               canvas_size: Tuple[int, int]) -> Tuple[float, float, float]:
        """
        Applique une distorsion d'ondulation (ripple) avec des vagues concentriques.
        Les déplacements sont appliqués dans la direction tangentielle pour créer
        un effet d'ondulation perpendiculaire au rayon.
        
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
        
        # Paramètres des ondulations concentriques
        wave_speed = 2.5  # Vitesse de propagation des ondulations
        wave_frequency = 0.03  # Fréquence des ondulations (espacement entre les vagues)
        wave_amplitude_scale = 0.8  # Échelle de l'amplitude
        
        # Phase de l'ondulation basée sur la distance et le temps
        ripple_phase = distance * wave_frequency - time * wave_speed
        
        # Amplitude de l'ondulation avec atténuation progressive
        max_distance = math.sqrt(center_x**2 + center_y**2)
        normalized_distance = distance / max_distance
        distance_attenuation = math.exp(-normalized_distance * 1.5)
        
        ripple_amplitude = math.sin(ripple_phase) * wave_amplitude_scale * distance_attenuation
        
        # Direction tangentielle (perpendiculaire au rayon)
        if distance > 0:
            # Vecteur unitaire radial
            radial_x = dx_center / distance
            radial_y = dy_center / distance
            
            # Vecteur tangentiel (rotation de 90 degrés du vecteur radial)
            tangent_x = -radial_y
            tangent_y = radial_x
            
            # Déplacement tangentiel basé sur l'amplitude de l'ondulation
            max_offset = cell_size * distortion_strength
            displacement_magnitude = ripple_amplitude * max_offset
            
            displacement_x = tangent_x * displacement_magnitude
            displacement_y = tangent_y * displacement_magnitude
        else:
            displacement_x = 0
            displacement_y = 0
        
        # Rotation légère basée sur l'amplitude de l'ondulation
        shape_rotation = ripple_amplitude * distortion_strength * 0.3
        
        return (
            base_pos[0] + displacement_x,
            base_pos[1] + displacement_y,
            shape_rotation
        )
    
    @staticmethod
    def apply_distortion_flow(base_pos: Tuple[float, float], 
                             params: dict,
                             cell_size: int,
                             distortion_strength: float,
                             time: float) -> Tuple[float, float, float]:
        """
        Applique une distorsion de flux (flow) avec un champ vectoriel pseudo curl-noise.
        Utilise des combinaisons de sin/cos pour créer un champ de vecteurs cohérent et lisse
        qui évolue dans le temps.
        
        Args:
            base_pos: Position de base (x, y)
            params: Paramètres de distorsion
            cell_size: Taille de la cellule
            distortion_strength: Intensité de distorsion
            time: Temps actuel pour l'animation
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        x, y = base_pos
        
        # Paramètres du champ de flux
        flow_scale = 0.01  # Échelle spatiale du champ de flux
        time_scale = 0.5   # Vitesse d'évolution temporelle
        noise_layers = 3   # Nombre de couches de bruit pour plus de complexité
        
        # Variables pour accumuler les composantes du champ vectoriel
        flow_x = 0.0
        flow_y = 0.0
        
        # Génération du champ vectoriel avec multiple octaves
        for octave in range(noise_layers):
            # Fréquence et amplitude pour cette octave
            freq = flow_scale * (2 ** octave)
            amplitude = 1.0 / (2 ** octave)
            
            # Coordonnées modulées par la fréquence et le temps
            fx = x * freq + time * time_scale * (octave + 1)
            fy = y * freq + time * time_scale * (octave + 1) * 0.7
            
            # Génération pseudo curl-noise utilisant des dérivées de fonctions périodiques
            # Pour créer un champ de flux cohérent, nous utilisons le rotationnel d'un champ scalaire
            
            # Potentiel scalaire A
            potential_a = math.sin(fx) * math.cos(fy * 1.3) + math.sin(fx * 0.7) * math.cos(fy)
            
            # Potentiel scalaire B (légèrement décalé pour diversité)
            potential_b = math.cos(fx * 1.1) * math.sin(fy * 0.9) + math.cos(fx) * math.sin(fy * 1.2)
            
            # Calcul approximatif du rotationnel pour obtenir un champ vectoriel divergence-free
            # curl = (∂B/∂x - ∂A/∂y, ∂A/∂x - ∂B/∂y)
            
            # Dérivées partielles approximées
            delta = 0.01
            
            # ∂A/∂x
            da_dx = (math.sin(fx + delta) * math.cos(fy * 1.3) + math.sin((fx + delta) * 0.7) * math.cos(fy) - potential_a) / delta
            
            # ∂A/∂y  
            da_dy = (math.sin(fx) * math.cos((fy + delta) * 1.3) + math.sin(fx * 0.7) * math.cos(fy + delta) - potential_a) / delta
            
            # ∂B/∂x
            db_dx = (math.cos((fx + delta) * 1.1) * math.sin(fy * 0.9) + math.cos(fx + delta) * math.sin(fy * 1.2) - potential_b) / delta
            
            # ∂B/∂y
            db_dy = (math.cos(fx * 1.1) * math.sin((fy + delta) * 0.9) + math.cos(fx) * math.sin((fy + delta) * 1.2) - potential_b) / delta
            
            # Champ vectoriel curl
            curl_x = db_dx - da_dy
            curl_y = da_dx - db_dy
            
            # Accumulation pondérée
            flow_x += curl_x * amplitude
            flow_y += curl_y * amplitude
        
        # Calcul de la magnitude du flux pour normalisation
        flow_magnitude = math.sqrt(flow_x**2 + flow_y**2)
        
        # Application du déplacement avec normalisation pour respecter les bornes
        max_offset = cell_size * distortion_strength
        
        if flow_magnitude > 0:
            # Normaliser le vecteur de flux pour qu'il reste dans les bornes
            # Utiliser tanh pour une transition douce et garantir |flow| <= 1
            normalized_magnitude = math.tanh(flow_magnitude)
            flow_x_normalized = (flow_x / flow_magnitude) * normalized_magnitude
            flow_y_normalized = (flow_y / flow_magnitude) * normalized_magnitude
            
            displacement_x = flow_x_normalized * max_offset
            displacement_y = flow_y_normalized * max_offset
        else:
            displacement_x = 0
            displacement_y = 0
        
        # Rotation basée sur la magnitude du flux original (avant normalisation)
        shape_rotation = math.tanh(flow_magnitude) * distortion_strength * 0.4
        
        return (
            base_pos[0] + displacement_x,
            base_pos[1] + displacement_y,
            shape_rotation
        )
    
    @staticmethod
    def apply_distortion_pulse(base_pos: Tuple[float, float], 
                                params: dict,
                                cell_size: int,
                                distortion_strength: float,
                                time: float,
                                canvas_size: Tuple[int, int]) -> Tuple[float, float, float]:
        """
        Pulsation avec effet ondulatoire radial + variation par cellule.
        Cela donne un effet de respiration organique plutôt qu'un simple zoom.
        """
        center_x = canvas_size[0] // 2
        center_y = canvas_size[1] // 2

        dx_center = base_pos[0] - center_x
        dy_center = base_pos[1] - center_y
        distance = math.sqrt(dx_center**2 + dy_center**2)

        if distance == 0:
            return (base_pos[0], base_pos[1], 0)

        # Paramètres de base
        base_frequency = 1.2  # pulsations par seconde
        base_amplitude = 0.4  # amplitude max
        ripple_frequency = 0.04  # fréquence de l'ondulation sur la distance

        # Décalage unique pour chaque cellule (random mais stable)
        cell_phase_offset = params.get("phase_offset", random.uniform(0, 2 * math.pi))

        # Facteur de pulsation basé sur distance + onde
        pulse_wave = math.sin(time * base_frequency * 2 * math.pi 
                            + distance * ripple_frequency 
                            + cell_phase_offset)

        # On normalise et applique l'amplitude (avec facteur de réduction pour intensité plus subtile)
        pulse_factor = 1.0 + (pulse_wave * base_amplitude * distortion_strength * 0.05)

        # Application du scaling radial
        new_x = center_x + dx_center * pulse_factor
        new_y = center_y + dy_center * pulse_factor

        # Rotation subtile en fonction de la phase (réduite pour plus de subtilité)
        rotation = pulse_wave * distortion_strength * 0.1

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_checkerboard(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float
    ) -> Tuple[float, float, float]:
        """
        Checkerboard Warp:
        Alternate distortion directions based on grid coordinates.
        Even cells move in one direction, odd cells in the opposite.
        Creates a tug-of-war effect across the grid.
        """
        x, y = base_pos

        # Get grid coordinates
        grid_x = int(x // cell_size)
        grid_y = int(y // cell_size)

        # Determine "polarity" of the cell (checkerboard pattern)
        direction = 1 if (grid_x + grid_y) % 2 == 0 else -1

        # Movement parameters
        move_speed = 0.8   # cycles per second
        max_offset = cell_size * 0.4 * distortion_strength

        # Oscillation over time
        offset = math.sin(time * move_speed * 2 * math.pi) * max_offset * direction

        # Apply offset horizontally (you could also make vertical or diagonal variants)
        new_x = x + offset
        new_y = y

        # Optional: small rotation for a more dynamic feel
        rotation = direction * math.sin(time * move_speed * 2 * math.pi) * distortion_strength * 0.15

        return (new_x, new_y, rotation)

    
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
            elif distortion_fn == DistortionType.RIPPLE.value:
                pos = DistortionEngine.apply_distortion_ripple(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.FLOW.value:
                pos = DistortionEngine.apply_distortion_flow(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.PULSE.value:
                pos = DistortionEngine.apply_distortion_pulse(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.CHECKERBOARD.value:
                pos = DistortionEngine.apply_distortion_checkerboard(
                    base_pos, params, cell_size, distortion_strength, time
                )
            else:
                pos = DistortionEngine.apply_distortion_random(
                    base_pos, params, cell_size, distortion_strength
                )

            
            positions.append(pos)
        
        return positions