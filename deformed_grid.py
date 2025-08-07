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
import colorsys
import threading
import queue

# Audio processing imports (optional - will gracefully degrade if not available)
try:
    import pyaudio
    import scipy.signal
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Audio libraries not available. Install pyaudio and scipy for music reactivity:")
    print("pip install pyaudio scipy")


class DistortionType(Enum):
    """Types de distorsion disponibles"""
    RANDOM = "random"
    SINE = "sine" 
    PERLIN = "perlin"
    CIRCULAR = "circular"


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


class AudioAnalyzer:
    """
    Analyseur audio en temps réel pour la réactivité musicale.
    
    Capture l'audio du microphone et extrait les caractéristiques fréquentielles
    pour contrôler les paramètres visuels.
    """
    
    def __init__(self, sample_rate: int = 44100, chunk_size: int = 1024):
        """
        Initialise l'analyseur audio.
        
        Args:
            sample_rate: Fréquence d'échantillonnage audio
            chunk_size: Taille des blocs audio à analyser
        """
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.audio_thread = None
        
        # Paramètres d'analyse
        self.bass_range = (20, 250)      # Hz
        self.mid_range = (250, 4000)     # Hz  
        self.high_range = (4000, 20000)  # Hz
        
        # Variables de sortie (thread-safe)
        self.bass_level = 0.0
        self.mid_level = 0.0
        self.high_level = 0.0
        self.overall_volume = 0.0
        self.beat_detected = False
        
        # Historique pour la détection de beats
        self.volume_history = []
        self.beat_threshold = 1.3
        self.beat_cooldown = 0
        
        # Lissage des valeurs
        self.smoothing_factor = 0.8
        
        # PyAudio setup
        if AUDIO_AVAILABLE:
            self.pa = pyaudio.PyAudio()
            self.stream = None
        else:
            self.pa = None
            self.stream = None
    
    def start_audio_capture(self):
        """Démarre la capture audio en arrière-plan"""
        if not AUDIO_AVAILABLE:
            print("Audio non disponible - mode silencieux")
            return False
            
        try:
            self.stream = self.pa.open(
                format=pyaudio.paFloat32,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback
            )
            
            self.is_running = True
            self.audio_thread = threading.Thread(target=self._process_audio, daemon=True)
            self.audio_thread.start()
            
            print("🎵 Capture audio démarrée - Votre art réagit maintenant à la musique!")
            return True
            
        except Exception as e:
            print(f"Erreur audio: {e}")
            return False
    
    def stop_audio_capture(self):
        """Arrête la capture audio"""
        self.is_running = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        
        if self.pa:
            self.pa.terminate()
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback pour recevoir les données audio"""
        try:
            audio_data = np.frombuffer(in_data, dtype=np.float32)
            self.audio_queue.put(audio_data, block=False)
        except queue.Full:
            pass  # Skip if queue is full
        return (None, pyaudio.paContinue)
    
    def _process_audio(self):
        """Thread principal de traitement audio"""
        while self.is_running:
            try:
                # Récupérer les données audio
                audio_data = self.audio_queue.get(timeout=0.1)
                
                # Calculer la FFT
                fft = np.fft.rfft(audio_data)
                magnitude = np.abs(fft)
                
                # Créer l'échelle de fréquences
                freqs = np.fft.rfftfreq(len(audio_data), 1/self.sample_rate)
                
                # Extraire les niveaux par bande de fréquence
                bass_indices = np.where((freqs >= self.bass_range[0]) & (freqs <= self.bass_range[1]))
                mid_indices = np.where((freqs >= self.mid_range[0]) & (freqs <= self.mid_range[1]))
                high_indices = np.where((freqs >= self.high_range[0]) & (freqs <= self.high_range[1]))
                
                # Calculer les niveaux moyens (avec lissage)
                bass_new = np.mean(magnitude[bass_indices]) if len(bass_indices[0]) > 0 else 0
                mid_new = np.mean(magnitude[mid_indices]) if len(mid_indices[0]) > 0 else 0
                high_new = np.mean(magnitude[high_indices]) if len(high_indices[0]) > 0 else 0
                volume_new = np.mean(magnitude)
                
                # Appliquer le lissage
                self.bass_level = self.bass_level * self.smoothing_factor + bass_new * (1 - self.smoothing_factor)
                self.mid_level = self.mid_level * self.smoothing_factor + mid_new * (1 - self.smoothing_factor)
                self.high_level = self.high_level * self.smoothing_factor + high_new * (1 - self.smoothing_factor)
                self.overall_volume = self.overall_volume * self.smoothing_factor + volume_new * (1 - self.smoothing_factor)
                
                # Détection de beats
                self._detect_beat(volume_new)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Erreur traitement audio: {e}")
                continue
    
    def _detect_beat(self, current_volume):
        """Détecte les beats dans l'audio"""
        self.volume_history.append(current_volume)
        
        # Garder seulement les 20 dernières valeurs
        if len(self.volume_history) > 20:
            self.volume_history.pop(0)
        
        # Réduire le cooldown
        if self.beat_cooldown > 0:
            self.beat_cooldown -= 1
        
        # Détecter un beat si le volume actuel dépasse significativement la moyenne récente
        if len(self.volume_history) >= 10 and self.beat_cooldown == 0:
            recent_avg = np.mean(self.volume_history[:-5])  # Moyenne des valeurs récentes
            if current_volume > recent_avg * self.beat_threshold:
                self.beat_detected = True
                self.beat_cooldown = 10  # Cooldown pour éviter les faux positifs
                return
        
        self.beat_detected = False
    
    def get_audio_features(self) -> dict:
        """
        Retourne les caractéristiques audio actuelles.
        
        Returns:
            Dict avec bass_level, mid_level, high_level, overall_volume, beat_detected
        """
        return {
            'bass_level': min(self.bass_level * 100, 1.0),      # Normalisé 0-1
            'mid_level': min(self.mid_level * 50, 1.0),         # Normalisé 0-1  
            'high_level': min(self.high_level * 20, 1.0),       # Normalisé 0-1
            'overall_volume': min(self.overall_volume * 30, 1.0), # Normalisé 0-1
            'beat_detected': self.beat_detected
        }


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
                 audio_reactive: bool = False):
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
        
        # Audio analyzer
        self.audio_analyzer = AudioAnalyzer() if audio_reactive else None
        self.base_distortion_strength = distortion_strength  # Sauvegarde de l'intensité de base
        
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
            
            color = self._get_color_for_position(x_norm, y_norm, distance_to_center, i)
            self.base_colors.append(color)
    
    def _get_color_for_position(self, x_norm: float, y_norm: float, 
                               distance_to_center: float, index: int) -> Tuple[int, int, int]:
        """
        Génère une couleur pour une position donnée selon le schéma de couleur actuel.
        
        Args:
            x_norm: Position X normalisée (0.0 à 1.0)
            y_norm: Position Y normalisée (0.0 à 1.0)
            distance_to_center: Distance au centre normalisée (0.0 à 1.0)
            index: Index du carré dans la grille
            
        Returns:
            Tuple RGB (r, g, b)
        """
        if self.color_scheme == ColorScheme.MONOCHROME.value:
            return self.square_color
            
        elif self.color_scheme == ColorScheme.GRADIENT.value:
            # Gradient diagonal du coin supérieur gauche au coin inférieur droit
            t = (x_norm + y_norm) / 2.0
            r = int(50 + t * 205)
            g = int(100 + t * 155)
            b = int(200 - t * 100)
            return (r, g, b)
            
        elif self.color_scheme == ColorScheme.RAINBOW.value:
            # Arc-en-ciel basé sur la position
            hue = (x_norm + y_norm * 0.5) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif self.color_scheme == ColorScheme.COMPLEMENTARY.value:
            # Couleurs complémentaires alternées
            if (index + (index // self.dimension)) % 2 == 0:
                return (255, 100, 50)  # Orange
            else:
                return (50, 150, 255)  # Bleu
                
        elif self.color_scheme == ColorScheme.TEMPERATURE.value:
            # Couleurs chaudes au centre, froides aux bords
            temp = 1.0 - distance_to_center
            if temp > 0.7:
                # Très chaud - rouge/jaune
                r, g, b = colorsys.hsv_to_rgb(0.1, 0.8, 1.0)
            elif temp > 0.4:
                # Chaud - orange/rouge
                r, g, b = colorsys.hsv_to_rgb(0.05, 0.9, 0.9)
            else:
                # Froid - bleu/violet
                r, g, b = colorsys.hsv_to_rgb(0.6 + temp * 0.2, 0.7, 0.8)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif self.color_scheme == ColorScheme.PASTEL.value:
            # Couleurs pastel douces
            hue = (x_norm * 0.3 + y_norm * 0.7) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 0.3, 0.9)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif self.color_scheme == ColorScheme.NEON.value:
            # Couleurs néon vives
            hue = (distance_to_center + x_norm * 0.5) % 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            return (int(r * 255), int(g * 255), int(b * 255))
            
        elif self.color_scheme == ColorScheme.OCEAN.value:
            # Thème océan - bleus et verts
            depth = distance_to_center
            if depth < 0.3:
                # Eau peu profonde - turquoise
                return (64, 224, 208)
            elif depth < 0.7:
                # Eau moyenne - bleu océan
                return (0, 119, 190)
            else:
                # Eau profonde - bleu foncé
                return (25, 25, 112)
                
        elif self.color_scheme == ColorScheme.FIRE.value:
            # Thème feu - rouges, oranges, jaunes
            intensity = 1.0 - distance_to_center + y_norm * 0.3
            if intensity > 0.8:
                return (255, 255, 100)  # Jaune chaud
            elif intensity > 0.5:
                return (255, 140, 0)    # Orange
            else:
                return (220, 20, 60)    # Rouge foncé
                
        elif self.color_scheme == ColorScheme.FOREST.value:
            # Thème forêt - verts variés
            green_intensity = 0.3 + distance_to_center * 0.7 + x_norm * 0.2
            if green_intensity > 0.8:
                return (144, 238, 144)  # Vert clair
            elif green_intensity > 0.5:
                return (34, 139, 34)    # Vert forêt
            else:
                return (0, 100, 0)      # Vert foncé
        
        # Par défaut, retourner blanc
        return (255, 255, 255)
    
    def _get_animated_color(self, base_color: Tuple[int, int, int], 
                           position_index: int) -> Tuple[int, int, int]:
        """
        Applique une animation de couleur si activée.
        
        Args:
            base_color: Couleur de base du carré
            position_index: Index de position pour variation
            
        Returns:
            Couleur animée ou couleur de base si animation désactivée
        """
        if not self.color_animation and not self.audio_reactive:
            return base_color
        
        r, g, b = base_color
        
        # Animation normale si pas d'audio
        if not self.audio_reactive or not self.audio_analyzer:
            pulse = math.sin(self.time * 2 + position_index * 0.1) * 0.2 + 1.0
            pulse = max(0.5, min(1.5, pulse))
            r = int(min(255, r * pulse))
            g = int(min(255, g * pulse))
            b = int(min(255, b * pulse))
            return (r, g, b)
        
        # Animation réactive à l'audio
        audio_features = self.audio_analyzer.get_audio_features()
        
        # Beat detection - flash blanc sur les beats
        if audio_features['beat_detected']:
            flash_intensity = 0.7
            r = int(min(255, r + (255 - r) * flash_intensity))
            g = int(min(255, g + (255 - g) * flash_intensity))
            b = int(min(255, b + (255 - b) * flash_intensity))
        
        # Hautes fréquences - augmentent la luminosité
        high_boost = 1.0 + audio_features['high_level'] * 0.5
        r = int(min(255, r * high_boost))
        g = int(min(255, g * high_boost))
        b = int(min(255, b * high_boost))
        
        # Moyennes fréquences - rotation de teinte
        if audio_features['mid_level'] > 0.1:
            # Convertir en HSV pour rotation de teinte
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            h = (h + audio_features['mid_level'] * 0.3) % 1.0
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            r, g, b = int(r * 255), int(g * 255), int(b * 255)
        
        return (r, g, b)
    
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
            final_color = self._get_animated_color(base_color, i)
            
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
                        print(f"Intensité: {self.distortion_strength:.1f}")
                    elif event.key == pygame.K_MINUS:
                        # Diminuer l'intensité
                        self.distortion_strength = max(0.0, self.distortion_strength - 0.1)
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
    
    def save_image(self, filename: str):
        """Sauvegarde l'image actuelle"""
        pygame.image.save(self.screen, filename)
        print(f"Image sauvegardée: {filename}")


# Fonctions utilitaires pour une utilisation simple

def create_deformed_grid(dimension: int = 64, 
                        cell_size: int = 8,
                        distortion_strength: float = 0.0,
                        distortion_fn: str = "random",
                        color_scheme: str = "rainbow",
                        color_animation: bool = False,
                        audio_reactive: bool = False,
                        fullscreen: bool = False) -> DeformedGrid:
    """
    Crée une grille déformée avec des paramètres simples.
    
    Args:
        dimension: Nombre de cellules par ligne/colonne
        cell_size: Taille moyenne d'un carré en pixels  
        distortion_strength: Intensité de la déformation (0.0 à 1.0)
        distortion_fn: Type de distorsion ("random", "sine", "perlin", "circular")
        color_scheme: Schéma de couleurs ("monochrome", "gradient", "rainbow", etc.)
        color_animation: Si True, les couleurs sont animées
        audio_reactive: Si True, réagit à l'audio en temps réel
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
        distortion_fn=distortion_fn,
        color_scheme=color_scheme,
        color_animation=color_animation,
        audio_reactive=audio_reactive
    )
    
    # Si plein écran demandé, l'activer immédiatement
    if fullscreen:
        grid.toggle_fullscreen()
    
    return grid


def quick_demo():
    """Démonstration rapide avec paramètres par défaut"""
    grid = create_deformed_grid(dimension=64, cell_size=16, distortion_strength=0.3, 
                               color_scheme="rainbow", color_animation=True)
    grid.run_interactive()


def fullscreen_demo():
    """Démonstration en plein écran"""
    grid = create_deformed_grid(dimension=80, cell_size=20, distortion_strength=0.4, 
                               color_scheme="neon", color_animation=True, fullscreen=True)
    grid.run_interactive()


def audio_reactive_demo():
    """Démonstration avec réactivité audio - PARFAIT POUR LA MUSIQUE! 🎵"""
    grid = create_deformed_grid(
        dimension=64, 
        cell_size=18, 
        distortion_strength=0.2,  # Distorsion de base plus faible (l'audio l'augmente)
        distortion_fn="sine",
        color_scheme="neon", 
        color_animation=True, 
        audio_reactive=True,
        fullscreen=True
    )
    print("\n🎵 MODE AUDIO-RÉACTIF ACTIVÉ!")
    print("🎧 Lancez votre musique préférée et regardez l'art danser!")
    print("🔊 Plus la musique est forte, plus les effets sont intenses!")
    grid.run_interactive()


if __name__ == "__main__":
    # Choisir la démo à lancer
    audio_reactive_demo()  # Mode audio-réactif par défaut!