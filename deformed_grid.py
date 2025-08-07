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
from typing import Callable, Tuple, List, Optional
from enum import Enum


class DistortionType(Enum):
    """Types de distorsion disponibles"""
    RANDOM = "random"
    SINE = "sine" 
    PERLIN = "perlin"
    CIRCULAR = "circular"


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
                 distortion_strength: float = 0.3,
                 distortion_fn: str = "random",
                 background_color: Tuple[int, int, int] = (20, 20, 30),
                 square_color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialise la grille déformée.
        
        Args:
            dimension: Nombre de cellules par ligne/colonne
            cell_size: Taille moyenne d'un carré en pixels
            canvas_size: Taille de la fenêtre (largeur, hauteur)
            distortion_strength: Intensité de la déformation (0.0 à 1.0)
            distortion_fn: Type de fonction de distorsion
            background_color: Couleur de fond RGB
            square_color: Couleur des carrés RGB
        """
        self.dimension = dimension
        self.cell_size = cell_size
        self.canvas_size = canvas_size
        self.distortion_strength = distortion_strength
        self.distortion_fn = distortion_fn
        self.background_color = background_color
        self.square_color = square_color
        
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
            # Paramètres aléatoires pour chaque carré
            distortion_params = {
                'offset_x': random.uniform(-1, 1),
                'offset_y': random.uniform(-1, 1),
                'phase_x': random.uniform(0, 2 * math.pi),
                'phase_y': random.uniform(0, 2 * math.pi),
                'frequency': random.uniform(0.5, 2.0),
                'rotation_phase': random.uniform(0, 2 * math.pi)
            }
            self.distortions.append(distortion_params)
    
    def _apply_distortion_random(self, base_pos: Tuple[float, float], 
                                params: dict) -> Tuple[float, float, float]:
        """
        Applique une distorsion aléatoire statique.
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        max_offset = self.cell_size * self.distortion_strength
        dx = params['offset_x'] * max_offset
        dy = params['offset_y'] * max_offset
        rotation = params['rotation_phase'] * self.distortion_strength * 0.2
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    def _apply_distortion_sine(self, base_pos: Tuple[float, float], 
                              params: dict) -> Tuple[float, float, float]:
        """
        Applique une distorsion sinusoïdale animée.
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        max_offset = self.cell_size * self.distortion_strength
        
        # Distorsion sinusoïdale avec phases différentes
        dx = math.sin(self.time * params['frequency'] + params['phase_x']) * max_offset
        dy = math.cos(self.time * params['frequency'] + params['phase_y']) * max_offset
        rotation = math.sin(self.time + params['rotation_phase']) * self.distortion_strength * 0.3
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    def _apply_distortion_perlin(self, base_pos: Tuple[float, float], 
                                params: dict) -> Tuple[float, float, float]:
        """
        Applique une distorsion basée sur du bruit de Perlin simplifié.
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        # Simulation simple de bruit de Perlin avec des sinus multiples
        max_offset = self.cell_size * self.distortion_strength
        
        # Utilisation de la position pour créer un bruit cohérent spatialement
        noise_x = (math.sin(base_pos[0] * 0.01 + self.time) + 
                  math.sin(base_pos[0] * 0.03 + self.time * 0.5) * 0.5)
        noise_y = (math.cos(base_pos[1] * 0.01 + self.time) + 
                  math.cos(base_pos[1] * 0.03 + self.time * 0.5) * 0.5)
        
        dx = noise_x * max_offset * 0.5
        dy = noise_y * max_offset * 0.5
        rotation = noise_x * self.distortion_strength * 0.2
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    def _apply_distortion_circular(self, base_pos: Tuple[float, float], 
                                  params: dict) -> Tuple[float, float, float]:
        """
        Applique une distorsion circulaire depuis le centre.
        
        Returns:
            Tuple[x, y, rotation] - Position déformée et rotation
        """
        center_x = self.canvas_size[0] // 2
        center_y = self.canvas_size[1] // 2
        
        # Distance au centre
        dx_center = base_pos[0] - center_x
        dy_center = base_pos[1] - center_y
        distance = math.sqrt(dx_center**2 + dy_center**2)
        
        if distance == 0:
            return (base_pos[0], base_pos[1], 0)
        
        # Effet d'onde circulaire
        wave = math.sin(distance * 0.02 - self.time * 2) * self.distortion_strength
        max_offset = self.cell_size * wave
        
        # Direction radiale
        dx = (dx_center / distance) * max_offset
        dy = (dy_center / distance) * max_offset
        rotation = wave * 0.5
        
        return (base_pos[0] + dx, base_pos[1] + dy, rotation)
    
    def _get_distorted_positions(self) -> List[Tuple[float, float, float]]:
        """
        Calcule toutes les positions déformées selon la fonction choisie.
        
        Returns:
            Liste de tuples (x, y, rotation) pour chaque carré
        """
        positions = []
        
        for i, (base_pos, params) in enumerate(zip(self.base_positions, self.distortions)):
            if self.distortion_fn == DistortionType.RANDOM.value:
                pos = self._apply_distortion_random(base_pos, params)
            elif self.distortion_fn == DistortionType.SINE.value:
                pos = self._apply_distortion_sine(base_pos, params)
            elif self.distortion_fn == DistortionType.PERLIN.value:
                pos = self._apply_distortion_perlin(base_pos, params)
            elif self.distortion_fn == DistortionType.CIRCULAR.value:
                pos = self._apply_distortion_circular(base_pos, params)
            else:
                pos = self._apply_distortion_random(base_pos, params)
            
            positions.append(pos)
        
        return positions
    
    def _draw_deformed_square(self, surface, x: float, y: float, 
                             rotation: float, size: int):
        """
        Dessine un carré déformé à la position donnée.
        
        Args:
            surface: Surface pygame où dessiner
            x, y: Position du centre du carré
            rotation: Rotation en radians
            size: Taille du carré
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
            rotated_corners.append((new_x, new_y))
        
        # Dessin du polygone
        pygame.draw.polygon(surface, self.square_color, rotated_corners)
    
    def render(self):
        """Rend la grille déformée sur l'écran"""
        self.screen.fill(self.background_color)
        
        # Obtenir toutes les positions déformées
        positions = self._get_distorted_positions()
        
        # Dessiner chaque carré déformé
        for x, y, rotation in positions:
            self._draw_deformed_square(self.screen, x, y, rotation, self.cell_size)
        
        pygame.display.flip()
    
    def update(self):
        """Met à jour l'animation"""
        self.time += self.animation_speed
    
    def run_interactive(self):
        """Lance la boucle interactive principale"""
        running = True
        
        print("Contrôles:")
        print("- ESC: Quitter")
        print("- F: Basculer plein écran/fenêtré")
        print("- SPACE: Changer le type de distorsion")
        print("- +/-: Ajuster l'intensité de distorsion")
        print("- R: Régénérer les paramètres aléatoires")
        print("- S: Sauvegarder l'image")
        
        distortion_types = [t.value for t in DistortionType]
        current_distortion_index = 0
        
        while running:
            for event in pygame.event.get():
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
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        # Augmenter l'intensité
                        self.distortion_strength = min(1.0, self.distortion_strength + 0.1)
                        print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_MINUS:
                        # Diminuer l'intensité
                        self.distortion_strength = max(0.0, self.distortion_strength - 0.1)
                        print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_r:
                        # Régénérer les paramètres
                        self._generate_distortions()
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
            
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        
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
    
    def save_image(self, filename: str):
        """Sauvegarde l'image actuelle"""
        pygame.image.save(self.screen, filename)
        print(f"Image sauvegardée: {filename}")


# Fonctions utilitaires pour une utilisation simple

def create_deformed_grid(dimension: int = 64, 
                        cell_size: int = 8,
                        distortion_strength: float = 0.3,
                        distortion_fn: str = "random",
                        fullscreen: bool = False) -> DeformedGrid:
    """
    Crée une grille déformée avec des paramètres simples.
    
    Args:
        dimension: Nombre de cellules par ligne/colonne
        cell_size: Taille moyenne d'un carré en pixels  
        distortion_strength: Intensité de la déformation (0.0 à 1.0)
        distortion_fn: Type de distorsion ("random", "sine", "perlin", "circular")
        fullscreen: Si True, démarre directement en plein écran
    
    Returns:
        Instance de DeformedGrid configurée
    """
    if fullscreen:
        # Pour le plein écran, utiliser une taille de fenêtre temporaire
        canvas_size = (1200, 900)
    else:
        canvas_size = (dimension * cell_size + 100, dimension * cell_size + 100)
    
    grid = DeformedGrid(
        dimension=dimension,
        cell_size=cell_size,
        canvas_size=canvas_size,
        distortion_strength=distortion_strength,
        distortion_fn=distortion_fn
    )
    
    # Si plein écran demandé, l'activer immédiatement
    if fullscreen:
        grid.toggle_fullscreen()
    
    return grid


def quick_demo():
    """Démonstration rapide avec paramètres par défaut"""
    grid = create_deformed_grid(dimension=64, cell_size=16, distortion_strength=0.4)
    grid.run_interactive()


def fullscreen_demo():
    """Démonstration en plein écran"""
    grid = create_deformed_grid(dimension=80, cell_size=20, distortion_strength=0.4, fullscreen=True)
    grid.run_interactive()


if __name__ == "__main__":
    fullscreen_demo()  # Start in fullscreen mode