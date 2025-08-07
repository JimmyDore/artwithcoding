"""
Générateur d'art génératif - Grille de carrés déformés géométriquement

Ce module implémente une grille régulière de carrés où chaque carré est légèrement 
déformé en position, forme ou orientation pour créer un effet visuel chaotique 
mais structuré.
"""

import pygame
import numpy as np
import math
import random
from typing import Tuple, List

from distorsion_movement.enums import DistortionType, ColorScheme
from distorsion_movement.audio_analyzer import AudioAnalyzer
from distorsion_movement.colors import ColorGenerator
from distorsion_movement.distortions import DistortionEngine


class DeformedGrid:
    """
    Générateur de grille de carrés déformés géométriquement.
    
    Cette classe crée une grille régulière où chaque carré peut être déformé
    par déplacement, modification de forme, ou rotation légère.
    """
    
    def __init__(self, 
                 dimension: int = 64,
                 cell_size: int = 8,
                 canvas_size: Tuple[int, int] = (1200, 900),
                 distortion_strength: float = 0.0,
                 distortion_fn: str = "random",
                 background_color: Tuple[int, int, int] = (20, 20, 30),
                 square_color: Tuple[int, int, int] = (255, 255, 255),
                 color_scheme: str = "monochrome",
                 color_animation: bool = False,
                 audio_reactive: bool = False,
                 mouse_interactive: bool = True,
                 mouse_mode: str = "attraction",
                 mouse_strength: float = 0.5,
                 mouse_radius: float = 100.0,
                 show_mouse_feedback: bool = True):
        """
        Initialise la grille déformée.
        
        Args:
            dimension: Nombre de cellules par ligne/colonne
            cell_size: Taille moyenne d'un carré en pixels
            canvas_size: Taille de la fenêtre (largeur, hauteur)
            distortion_strength: Intensité de la déformation (0.0 à 1.0)
            distortion_fn: Type de fonction de distorsion
            background_color: Couleur de fond RGB
            square_color: Couleur des carrés RGB (utilisée pour monochrome)
            color_scheme: Schéma de couleurs ("monochrome", "gradient", "rainbow", etc.)
            color_animation: Si True, les couleurs changent dans le temps
            audio_reactive: Si True, réagit à l'audio en temps réel
            mouse_interactive: Si True, active les interactions souris
            mouse_mode: Mode d'interaction souris ("attraction", "repulsion", etc.)
            mouse_strength: Force des interactions souris (0.0 à 1.0)
            mouse_radius: Rayon d'influence de la souris en pixels
            show_mouse_feedback: Si True, affiche le feedback visuel de la souris
        """
        self.dimension = dimension
        self.cell_size = cell_size
        self.canvas_size = canvas_size
        self.distortion_strength = distortion_strength
        self.distortion_fn = distortion_fn
        self.background_color = background_color
        self.square_color = square_color
        self.color_scheme = color_scheme
        self.color_animation = color_animation
        self.audio_reactive = audio_reactive
        self.mouse_interactive = mouse_interactive
        self.mouse_mode = mouse_mode
        self.mouse_strength = mouse_strength
        self.mouse_radius = mouse_radius
        self.show_mouse_feedback = show_mouse_feedback
        
        # Audio analyzer
        self.audio_analyzer = AudioAnalyzer() if audio_reactive else None
        self.base_distortion_strength = distortion_strength  # Sauvegarde de l'intensité de base
        
        # Mouse interaction engine
        if mouse_interactive:
            from distorsion_movement.mouse_interactions import MouseInteractionEngine
            from distorsion_movement.enums import MouseInteractionType, MouseMode
            
            # Convertir le mode string en enum
            try:
                interaction_type = MouseInteractionType(mouse_mode)
            except ValueError:
                interaction_type = MouseInteractionType.ATTRACTION
            
            self.mouse_engine = MouseInteractionEngine(
                interaction_type=interaction_type,
                mouse_mode=MouseMode.CONTINUOUS,
                strength=mouse_strength,
                radius=mouse_radius,
                show_feedback=show_mouse_feedback
            )
        else:
            self.mouse_engine = None
        
        # Calcul automatique du décalage pour centrer la grille
        grid_total_size = dimension * cell_size
        self.offset_x = (canvas_size[0] - grid_total_size) // 2
        self.offset_y = (canvas_size[1] - grid_total_size) // 2
        
        # Variables pour l'animation
        self.time = 0.0
        self.animation_speed = 0.02
        
        # Initialisation pygame
        pygame.init()
        # Get screen info for fullscreen
        info = pygame.display.Info()
        self.fullscreen_size = (info.current_w, info.current_h)
        
        # Start in windowed mode but store both modes
        self.windowed_size = canvas_size
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode(canvas_size)
        pygame.display.set_caption("Grille Déformée - Art Génératif")
        self.clock = pygame.time.Clock()
        
        # Génération des positions de base et des déformations
        self._generate_base_positions()
        self._generate_distortions()
        
        # Génération des couleurs de base pour chaque carré
        self._generate_base_colors()
        
        # Démarrage de l'analyse audio si activée
        if self.audio_reactive and self.audio_analyzer:
            self.audio_analyzer.start_audio_capture()
    
    def _generate_base_positions(self):
        """Génère les positions de base de la grille régulière"""
        self.base_positions = []
        for row in range(self.dimension):
            for col in range(self.dimension):
                x = col * self.cell_size + self.offset_x
                y = row * self.cell_size + self.offset_y
                self.base_positions.append((x, y))
    
    def _generate_distortions(self):
        """Génère les paramètres de distorsion pour chaque carré"""
        self.distortions = []
        for i in range(self.dimension * self.dimension):
            distortion_params = DistortionEngine.generate_distortion_params()
            self.distortions.append(distortion_params)
    
    def _generate_base_colors(self):
        """Génère les couleurs de base pour chaque carré selon le schéma choisi"""
        self.base_colors = []
        
        for i in range(self.dimension * self.dimension):
            row = i // self.dimension
            col = i % self.dimension
            
            # Normalisation des coordonnées (0.0 à 1.0)
            x_norm = col / (self.dimension - 1) if self.dimension > 1 else 0.5
            y_norm = row / (self.dimension - 1) if self.dimension > 1 else 0.5
            
            # Distance au centre normalisée
            center_x, center_y = 0.5, 0.5
            distance_to_center = math.sqrt((x_norm - center_x)**2 + (y_norm - center_y)**2)
            distance_to_center = min(distance_to_center / 0.707, 1.0)  # Normalise à [0,1]
            
            color = ColorGenerator.get_color_for_position(
                self.color_scheme, self.square_color, x_norm, y_norm, 
                distance_to_center, i, self.dimension
            )
            self.base_colors.append(color)
    
    def _get_distorted_positions(self) -> List[Tuple[float, float, float]]:
        """
        Calcule toutes les positions déformées selon la fonction choisie.
        
        Returns:
            Liste de tuples (x, y, rotation) pour chaque carré
        """
        # Calculer les positions de base avec la distorsion principale
        base_distorted = DistortionEngine.get_distorted_positions(
            self.base_positions,
            self.distortions,
            self.distortion_fn,
            self.cell_size,
            self.distortion_strength,
            self.time,
            self.canvas_size,
            self.mouse_engine
        )
        
        # Appliquer les forces de souris de manière additive si activées
        if (self.mouse_interactive and self.mouse_engine and 
            self.distortion_fn not in ["mouse_attraction", "mouse_repulsion"]):
            
            final_positions = []
            for i, (x, y, rotation) in enumerate(base_distorted):
                # Calculer la force de souris pour cette position
                mouse_force = self.mouse_engine.calculate_mouse_force((x, y))
                
                # Appliquer la force avec un facteur d'échelle
                force_multiplier = self.cell_size * self.mouse_strength * 5.0
                mouse_dx = mouse_force[0] * force_multiplier
                mouse_dy = mouse_force[1] * force_multiplier
                
                # Rotation additionnelle basée sur la force
                force_magnitude = math.sqrt(mouse_force[0]**2 + mouse_force[1]**2)
                mouse_rotation = force_magnitude * self.mouse_strength * 0.3
                
                # Combiner les déformations
                final_x = x + mouse_dx
                final_y = y + mouse_dy
                final_rotation = rotation + mouse_rotation
                
                final_positions.append((final_x, final_y, final_rotation))
            
            return final_positions
        
        return base_distorted
    
    def _draw_deformed_square(self, surface, x: float, y: float, 
                             rotation: float, size: int, color: Tuple[int, int, int]):
        """
        Dessine un carré déformé à la position donnée.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre du carré
            rotation: Rotation en radians
            size: Taille du carré
            color: Couleur RGB du carré
        """
        # Calcul des coins du carré
        half_size = size // 2
        corners = [
            (-half_size, -half_size),
            (half_size, -half_size),
            (half_size, half_size),
            (-half_size, half_size)
        ]
        
        # Application de la rotation
        rotated_corners = []
        cos_r = math.cos(rotation)
        sin_r = math.sin(rotation)
        
        for corner_x, corner_y in corners:
            new_x = corner_x * cos_r - corner_y * sin_r + x
            new_y = corner_x * sin_r + corner_y * cos_r + y
            
            # Validation des coordonnées (éviter NaN/Inf)
            if math.isfinite(new_x) and math.isfinite(new_y):
                rotated_corners.append((int(new_x), int(new_y)))
            else:
                # Fallback vers la position centrale si coordonnées invalides
                rotated_corners.append((int(x), int(y)))
        
        # Dessin du polygone (seulement si on a des coordonnées valides)
        if len(rotated_corners) >= 3:
            try:
                pygame.draw.polygon(surface, color, rotated_corners)
            except (TypeError, ValueError):
                # Fallback: dessiner un petit rectangle centré
                rect = pygame.Rect(int(x) - 2, int(y) - 2, 4, 4)
                pygame.draw.rect(surface, color, rect)
    
    def render(self):
        """Rend la grille déformée sur l'écran"""
        self.screen.fill(self.background_color)
        
        # Obtenir toutes les positions déformées
        positions = self._get_distorted_positions()
        
        # Dessiner chaque carré déformé avec sa couleur
        for i, (x, y, rotation) in enumerate(positions):
            # Obtenir la couleur de base et appliquer l'animation si nécessaire
            base_color = self.base_colors[i]
            final_color = ColorGenerator.get_animated_color(
                base_color, i, self.time, self.color_animation, 
                self.audio_reactive, self.audio_analyzer
            )
            
            self._draw_deformed_square(self.screen, x, y, rotation, self.cell_size, final_color)
        
        pygame.display.flip()
    
    def update(self):
        """Met à jour l'animation"""
        self.time += self.animation_speed
        
        # Mise à jour de l'intensité de distorsion basée sur l'audio
        if self.audio_reactive and self.audio_analyzer:
            audio_features = self.audio_analyzer.get_audio_features()
            
            # Les basses fréquences contrôlent l'intensité de distorsion
            bass_boost = min(audio_features['bass_level'] * 0.8, 1.0)  # Limiter à 1.0
            self.distortion_strength = min(self.base_distortion_strength + bass_boost, 2.0)  # Max 2.0
            
            # Le volume global contrôle la vitesse d'animation
            volume_speed = 1.0 + min(audio_features['overall_volume'] * 2.0, 3.0)  # Max 4x speed
            self.animation_speed = max(0.005, min(0.02 * volume_speed, 0.1))  # Entre 0.005 et 0.1
    
    def run_interactive(self):
        """Lance la boucle interactive principale"""
        running = True
        
        print("Contrôles:")
        print("- ESC: Quitter")
        print("- F: Basculer plein écran/fenêtré")
        print("- SPACE: Changer le type de distorsion")
        print("- C: Changer le schéma de couleurs")
        print("- A: Activer/désactiver l'animation des couleurs")
        print("- M: Activer/désactiver la réactivité audio")
        print("- +/-: Ajuster l'intensité de distorsion")
        print("- R: Régénérer les paramètres aléatoires")
        print("- S: Sauvegarder l'image")
        if self.mouse_interactive:
            print("\nContrôles souris:")
            print("- Mouvement souris: Interaction continue")
            print("- Clic gauche: Effet d'ondulation")
            print("- Clic droit: Effet d'explosion")
            print("- TAB: Basculer interactions souris")
            print("- 1-7: Changer mode d'interaction")
        
        distortion_types = [t.value for t in DistortionType]
        current_distortion_index = 0
        
        color_schemes = [c.value for c in ColorScheme]
        current_color_index = 0
        # Trouver l'index actuel du schéma de couleur
        try:
            current_color_index = color_schemes.index(self.color_scheme)
        except ValueError:
            current_color_index = 0
        
        while running:
            # Collecter les événements
            events = pygame.event.get()
            
            # Traiter les événements souris si activées
            if self.mouse_engine:
                self.mouse_engine.update_mouse_state(events)
            
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        # Changer le type de distorsion
                        current_distortion_index = (current_distortion_index + 1) % len(distortion_types)
                        self.distortion_fn = distortion_types[current_distortion_index]
                        print(f"Distorsion: {self.distortion_fn}")
                    elif event.key == pygame.K_c:
                        # Changer le schéma de couleurs
                        current_color_index = (current_color_index + 1) % len(color_schemes)
                        self.color_scheme = color_schemes[current_color_index]
                        self._generate_base_colors()  # Régénérer les couleurs
                        print(f"Schéma de couleurs: {self.color_scheme}")
                    elif event.key == pygame.K_a:
                        # Activer/désactiver l'animation des couleurs
                        self.color_animation = not self.color_animation
                        status = "activée" if self.color_animation else "désactivée"
                        print(f"Animation des couleurs: {status}")
                    elif event.key == pygame.K_m:
                        # Activer/désactiver la réactivité audio
                        from distorsion_movement.audio_analyzer import AUDIO_AVAILABLE
                        if not AUDIO_AVAILABLE:
                            print("Audio non disponible - installez pyaudio et scipy")
                        else:
                            self.audio_reactive = not self.audio_reactive
                            if self.audio_reactive:
                                if not self.audio_analyzer:
                                    self.audio_analyzer = AudioAnalyzer()
                                self.audio_analyzer.start_audio_capture()
                                print("🎵 Mode audio-réactif activé!")
                            else:
                                if self.audio_analyzer:
                                    self.audio_analyzer.stop_audio_capture()
                                print("🔇 Mode audio-réactif désactivé")
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        # Augmenter l'intensité
                        self.distortion_strength = min(1.0, self.distortion_strength + 0.1)
                        self.base_distortion_strength = self.distortion_strength
                        print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_MINUS:
                        # Diminuer l'intensité
                        self.distortion_strength = max(0.0, self.distortion_strength - 0.1)
                        self.base_distortion_strength = self.distortion_strength
                        print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_r:
                        # Régénérer les paramètres
                        self._generate_distortions()
                        self._generate_base_colors()
                        print("Paramètres régénérés")
                    elif event.key == pygame.K_s:
                        # Sauvegarder
                        self.save_image(f"deformed_grid_{self.distortion_fn}_{int(self.time*100)}.png")
                        print("Image sauvegardée")
                    elif event.key == pygame.K_f:
                        # Basculer plein écran
                        self.toggle_fullscreen()
                        mode = "plein écran" if self.is_fullscreen else "fenêtré"
                        print(f"Mode: {mode}")
                    elif event.key == pygame.K_TAB:
                        # Basculer les interactions souris
                        if self.mouse_engine:
                            from distorsion_movement.enums import MouseMode
                            if self.mouse_engine.mouse_mode == MouseMode.DISABLED:
                                self.mouse_engine.set_mouse_mode(MouseMode.CONTINUOUS)
                                print("🖱️ Interactions souris activées")
                            else:
                                self.mouse_engine.set_mouse_mode(MouseMode.DISABLED)
                                print("🚫 Interactions souris désactivées")
                    elif event.key >= pygame.K_1 and event.key <= pygame.K_7:
                        # Changer le mode d'interaction souris (1-7)
                        if self.mouse_engine:
                            from distorsion_movement.enums import MouseInteractionType
                            interaction_types = list(MouseInteractionType)
                            key_index = event.key - pygame.K_1
                            if key_index < len(interaction_types):
                                self.mouse_engine.set_interaction_type(interaction_types[key_index])
                                print(f"🖱️ Mode souris: {interaction_types[key_index].value}")
            
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        
        # Cleanup audio
        if self.audio_analyzer:
            self.audio_analyzer.stop_audio_capture()
        
        pygame.quit()
    
    def toggle_fullscreen(self):
        """Basculer entre mode fenêtré et plein écran"""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # Passer en plein écran
            self.screen = pygame.display.set_mode(self.fullscreen_size, pygame.FULLSCREEN)
            # Recalculer les offsets pour centrer la grille sur l'écran plein
            grid_total_size = self.dimension * self.cell_size
            self.offset_x = (self.fullscreen_size[0] - grid_total_size) // 2
            self.offset_y = (self.fullscreen_size[1] - grid_total_size) // 2
        else:
            # Retour au mode fenêtré
            self.screen = pygame.display.set_mode(self.windowed_size)
            # Restaurer les offsets originaux
            grid_total_size = self.dimension * self.cell_size
            self.offset_x = (self.windowed_size[0] - grid_total_size) // 2
            self.offset_y = (self.windowed_size[1] - grid_total_size) // 2
        
        # Recalculer les positions de base avec les nouveaux offsets
        self._generate_base_positions()
    
    def save_image(self, filename: str):
        """Sauvegarde l'image actuelle"""
        pygame.image.save(self.screen, filename)
        print(f"Image sauvegardée: {filename}")