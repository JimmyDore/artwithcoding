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
import datetime
import threading
from typing import Tuple, List

from distorsion_movement.enums import DistortionType, ColorScheme, ShapeType
from distorsion_movement.colors import ColorGenerator
from distorsion_movement.distortions import DistortionEngine
from distorsion_movement.shapes import get_shape_renderer_function

import os 
import imageio
import yaml
import glob


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
                 shape_type: str = "square",
                 mixed_shapes: bool = False):
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
            shape_type: Type de forme à dessiner ("square", "circle", "triangle", etc.)
            mixed_shapes: Si True, utilise différentes formes dans la grille
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
        self.shape_type = shape_type
        self.mixed_shapes = mixed_shapes
        
        self.base_distortion_strength = distortion_strength  # Sauvegarde de l'intensité de base
        
        # Calcul automatique du décalage pour centrer la grille
        grid_total_size = dimension * cell_size
        self.offset_x = (canvas_size[0] - grid_total_size) // 2
        self.offset_y = (canvas_size[1] - grid_total_size) // 2
        
        # Variables pour l'animation
        self.time = 0.0
        self.animation_speed = 0.02
        
        # Variables pour le menu d'aide
        self.show_help = False
        self.help_font = None
        
        # Variables pour l'affichage du statut
        self.show_status = True
        self.status_font = None
        
        # Variables pour l'enregistrement GIF
        self.is_recording = False
        self.recorded_frames = []
        self.max_frames = 900  # Max 15 secondes à 60 FPS
        self.frame_skip = 1  # Capturer chaque frame par défaut
        self.recording_start_time = None
        
        # Variables pour le contrôle dynamique de la densité de grille
        self.base_dimension = dimension  # Sauvegarder la dimension originale
        self.grid_density_mode = False  # Mode d'ajustement de la densité de grille
        
        # Variables pour l'itération à travers les scènes sauvegardées
        self.saved_scenes = []
        self.current_scene_index = -1
        self.scene_iteration_mode = False
        
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
        
        # Initialiser les polices pour le menu d'aide et l'affichage du statut
        try:
            pygame.font.init()  # Ensure font system is initialized
            self.help_font = pygame.font.Font(None, 24)
            self.help_title_font = pygame.font.Font(None, 32)
            self.status_font = pygame.font.Font(None, 20)
        except pygame.error:
            # Fallback for headless environments (tests)
            self.help_font = None
            self.help_title_font = None
            self.status_font = None
        
        # Génération des positions de base et des déformations
        self._generate_base_positions()
        self._generate_distortions()
        
        # Génération des couleurs de base pour chaque carré
        self._generate_base_colors()
        
        # Génération des types de formes pour chaque cellule
        self._generate_shape_types()
            
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
    
    def _generate_shape_types(self):
        """Génère les types de formes pour chaque cellule selon le mode choisi"""
        self.shape_types = []
        
        if self.mixed_shapes:
            # Mode formes mixtes: assignation aléatoire de différentes formes
            available_shapes = [shape.value for shape in ShapeType]
            for i in range(self.dimension * self.dimension):
                shape_type = random.choice(available_shapes)
                self.shape_types.append(shape_type)
        else:
            # Mode forme unique: toutes les cellules ont la même forme
            for i in range(self.dimension * self.dimension):
                self.shape_types.append(self.shape_type)
    
    def _update_grid_density(self, increase: bool):
        """
        Met à jour la densité de la grille en changeant le nombre de cellules.
        Maintient approximativement la même taille totale de grille.
        
        Args:
            increase: Si True, augmente la densité (plus de cellules), sinon diminue
        """
        current_size = self.fullscreen_size if self.is_fullscreen else self.windowed_size
        
        # Calculer la taille de grille cible (80% de la plus petite dimension d'écran)
        target_grid_size = min(current_size[0], current_size[1]) * 0.8
        
        # Calculer la nouvelle dimension basée sur la direction
        if increase:
            new_dimension = min(self.dimension + 8, 256)  # Augmenter par incréments de 8, max 256
        else:
            new_dimension = max(self.dimension - 8, 8)   # Diminuer par incréments de 8, min 8
        
        if new_dimension == self.dimension:
            return  # Pas de changement possible
        
        # Calculer la nouvelle taille de cellule pour maintenir la taille de grille
        new_cell_size = max(2, int(target_grid_size / new_dimension))
        
        # Mettre à jour les paramètres
        old_dimension = self.dimension
        self.dimension = new_dimension
        self.cell_size = new_cell_size
        
        # Recalculer les offsets pour centrer la grille
        grid_total_size = self.dimension * self.cell_size
        self.offset_x = (current_size[0] - grid_total_size) // 2
        self.offset_y = (current_size[1] - grid_total_size) // 2
        
        # Régénérer tous les éléments de la grille pour la nouvelle dimension
        self._generate_base_positions()
        self._generate_distortions()
        self._generate_base_colors()
        self._generate_shape_types()
        
        direction = "augmentée" if increase else "diminuée"
        print(f"Densité de grille {direction}: {old_dimension}x{old_dimension} → {self.dimension}x{self.dimension}")
        print(f"Taille des cellules: {self.cell_size}px (grille: {grid_total_size}x{grid_total_size}px)")
    
    def _get_distorted_positions(self) -> List[Tuple[float, float, float]]:
        """
        Calcule toutes les positions déformées selon la fonction choisie.
        
        Returns:
            Liste de tuples (x, y, rotation) pour chaque carré
        """
        return DistortionEngine.get_distorted_positions(
            self.base_positions,
            self.distortions,
            self.distortion_fn,
            self.cell_size,
            self.distortion_strength,
            self.time,
            self.canvas_size
        )
    
    def _draw_shape(self, surface, x: float, y: float, rotation: float, 
                   size: int, color: Tuple[int, int, int], shape_type: str):
        """
        Dessine une forme à la position donnée.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre de la forme
            rotation: Rotation en radians
            size: Taille de la forme
            color: Couleur RGB de la forme
            shape_type: Type de forme à dessiner
        """
        # Obtenir la fonction de rendu pour ce type de forme
        shape_function = get_shape_renderer_function(shape_type)
        
        # Dessiner la forme
        shape_function(surface, x, y, rotation, size, color)
    
    def _render_help_menu(self):
        """
        Affiche le menu d'aide par-dessus la grille.
        """
        if not self.show_help:
            return
        
        # Skip help menu if fonts are not available (headless environment)
        if self.help_font is None or self.help_title_font is None:
            return
        
        # Créer une surface semi-transparente pour l'arrière-plan
        current_size = self.screen.get_size()
        overlay = pygame.Surface(current_size)
        overlay.set_alpha(200)  # Semi-transparent
        overlay.fill((0, 0, 0))  # Noir
        self.screen.blit(overlay, (0, 0))
        
        # Titre du menu d'aide
        title_text = self.help_title_font.render("AIDE - Contrôles disponibles", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(current_size[0] // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Définir les contrôles et leurs descriptions
        controls = [
            ("Navigation & Interface", [
                ("ESC", "Quitter l'application"),
                ("F", "Basculer plein écran/fenêtré"),
                ("I ou TAB", "Afficher/masquer cette aide"),
                ("D", "Afficher/masquer les infos de statut"),
            ]),
            ("Distorsion & Animation", [
                ("ESPACE", "Changer le type de distorsion"),
                ("+/-", "Ajuster l'intensité de distorsion"),
                ("R", "Régénérer les paramètres aléatoires"),
            ]),
            ("Grille & Densité", [
                ("T puis +/-", "Ajuster la densité de grille (nombre de cellules)"),
            ]),
            ("Couleurs", [
                ("C", "Changer le schéma de couleurs"),
                ("A", "Activer/désactiver l'animation des couleurs"),
            ]),
            ("Formes", [
                ("H", "Changer le type de forme"),
                ("Shift+H", "Basculer mode formes mixtes"),
            ]),
            ("Sauvegarde", [
                ("S", "Sauvegarder l'image actuelle (+ paramètres YAML)"),
                ("G", "Démarrer/arrêter l'enregistrement GIF"),
            ]),
            ("Scènes Sauvegardées", [
                ("L", "Charger la scène suivante"),
                ("K", "Charger la scène précédente"),
                ("P", "Actualiser la liste des scènes"),
            ])
        ]
        
        # Position de départ pour le texte
        y_offset = 100
        section_spacing = 40
        line_spacing = 25
        
        for section_title, section_controls in controls:
            # Titre de section
            section_text = self.help_title_font.render(section_title, True, (255, 200, 100))
            section_rect = section_text.get_rect(center=(current_size[0] // 2, y_offset))
            self.screen.blit(section_text, section_rect)
            y_offset += section_spacing
            
            # Contrôles de la section
            for key, description in section_controls:
                # Afficher la touche en couleur
                key_text = self.help_font.render(f"{key}:", True, (100, 255, 100))
                desc_text = self.help_font.render(description, True, (255, 255, 255))
                
                # Centrer horizontalement
                total_width = key_text.get_width() + desc_text.get_width() + 10
                start_x = (current_size[0] - total_width) // 2
                
                self.screen.blit(key_text, (start_x, y_offset))
                self.screen.blit(desc_text, (start_x + key_text.get_width() + 10, y_offset))
                y_offset += line_spacing
            
            y_offset += 10  # Espacement entre sections
        
        # Instructions en bas
        footer_text = self.help_font.render("Appuyez sur 'I' ou TAB pour fermer cette aide", True, (200, 200, 200))
        footer_rect = footer_text.get_rect(center=(current_size[0] // 2, current_size[1] - 30))
        self.screen.blit(footer_text, footer_rect)
    
    def _render_status_display(self):
        """
        Affiche les informations de statut en haut à droite de l'écran.
        """
        if not self.show_status:
            return
        
        # Skip status display if font is not available (headless environment)
        if self.status_font is None:
            return
        
        current_size = self.screen.get_size()
        
        # Informations à afficher
        total_cells = self.dimension * self.dimension
        status_lines = [
            f"Distorsion: {self.distortion_fn}",
            f"Intensité: {self.distortion_strength:.2f}",
            f"Cellules: {self.dimension}x{self.dimension} ({total_cells})",
            f"Couleurs: {self.color_scheme}"
        ]
        
        # Ajouter des informations supplémentaires si pertinentes
        if self.color_animation:
            status_lines.append("Color animation: ON")
        if self.mixed_shapes:
            status_lines.append("Formes: Mixtes")
        else:
            status_lines.append(f"Forme: {self.shape_type}")
        if self.is_recording:
            status_lines.append(f"REC: {len(self.recorded_frames)}f")
        
        # Calculer la position de départ (en haut à droite avec marge)
        margin = 10
        line_height = 22
        max_width = 0
        
        # Calculer la largeur maximale nécessaire
        for line in status_lines:
            text_surface = self.status_font.render(line, True, (255, 255, 255))
            max_width = max(max_width, text_surface.get_width())
        
        # Créer un fond semi-transparent
        background_width = max_width + 20
        background_height = len(status_lines) * line_height + 10
        background_rect = pygame.Rect(
            current_size[0] - background_width - margin,
            margin,
            background_width,
            background_height
        )
        
        # Dessiner le fond semi-transparent
        overlay = pygame.Surface((background_width, background_height))
        overlay.set_alpha(128)  # Semi-transparent
        overlay.fill((0, 0, 0))  # Noir
        self.screen.blit(overlay, background_rect.topleft)
        
        # Dessiner chaque ligne de texte
        start_x = current_size[0] - max_width - margin - 10
        start_y = margin + 5
        
        for i, line in enumerate(status_lines):
            text_surface = self.status_font.render(line, True, (255, 255, 255))
            y_pos = start_y + i * line_height
            self.screen.blit(text_surface, (start_x, y_pos))
    
    def render(self):
        """Rend la grille déformée sur l'écran"""
        self.screen.fill(self.background_color)
        
        # Obtenir toutes les positions déformées
        positions = self._get_distorted_positions()
        
        # Dessiner chaque forme déformée avec sa couleur
        for i, (x, y, rotation) in enumerate(positions):
            # Obtenir la couleur de base et appliquer l'animation si nécessaire
            base_color = self.base_colors[i]
            final_color = ColorGenerator.get_animated_color(
                base_color, i, self.time, self.color_animation
            )
            
            # Obtenir le type de forme pour cette cellule
            shape_type = self.shape_types[i]
            
            self._draw_shape(self.screen, x, y, rotation, self.cell_size, final_color, shape_type)
        
        # Afficher le menu d'aide si activé
        self._render_help_menu()
        
        # Afficher le statut si activé
        self._render_status_display()
        
        pygame.display.flip()
    
    def update(self):
        """Met à jour l'animation"""
        self.time += self.animation_speed
        
    def start_gif_recording(self):
        """Démarre l'enregistrement GIF"""
        if self.is_recording:
            print("⚠️ Enregistrement déjà en cours!")
            return
            
        self.is_recording = True
        self.recorded_frames = []
        self.recording_start_time = datetime.datetime.now()
        print(f"🔴 Enregistrement GIF démarré (max {self.max_frames} frames)")
        print("   Appuyez sur 'G' à nouveau pour arrêter et sauvegarder")
    
    def stop_gif_recording(self):
        """Arrête l'enregistrement et sauvegarde le GIF"""
        if not self.is_recording:
            print("⚠️ Aucun enregistrement en cours!")
            return
            
        self.is_recording = False
        
        if len(self.recorded_frames) == 0:
            print("⚠️ Aucune frame capturée!")
            return
            
        # Créer le GIF dans un thread séparé pour éviter de bloquer l'UI
        thread = threading.Thread(target=self._save_gif_async)
        thread.start()
        print(f"🟡 Arrêt de l'enregistrement ({len(self.recorded_frames)} frames)")
        print("   Création du GIF en cours...")
    
    def _capture_frame(self):
        """Capture la frame actuelle pour l'enregistrement GIF"""
        if not self.is_recording:
            return
            
        # Éviter de capturer trop de frames
        if len(self.recorded_frames) >= self.max_frames:
            print(f"⚠️ Limite de frames atteinte ({self.max_frames}), arrêt auto...")
            self.stop_gif_recording()
            return
            
        # Capturer chaque N-ième frame selon frame_skip
        frame_count = len(self.recorded_frames)
        if frame_count % self.frame_skip == 0:
            # Convertir la surface pygame en array numpy
            surface_array = pygame.surfarray.array3d(self.screen)
            # Pygame utilise (width, height, channels), nous devons transposer en (height, width, channels)
            frame_array = np.transpose(surface_array, (1, 0, 2))
            self.recorded_frames.append(frame_array)
    
    def _save_gif_async(self):
        """Sauvegarde le GIF de façon asynchrone"""
        try:
            
            # Générer un nom de fichier unique
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_art_animation.gif"
            # Créer le dossier 'gifs' s'il n'existe pas
            gif_folder = "gifs"
            if not os.path.exists(gif_folder):
                os.makedirs(gif_folder)
            filename = os.path.join(gif_folder, filename)
            # Créer le GIF avec imageio
            # FPS ajusté selon le frame_skip pour avoir une animation fluide
            fps = 60 // self.frame_skip if self.frame_skip > 0 else 30
            fps = min(fps, 20)  # Limiter le FPS pour éviter des GIFs trop rapides
            
            imageio.mimsave(filename, self.recorded_frames, fps=fps, loop=0)
            
            duration = len(self.recorded_frames) / fps
            print(f"✅ GIF sauvegardé: {filename}")
            print(f"   📊 {len(self.recorded_frames)} frames, {duration:.1f}s, {fps} FPS")
            
        except ImportError:
            print("❌ Erreur: imageio non installé!")
            print("   Installez avec: pip install imageio")
            # Fallback: sauvegarder les frames individuellement
            self._save_frames_as_images()
        except Exception as e:
            print(f"❌ Erreur lors de la création du GIF: {e}")
            self._save_frames_as_images()
    
    def _save_frames_as_images(self):
        """Sauvegarde les frames comme images individuelles (fallback)"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"💾 Sauvegarde de {len(self.recorded_frames)} frames individuelles...")
        
        for i, frame in enumerate(self.recorded_frames):
            filename = f"frame_{timestamp}_{i:04d}.png"
            # Convertir numpy array vers surface pygame puis sauvegarder
            frame_transposed = np.transpose(frame, (1, 0, 2))
            surface = pygame.surfarray.make_surface(frame_transposed)
            pygame.image.save(surface, filename)
            
        print(f"✅ Frames sauvegardées: frame_{timestamp}_0000.png à frame_{timestamp}_{len(self.recorded_frames)-1:04d}.png")

    def run_interactive(self):
        """Lance la boucle interactive principale"""
        running = True
        
        print("Contrôles:")
        print("- ESC: Quitter")
        print("- I ou TAB: Afficher/masquer l'aide")
        print("- D: Afficher/masquer les infos de statut")
        print("- F: Basculer plein écran/fenêtré")
        print("- SPACE: Changer le type de distorsion")
        print("- C: Changer le schéma de couleurs")

        print("- A: Activer/désactiver l'animation des couleurs")
        print("- H: Changer le type de forme")
        print("- Shift+H: Basculer mode formes mixtes")
        print("- +/-: Ajuster l'intensité de distorsion")
        print("- T puis +/-: Ajuster la densité de grille (nombre de cellules)")
        print("- R: Régénérer les paramètres aléatoires")
        print("- S: Sauvegarder l'image")
        print("- G: Démarrer/arrêter l'enregistrement GIF")
        
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_i:
                        # I pour "Info" - aide
                        self.show_help = not self.show_help
                        status = "affiché" if self.show_help else "masqué"
                        print(f"Menu d'aide: {status}")
                    elif event.key == pygame.K_TAB:
                        # Tab comme alternative pour l'aide (facile d'accès)
                        self.show_help = not self.show_help
                        status = "affiché" if self.show_help else "masqué"
                        print(f"Menu d'aide: {status}")
                    elif event.key == pygame.K_d:
                        # D pour basculer l'affichage du statut
                        self.show_status = not self.show_status
                        status = "affiché" if self.show_status else "masqué"
                        print(f"Affichage du statut: {status}")
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

                    elif event.key == pygame.K_t:
                        # Basculer le mode d'ajustement de la densité de grille
                        self.grid_density_mode = not self.grid_density_mode
                        mode_text = "activé" if self.grid_density_mode else "désactivé"
                        action_text = "Utilisez +/- pour ajuster" if self.grid_density_mode else ""
                        print(f"Mode ajustement densité de grille: {mode_text} {action_text}")
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        if self.grid_density_mode:
                            # Augmenter la densité de grille (plus de cellules)
                            self._update_grid_density(increase=True)
                        else:
                            # Augmenter l'intensité de distorsion
                            self.distortion_strength = min(1.0, self.distortion_strength + 0.1)
                            self.base_distortion_strength = self.distortion_strength
                            print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_MINUS:
                        if self.grid_density_mode:
                            # Diminuer la densité de grille (moins de cellules)
                            self._update_grid_density(increase=False)
                        else:
                            # Diminuer l'intensité de distorsion
                            self.distortion_strength = max(0.0, self.distortion_strength - 0.1)
                            self.base_distortion_strength = self.distortion_strength
                            print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_r:
                        # Régénérer les paramètres
                        self._generate_distortions()
                        self._generate_base_colors()
                        self._generate_shape_types()
                        print("Paramètres régénérés")
                    elif event.key == pygame.K_s:
                        # Sauvegarder
                        self.save_image(f"deformed_grid_{self.distortion_fn}_{int(self.time*100)}.png")
                        print("Image sauvegardée")
                    elif event.key == pygame.K_h and (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                        # Basculer le mode formes mixtes (Shift+H) - doit être testé en PREMIER
                        self.mixed_shapes = not self.mixed_shapes
                        self._generate_shape_types()  # Régénérer les formes
                        mode = "formes mixtes" if self.mixed_shapes else "forme unique"
                        print(f"Mode: {mode} ({self.shape_type})")
                    elif event.key == pygame.K_h:
                        # Changer le type de forme (H seul)
                        shape_types = [s.value for s in ShapeType]
                        current_shape_index = shape_types.index(self.shape_type) if self.shape_type in shape_types else 0
                        current_shape_index = (current_shape_index + 1) % len(shape_types)
                        self.shape_type = shape_types[current_shape_index]
                        self._generate_shape_types()  # Régénérer les formes
                        print(f"Forme: {self.shape_type}")
                    elif event.key == pygame.K_f:
                        # Basculer plein écran
                        self.toggle_fullscreen()
                        mode = "plein écran" if self.is_fullscreen else "fenêtré"
                        print(f"Mode: {mode}")
                    elif event.key == pygame.K_g:
                        # Basculer l'enregistrement GIF
                        if self.is_recording:
                            self.stop_gif_recording()
                        else:
                            self.start_gif_recording()
                    elif event.key == pygame.K_l:
                        # Charger la scène suivante
                        self.load_next_scene()
                    elif event.key == pygame.K_k:
                        # Charger la scène précédente
                        self.load_previous_scene()
                    elif event.key == pygame.K_p:
                        # Actualiser la liste des scènes sauvegardées
                        self.refresh_saved_scenes()
            
            self.update()
            self.render()
            
            # Capturer la frame pour l'enregistrement GIF si actif
            self._capture_frame()
            
            self.clock.tick(60)  # 60 FPS
        
        # Auto-sauvegarder le GIF si un enregistrement est en cours
        if self.is_recording:
            print("\n🟡 Fermeture de l'application - sauvegarde automatique du GIF...")
            self.stop_gif_recording()
            # Attendre un peu pour permettre au thread de se terminer
            import time
            time.sleep(2)
        
        pygame.quit()
    
    def toggle_fullscreen(self):
        """Basculer entre mode fenêtré et plein écran"""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            # Passer en plein écran
            self.screen = pygame.display.set_mode(self.fullscreen_size, pygame.FULLSCREEN)
        else:
            # Retour au mode fenêtré
            self.screen = pygame.display.set_mode(self.windowed_size)
        
        # Recalculer les offsets pour centrer la grille avec la taille d'écran appropriée
        current_size = self.fullscreen_size if self.is_fullscreen else self.windowed_size
        grid_total_size = self.dimension * self.cell_size
        self.offset_x = (current_size[0] - grid_total_size) // 2
        self.offset_y = (current_size[1] - grid_total_size) // 2
        
        # Recalculer les positions de base avec les nouveaux offsets
        self._generate_base_positions()
    
    def save_image(self, filename: str):
        """Sauvegarde l'image actuelle avec ses paramètres"""

        # Create the folders if they don't exist
        os.makedirs("images", exist_ok=True)
        os.makedirs("saved_params", exist_ok=True)
        
        # Save the image
        image_path = os.path.join("images", filename)
        pygame.image.save(self.screen, image_path)
        
        # Save the parameters in YAML format
        base_name = os.path.splitext(filename)[0]  # Remove extension
        param_filename = f"{base_name}.yaml"
        param_path = os.path.join("saved_params", param_filename)
        
        self.save_parameters(param_path)
        
        print(f"Image sauvegardée: {image_path}")
        print(f"Paramètres sauvegardés: {param_path}")
    
    def get_current_parameters(self) -> dict:
        """Retourne tous les paramètres actuels de la grille"""
        return {
            # Core parameters
            "dimension": self.dimension,
            "cell_size": self.cell_size,
            "canvas_size": list(self.canvas_size),
            "distortion_strength": self.distortion_strength,
            "distortion_fn": self.distortion_fn,
            "background_color": list(self.background_color),
            "square_color": list(self.square_color),
            "color_scheme": self.color_scheme,
            "color_animation": self.color_animation,
            "shape_type": self.shape_type,
            "mixed_shapes": self.mixed_shapes,
            
            # Animation parameters
            "time": self.time,
            "animation_speed": self.animation_speed,
            
            # Display settings
            "show_help": self.show_help,
            "show_status": self.show_status,
            "is_fullscreen": self.is_fullscreen,
            "windowed_size": list(self.windowed_size),
            
            # Grid density settings
            "base_dimension": self.base_dimension,
            "grid_density_mode": self.grid_density_mode,
            
            # Grid positioning (calculated automatically but saved for reference)
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            
            # Metadata
            "saved_at": datetime.datetime.now().isoformat(),
            "saved_filename": None  # Will be set when saving
        }
    
    def save_parameters(self, filepath: str):
        """Sauvegarde les paramètres actuels dans un fichier YAML"""
        params = self.get_current_parameters()
        params["saved_filename"] = os.path.basename(filepath)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(params, f, default_flow_style=False, indent=2, allow_unicode=True)
    
    def load_parameters(self, filepath: str):
        """Charge les paramètres depuis un fichier YAML et les applique"""
        if not os.path.exists(filepath):
            print(f"Fichier de paramètres non trouvé: {filepath}")
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                params = yaml.safe_load(f)
            
            # Apply core parameters
            self.dimension = params.get("dimension", self.dimension)
            self.cell_size = params.get("cell_size", self.cell_size)
            self.canvas_size = tuple(params.get("canvas_size", self.canvas_size))
            self.distortion_strength = params.get("distortion_strength", self.distortion_strength)
            self.distortion_fn = params.get("distortion_fn", self.distortion_fn)
            self.background_color = tuple(params.get("background_color", self.background_color))
            self.square_color = tuple(params.get("square_color", self.square_color))
            self.color_scheme = params.get("color_scheme", self.color_scheme)
            self.color_animation = params.get("color_animation", self.color_animation)
            self.shape_type = params.get("shape_type", self.shape_type)
            self.mixed_shapes = params.get("mixed_shapes", self.mixed_shapes)
            
            # Apply animation parameters
            self.time = params.get("time", self.time)
            self.animation_speed = params.get("animation_speed", self.animation_speed)
            
            # Apply display settings
            self.show_help = params.get("show_help", self.show_help)
            self.show_status = params.get("show_status", self.show_status)
            
            # Apply grid density settings
            self.base_dimension = params.get("base_dimension", self.base_dimension)
            self.grid_density_mode = params.get("grid_density_mode", self.grid_density_mode)
            
            # Update base distortion strength
            self.base_distortion_strength = self.distortion_strength
            
            # Recalculate offsets to center the grid with new dimensions
            grid_total_size = self.dimension * self.cell_size
            self.offset_x = (self.canvas_size[0] - grid_total_size) // 2
            self.offset_y = (self.canvas_size[1] - grid_total_size) // 2
            
            # Regenerate everything with new parameters
            self._generate_base_positions()
            self._generate_distortions()
            self._generate_base_colors()
            self._generate_shape_types()
            
            print(f"Paramètres chargés depuis: {filepath}")
            print(f"Scene: {params.get('distortion_fn', 'N/A')} | {params.get('color_scheme', 'N/A')} | {params.get('shape_type', 'N/A')}")
            return True
            
        except Exception as e:
            print(f"Erreur lors du chargement des paramètres: {e}")
            return False
    
    def get_saved_scenes(self) -> list:
        """Retourne la liste des scènes sauvegardées (fichiers YAML)"""
        if not os.path.exists("saved_params"):
            return []
        
        yaml_files = glob.glob(os.path.join("saved_params", "*.yaml"))
        yaml_files.sort(key=os.path.getmtime, reverse=True)  # Sort by modification time, newest first
        return yaml_files
    
    def initialize_scene_iteration(self):
        """Initialise l'itération des scènes sauvegardées"""
        self.saved_scenes = self.get_saved_scenes()
        if self.saved_scenes:
            self.current_scene_index = 0
            self.scene_iteration_mode = True
            print(f"🎬 Mode itération de scènes activé! {len(self.saved_scenes)} scène(s) trouvée(s)")
            print("🎮 Utilisez L (suivant) et K (précédent) pour naviguer")
            return True
        else:
            print("🚫 Aucune scène sauvegardée trouvée dans le dossier saved_params/")
            return False
    
    def load_next_scene(self):
        """Charge la prochaine scène sauvegardée"""
        if not self.scene_iteration_mode or not self.saved_scenes:
            if not self.initialize_scene_iteration():
                return
        
        self.current_scene_index = (self.current_scene_index + 1) % len(self.saved_scenes)
        scene_file = self.saved_scenes[self.current_scene_index]
        scene_name = os.path.splitext(os.path.basename(scene_file))[0]
        
        if self.load_parameters(scene_file):
            print(f"🎬 Scène {self.current_scene_index + 1}/{len(self.saved_scenes)}: {scene_name}")
    
    def load_previous_scene(self):
        """Charge la scène précédente sauvegardée"""
        if not self.scene_iteration_mode or not self.saved_scenes:
            if not self.initialize_scene_iteration():
                return
        
        self.current_scene_index = (self.current_scene_index - 1) % len(self.saved_scenes)
        scene_file = self.saved_scenes[self.current_scene_index]
        scene_name = os.path.splitext(os.path.basename(scene_file))[0]
        
        if self.load_parameters(scene_file):
            print(f"🎬 Scène {self.current_scene_index + 1}/{len(self.saved_scenes)}: {scene_name}")
    
    def refresh_saved_scenes(self):
        """Actualise la liste des scènes sauvegardées"""
        self.saved_scenes = self.get_saved_scenes()
        if self.saved_scenes and self.current_scene_index >= len(self.saved_scenes):
            self.current_scene_index = 0
        print(f"🔄 Liste des scènes actualisée: {len(self.saved_scenes)} scène(s) trouvée(s)")