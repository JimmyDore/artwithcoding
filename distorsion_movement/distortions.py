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
    def apply_distortion_checkerboard_diagonal(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float
    ) -> Tuple[float, float, float]:
        """
        Checkerboard Warp (diagonal):
        Neighboring cells tug in opposite directions along a diagonal.
        Set params["diag_variant"] = "anti" to use the other diagonal (/ instead of \).
        """
        x, y = base_pos

        # Grid coords from position
        gx = int(x // cell_size)
        gy = int(y // cell_size)

        # Checkerboard polarity
        polarity = 1 if ((gx + gy) % 2 == 0) else -1

        # Choose which diagonal axis to use
        use_anti = (params.get("diag_variant") == "anti")
        if use_anti:
            # unit vector along '/' diagonal
            ux, uy = (1 / math.sqrt(2), -1 / math.sqrt(2))
        else:
            # unit vector along '\' diagonal
            ux, uy = (1 / math.sqrt(2),  1 / math.sqrt(2))

        # Optional per-cell stable phase so it's not robotically in-sync
        if "phase_offset" not in params:
            params["phase_offset"] = random.uniform(0, 2 * math.pi)
        phase = params["phase_offset"]

        # Motion settings
        move_speed = 0.6  # cycles per second (tweak to taste)
        max_offset = cell_size * 0.35 * distortion_strength

        s = math.sin(2 * math.pi * move_speed * time + phase)
        offset = s * max_offset * polarity

        new_x = x + ux * offset
        new_y = y + uy * offset

        # Small rotation to sell the tug
        rotation = s * polarity * distortion_strength * 0.12

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_tornado(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float,
        canvas_size: Tuple[int, int]
    ) -> Tuple[float, float, float]:
        """
        Tornado Column:
        Swirl effect where rotation speed increases toward the center axis,
        with a mild inward pull to simulate a funnel.
        """
        cx = canvas_size[0] * 0.5
        cy = canvas_size[1] * 0.5

        dx = base_pos[0] - cx
        dy = base_pos[1] - cy
        r = math.hypot(dx, dy)

        if r == 0:
            return (base_pos[0], base_pos[1], 0.0)

        # --- Parameters ---
        swirl_base_speed = 0.6   # base swirl cycles per second
        swirl_accel = 3.0        # how much faster near center
        inward_strength = 0.15   # pull toward center
        max_swirl_offset = cell_size * 0.45 * distortion_strength

        # Angular velocity increases as radius decreases
        normalized_r = r / (max(canvas_size) * 0.5)
        angular_speed = swirl_base_speed + swirl_accel * (1.0 - normalized_r)

        # Swirl angle over time
        angle = angular_speed * time * 2 * math.pi

        # Tangent vector (perpendicular to radius)
        tx = -dy / r
        ty = dx / r

        # Swirl displacement
        swirl_phase = math.sin(angle)
        swirl_disp = swirl_phase * max_swirl_offset * (1.0 - normalized_r * 0.7)

        # Inward pull displacement
        inward_disp = inward_strength * distortion_strength * (1.0 - normalized_r) * cell_size
        ix = -dx / r * inward_disp
        iy = -dy / r * inward_disp

        # Apply displacements
        new_x = base_pos[0] + tx * swirl_disp + ix
        new_y = base_pos[1] + ty * swirl_disp + iy

        # Rotation of the square itself (more intense near center)
        rotation = swirl_phase * distortion_strength * (0.3 + 0.4 * (1.0 - normalized_r))

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_spiral(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float,
        canvas_size: Tuple[int, int]
    ) -> Tuple[float, float, float]:
        """
        Spiral Warp:
        Smooth vortex-like rotation where points follow a spiral path
        with slow radius oscillations, like a galaxy formation.
        """
        cx = canvas_size[0] * 0.5
        cy = canvas_size[1] * 0.5

        dx = base_pos[0] - cx
        dy = base_pos[1] - cy
        r = math.hypot(dx, dy)
        if r == 0:
            return (base_pos[0], base_pos[1], 0.0)

        # --- Parameters ---
        angular_speed = 0.25  # rotations per second (slower = calmer)
        radius_osc_speed = 0.08  # cycles per second for in/out breathing
        radius_osc_amplitude = cell_size * 0.35 * distortion_strength  # how far radius changes

        # --- Angle-based spiral motion ---
        base_angle = math.atan2(dy, dx)
        angle_offset = angular_speed * time * 2 * math.pi

        # New angle
        new_angle = base_angle + angle_offset

        # --- Radius oscillation ---
        radius_offset = math.sin(time * radius_osc_speed * 2 * math.pi + r * 0.01) * radius_osc_amplitude
        new_r = r + radius_offset

        # Convert back to Cartesian
        new_x = cx + math.cos(new_angle) * new_r
        new_y = cy + math.sin(new_angle) * new_r

        # Rotation of the square itself → match rotation direction
        shape_rotation = angle_offset * 0.15  # subtle spin

        return (new_x, new_y, shape_rotation)

    @staticmethod
    def apply_distortion_shear(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float
    ) -> Tuple[float, float, float]:
        """
        Shear / Skew Distortion:
        Apply a horizontal or vertical shear based on position and time.
        Produces a diagonal wave-like skew.
        Set params["axis"] = "vertical" to skew along vertical instead of horizontal.
        """
        x, y = base_pos

        # Motion settings
        wave_speed = 0.5   # cycles per second
        wave_freq = 0.02   # spatial frequency (bigger = tighter waves)
        max_shear = cell_size * 0.5 * distortion_strength  # max offset

        # Optional per-cell stable phase for variety
        if "phase_offset" not in params:
            params["phase_offset"] = random.uniform(0, 2 * math.pi)
        phase = params["phase_offset"]

        # Horizontal shear (default)
        if params.get("axis", "horizontal") == "horizontal":
            shear_offset = math.sin(y * wave_freq + time * 2 * math.pi * wave_speed + phase) * max_shear
            new_x = x + shear_offset
            new_y = y
        else:  # Vertical shear
            shear_offset = math.sin(x * wave_freq + time * 2 * math.pi * wave_speed + phase) * max_shear
            new_x = x
            new_y = y + shear_offset

        # Small rotation to enhance skew illusion
        rotation = shear_offset / cell_size * 0.15

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_lens(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float,
        canvas_size: Tuple[int, int]
    ) -> Tuple[float, float, float]:
        """
        Lens / Magnify Effect:
        Moving focus point distorts nearby cells outward (magnification)
        and compresses farther cells slightly.
        """
        x, y = base_pos
        w, h = canvas_size

        # --- Focus point path (slow circular motion) ---
        focus_radius = min(w, h) * 0.25
        focus_speed = 0.1  # rotations per second
        focus_x = w / 2 + math.cos(time * 2 * math.pi * focus_speed) * focus_radius
        focus_y = h / 2 + math.sin(time * 2 * math.pi * focus_speed) * focus_radius

        # Allow manual override
        focus_x = params.get("focus_x", focus_x)
        focus_y = params.get("focus_y", focus_y)

        # --- Distance from focus point ---
        dx = x - focus_x
        dy = y - focus_y
        dist = math.hypot(dx, dy)

        # Radius of magnification zone
        lens_radius = min(w, h) * 0.25
        edge_softness = 0.2  # 0 = hard edge, 1 = very soft

        if dist < lens_radius:
            # Inside lens → magnify
            t = dist / lens_radius
            falloff = 1 - (t ** (1 + edge_softness * 2))  # smooth edge
            magnification = 1 + 0.5 * distortion_strength * falloff

            new_x = focus_x + dx * magnification
            new_y = focus_y + dy * magnification
        else:
            # Outside lens → slight compression toward edge
            compression = 1 - 0.1 * distortion_strength
            new_x = focus_x + dx * compression
            new_y = focus_y + dy * compression

        # Optional rotation for nearby cells (looks like glass refraction)
        rotation = 0
        if dist < lens_radius:
            rotation = (1 - dist / lens_radius) * distortion_strength * 0.2

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_spiral_wave(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float,
        canvas_size: Tuple[int, int]
    ) -> Tuple[float, float, float]:
        """
        Spiral Wave:
        Combination of circular ripple + swirl, so waves travel outward
        while rotating around the center.
        """
        cx = canvas_size[0] * 0.5
        cy = canvas_size[1] * 0.5

        dx = base_pos[0] - cx
        dy = base_pos[1] - cy
        r = math.hypot(dx, dy)
        if r == 0:
            return (base_pos[0], base_pos[1], 0.0)

        # Unit radial vector
        ux, uy = dx / r, dy / r

        # --- Ripple parameters ---
        ripple_speed = 4.0       # outward travel speed
        ripple_freq = 0.05       # controls spacing between ripples
        ripple_amp = cell_size * 0.4 * distortion_strength

        # --- Swirl parameters ---
        swirl_speed = 0.8        # rotations per second
        swirl_amp = cell_size * 0.25 * distortion_strength

        # Ripple wave (radial motion)
        ripple_phase = r * ripple_freq - time * ripple_speed
        ripple_offset = math.sin(ripple_phase) * ripple_amp * (1 - r / (max(canvas_size) * 0.5))

        # Swirl displacement (tangential motion)
        tx, ty = -uy, ux  # tangent vector
        swirl_angle = swirl_speed * time * 2 * math.pi
        swirl_offset = math.sin(swirl_angle + r * 0.01) * swirl_amp * (1 - r / (max(canvas_size) * 0.5))

        # Combine displacements
        new_x = base_pos[0] + ux * ripple_offset + tx * swirl_offset
        new_y = base_pos[1] + uy * ripple_offset + ty * swirl_offset

        # Rotation of the shape: blend ripple + swirl phases
        rotation = (ripple_offset / cell_size + swirl_offset / cell_size) * 0.15

        return (new_x, new_y, rotation)


    @staticmethod
    def apply_distortion_noise_rotation(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float
    ) -> Tuple[float, float, float]:
        """
        Noise-driven Rotation:
        Positions stay put; each cell's rotation is driven by a smooth noise field over time.
        Optionally add tiny positional shimmer via params["pos_jitter"]=True.
        """
        x, y = base_pos

        # Stable per-cell phase
        if "phase_offset" not in params:
            params["phase_offset"] = random.uniform(0, 2 * math.pi)
        phase = params["phase_offset"]

        # ---- Noise field (Perlin-ish via layered sin/cos) ----
        # Spatial scale controls how quickly the field changes across the grid
        spatial_scale = 0.2 #0.015
        time_scale = 2 # 0.5  # how fast the field evolves

        # 3 octaves for smooth but interesting motion
        def octave_noise(px, py, t, fmul, amp):
            fx = px * spatial_scale * fmul + t * time_scale * (0.9 + 0.2 * fmul)
            fy = py * spatial_scale * fmul + t * time_scale * (0.7 + 0.15 * fmul)
            # bounded in [-1, 1] and smooth
            return (math.sin(fx + phase) * math.cos(fy * 1.27 - phase)) * amp

        n = 0.0
        n += octave_noise(x, y, time, 1.0, 0.60)
        n += octave_noise(x, y, time, 2.0, 0.28)
        n += octave_noise(x, y, time, 4.0, 0.12)

        # ---- Rotation amplitude ----
        # More rotation: increase the maximum rotation range (up to ~60° at strength=1)
        max_rot_radians = (math.pi / 3.0) * (0.25 + 0.75 * distortion_strength)  # up to ~60°
        rotation = n * max_rot_radians

        # ---- Optional tiny positional shimmer (off by default) ----
        if params.get("pos_jitter", False):
            jitter_amp = cell_size * 0.05 * distortion_strength  # very small
            # Derive a "direction" from the noise for a coherent shimmer
            jx = math.sin(phase * 0.7 + time * 0.9) * jitter_amp * n
            jy = math.cos(phase * 0.9 - time * 0.7) * jitter_amp * n
            return (x + jx, y + jy, rotation)

        # Default: positions unchanged
        return (x, y, rotation)

    @staticmethod
    def apply_distortion_curl_warp(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float
    ) -> Tuple[float, float, float]:
        """
        Curl Warp:
        Proper curl-noise-like distortion producing smooth, divergence-free
        swirling vector fields that evolve over time.
        """
        x, y = base_pos

        # Per-cell stable offset so every cell follows a unique part of the field
        if "offset_x" not in params:
            params["offset_x"] = random.uniform(0, 1000)
            params["offset_y"] = random.uniform(0, 1000)
        ox = params["offset_x"]
        oy = params["offset_y"]

        # Noise parameters
        scale = 0.015   # spatial scale of the noise field
        tscale = 0.6    # temporal speed
        eps = 0.001     # small step for partial derivatives

        # Simple pseudo-Perlin noise function using layered sin/cos
        def pseudo_noise(px, py, t):
            return (
                math.sin(px) * math.cos(py * 1.3) +
                math.sin(px * 0.7 + t) * math.cos(py * 0.9 - t * 1.1)
            )

        # Sample noise at our point
        px = (x + ox) * scale
        py = (y + oy) * scale
        tt = time * tscale

        # Compute derivatives for curl
        n1 = pseudo_noise(px, py, tt)
        dn1_dy = (pseudo_noise(px, py + eps, tt) - pseudo_noise(px, py - eps, tt)) / (2 * eps)
        dn1_dx = (pseudo_noise(px + eps, py, tt) - pseudo_noise(px - eps, py, tt)) / (2 * eps)

        # Second noise with different phase to avoid symmetry
        n2 = pseudo_noise(px + 5.2, py - 3.7, tt + 2.5)
        dn2_dy = (pseudo_noise(px + 5.2, py - 3.7 + eps, tt + 2.5) - pseudo_noise(px + 5.2, py - 3.7 - eps, tt + 2.5)) / (2 * eps)
        dn2_dx = (pseudo_noise(px + 5.2 + eps, py - 3.7, tt + 2.5) - pseudo_noise(px + 5.2 - eps, py - 3.7, tt + 2.5)) / (2 * eps)

        # Curl = (∂n2/∂x - ∂n1/∂y, ∂n1/∂x - ∂n2/∂y)
        curl_x = dn2_dx - dn1_dy
        curl_y = dn1_dx - dn2_dy

        # Normalize & scale displacement
        mag = math.sqrt(curl_x**2 + curl_y**2)
        if mag > 0:
            curl_x /= mag
            curl_y /= mag

        max_offset = cell_size * 0.45 * distortion_strength
        disp_x = curl_x * max_offset
        disp_y = curl_y * max_offset

        # Apply displacement
        new_x = x + disp_x
        new_y = y + disp_y

        # Rotation: proportional to curl magnitude
        rotation = mag * distortion_strength * 0.4

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_fractal_noise(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float
    ) -> Tuple[float, float, float]:
        """
        Fractal Noise Warp:
        Multi-octave noise-based displacement for organic, terrain-like distortions.
        Similar to PERLIN but richer, with large + small-scale variations.
        """
        x, y = base_pos

        # Stable per-cell offset for noise sampling
        if "offset_x" not in params:
            params["offset_x"] = random.uniform(0, 1000)
            params["offset_y"] = random.uniform(0, 1000)
        ox = params["offset_x"]
        oy = params["offset_y"]

        # Noise parameters
        base_scale = 0.012       # spatial scale for largest octave
        base_speed = 0.4         # base temporal speed
        octaves = 4              # number of layers
        persistence = 0.5        # amplitude falloff per octave

        # Simple pseudo noise generator
        def pseudo_noise(px, py, t):
            return math.sin(px) * math.cos(py * 1.3) + math.sin(px * 0.7 + t) * math.cos(py * 0.9 - t * 1.1)

        disp_x, disp_y = 0.0, 0.0
        amplitude = 1.0
        freq_mul = 1.0
        max_amp_sum = 0.0

        for _ in range(octaves):
            # Sample coordinates for this octave
            px = (x + ox) * base_scale * freq_mul
            py = (y + oy) * base_scale * freq_mul
            t = time * base_speed * freq_mul

            n_x = pseudo_noise(px, py, t)
            n_y = pseudo_noise(py + 5.2, px - 3.7, t + 1.5)  # second noise for Y axis

            disp_x += n_x * amplitude
            disp_y += n_y * amplitude

            max_amp_sum += amplitude
            amplitude *= persistence
            freq_mul *= 2.0  # double frequency each octave

        # Normalize total displacement
        disp_x /= max_amp_sum
        disp_y /= max_amp_sum

        # Scale by strength & cell size
        max_offset = cell_size * 0.45 * distortion_strength
        new_x = x + disp_x * max_offset
        new_y = y + disp_y * max_offset

        # Rotation based on fine noise detail
        rotation = (disp_x + disp_y) * 0.15 * distortion_strength

        return (new_x, new_y, rotation)

    @staticmethod
    def apply_distortion_moire(
        base_pos: Tuple[float, float],
        params: dict,
        cell_size: int,
        distortion_strength: float,
        time: float,
        canvas_size: Tuple[int, int]
    ) -> Tuple[float, float, float]:
        """
        Moiré Warp (strong/obvious):
        Sum of two almost-identical plane waves with a tiny angle/frequency detune.
        The slow envelope (beat) modulates amplitude -> big drifting bands.
        """
        x, y = base_pos
        cx, cy = canvas_size[0] * 0.5, canvas_size[1] * 0.5
        dx, dy = x - cx, y - cy

        # ---- Controls (these make or break the moiré look) ----
        wavelength_px = params.get("wavelength_px", 90.0)   # base wavelength in pixels
        detune_freq   = params.get("detune_freq", 0.06)     # 0.03–0.10: small diff in wavelength
        base_angle_deg= params.get("base_angle_deg", 25.0)  # direction of wave 1
        detune_angle  = params.get("detune_angle_deg", 8.0) # 4–12°: tiny angle difference
        phase_speed   = params.get("phase_speed", 0.15)     # cycles/sec (slow drift)
        max_factor    = params.get("max_factor", 0.6)      # displacement scale

        # Per-cell stable phase
        if "phase_offset" not in params:
            params["phase_offset"] = random.uniform(0, 2*math.pi)
        phase0 = params["phase_offset"]

        # Wave numbers
        k1 = 2*math.pi / wavelength_px
        k2 = 2*math.pi / (wavelength_px * (1.0 + detune_freq))

        # Directions (unit vectors)
        a1 = math.radians(base_angle_deg)
        a2 = math.radians(base_angle_deg + detune_angle)
        u1 = (math.cos(a1), math.sin(a1))
        u2 = (math.cos(a2), math.sin(a2))

        # Projections
        p1 = dx * u1[0] + dy * u1[1]
        p2 = dx * u2[0] + dy * u2[1]

        # Time phases
        tphase = 2*math.pi*phase_speed*time

        # Two nearly-identical waves
        s1 = math.sin(k1 * p1 + tphase + 0.7*phase0)
        s2 = math.sin(k2 * p2 - tphase + 1.1*phase0)

        # Strong interference bands via *envelope* of the difference vector
        # Envelope wavevector ≈ (k1*u1 - k2*u2) -> low frequency (big bands)
        env_vec_x = k1*u1[0] - k2*u2[0]
        env_vec_y = k1*u1[1] - k2*u2[1]
        env_norm  = math.hypot(env_vec_x, env_vec_y)
        if env_norm < 1e-6:
            env_norm = 1e-6
        env_ux, env_uy = env_vec_x/env_norm, env_vec_y/env_norm
        env_proj = dx*env_ux + dy*env_uy
        envelope = 0.5 + 0.5 * math.sin(env_norm * env_proj + 0.6*tphase + phase0)
        # envelope in [0,1] -> multiplies amplitude to reveal big drifting bands

        # Displacement = vector sum of the two waves, modulated by envelope
        disp_x = (s1 * u1[0] + s2 * u2[0]) * envelope
        disp_y = (s1 * u1[1] + s2 * u2[1]) * envelope

        # Normalize & scale so it stays nice at strength=1
        mag = math.hypot(disp_x, disp_y)
        if mag > 1e-6:
            disp_x /= mag
            disp_y /= mag

        max_offset = cell_size * max_factor * distortion_strength
        new_x = x + disp_x * max_offset
        new_y = y + disp_y * max_offset

        # Subtle rotation tied to envelope (bands look like they “shimmer”)
        rotation = envelope * 0.12 * distortion_strength * (s1 - s2)

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
            elif distortion_fn == DistortionType.CHECKERBOARD_DIAGONAL.value:
                pos = DistortionEngine.apply_distortion_checkerboard_diagonal(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.TORNADO.value:
                pos = DistortionEngine.apply_distortion_tornado(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.SPIRAL.value:
                pos = DistortionEngine.apply_distortion_spiral(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.SHEAR.value:
                pos = DistortionEngine.apply_distortion_shear(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.LENS.value:
                pos = DistortionEngine.apply_distortion_lens(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.SPIRAL_WAVE.value:
                pos = DistortionEngine.apply_distortion_spiral_wave(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            elif distortion_fn == DistortionType.NOISE_ROTATION.value:
                pos = DistortionEngine.apply_distortion_noise_rotation(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.CURL_WARP.value:
                pos = DistortionEngine.apply_distortion_curl_warp(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.FRACTAL_NOISE.value:
                pos = DistortionEngine.apply_distortion_fractal_noise(
                    base_pos, params, cell_size, distortion_strength, time
                )
            elif distortion_fn == DistortionType.MOIRE.value:
                pos = DistortionEngine.apply_distortion_moire(
                    base_pos, params, cell_size, distortion_strength, time, canvas_size
                )
            else:
                pos = DistortionEngine.apply_distortion_random(
                    base_pos, params, cell_size, distortion_strength
                )

            
            positions.append(pos)
        
        return positions