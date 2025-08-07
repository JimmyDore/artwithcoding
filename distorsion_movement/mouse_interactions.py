"""
Moteur d'interactions souris pour les grilles déformées.

Ce module gère toutes les interactions utilisateur via la souris :
- Attraction/répulsion des carrés vers/depuis le curseur
- Effets de clic (ondulations, explosions)
- Traînées de mouvement
- Interactions de glisser-déposer
"""

import math
import time
import pygame
from typing import Tuple, List, Dict, Optional, Any
from dataclasses import dataclass

from distorsion_movement.enums import MouseInteractionType, MouseMode, MouseButton


@dataclass
class MouseState:
    """État actuel de la souris"""
    position: Tuple[int, int] = (0, 0)
    prev_position: Tuple[int, int] = (0, 0)
    is_pressed: Dict[str, bool] = None
    is_dragging: bool = False
    drag_start: Optional[Tuple[int, int]] = None
    
    def __post_init__(self):
        if self.is_pressed is None:
            self.is_pressed = {
                MouseButton.LEFT.value: False,
                MouseButton.RIGHT.value: False,
                MouseButton.MIDDLE.value: False
            }


@dataclass
class ClickEffect:
    """Représente un effet de clic temporaire"""
    position: Tuple[float, float]
    effect_type: MouseInteractionType
    start_time: float
    duration: float = 1.0
    max_radius: float = 100.0
    strength: float = 1.0
    
    @property
    def progress(self) -> float:
        """Progrès de l'effet (0.0 à 1.0)"""
        elapsed = time.time() - self.start_time
        return min(elapsed / self.duration, 1.0)
    
    @property
    def is_finished(self) -> bool:
        """L'effet est-il terminé ?"""
        return self.progress >= 1.0
    
    @property
    def current_radius(self) -> float:
        """Rayon actuel de l'effet"""
        return self.max_radius * self.progress
    
    @property
    def current_strength(self) -> float:
        """Force actuelle de l'effet (avec fade out)"""
        fade = 1.0 - self.progress
        return self.strength * fade


class MouseInteractionEngine:
    """
    Moteur principal pour les interactions souris.
    
    Gère le tracking de la souris, calcule les forces d'interaction,
    et maintient les effets temporaires comme les ondulations.
    """
    
    def __init__(self, 
                 interaction_type: MouseInteractionType = MouseInteractionType.ATTRACTION,
                 mouse_mode: MouseMode = MouseMode.CONTINUOUS,
                 strength: float = 0.5,
                 radius: float = 100.0,
                 show_feedback: bool = True):
        """
        Initialise le moteur d'interactions souris.
        
        Args:
            interaction_type: Type d'interaction par défaut
            mouse_mode: Mode de fonctionnement de la souris
            strength: Force de l'interaction (0.0 à 1.0)
            radius: Rayon d'influence en pixels
            show_feedback: Afficher les retours visuels
        """
        self.interaction_type = interaction_type
        self.mouse_mode = mouse_mode
        self.strength = strength
        self.radius = radius
        self.show_feedback = show_feedback
        
        # État de la souris
        self.mouse_state = MouseState()
        
        # Effets temporaires actifs
        self.active_effects: List[ClickEffect] = []
        
        # Historique des positions pour les traînées
        self.position_trail: List[Tuple[Tuple[int, int], float]] = []
        self.max_trail_length = 20
        
        # Paramètres configurables
        self.falloff_power = 2.0  # Puissance de l'atténuation avec la distance
        self.min_distance = 1.0   # Distance minimale pour éviter la division par zéro
        
    def update_mouse_state(self, pygame_events: List[pygame.event.Event]) -> None:
        """
        Met à jour l'état de la souris basé sur les événements pygame.
        
        Args:
            pygame_events: Liste des événements pygame à traiter
        """
        # Sauvegarder la position précédente
        self.mouse_state.prev_position = self.mouse_state.position
        
        # Obtenir la position actuelle
        self.mouse_state.position = pygame.mouse.get_pos()
        
        # Traiter les événements
        for event in pygame_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(event)
        
        # Mettre à jour la traînée
        self._update_trail()
        
        # Nettoyer les effets expirés
        self._cleanup_expired_effects()
    
    def _handle_mouse_button_down(self, event: pygame.event.Event) -> None:
        """Gère les événements de pression des boutons de souris"""
        button_map = {
            1: MouseButton.LEFT.value,
            2: MouseButton.MIDDLE.value, 
            3: MouseButton.RIGHT.value
        }
        
        if event.button in button_map:
            button = button_map[event.button]
            self.mouse_state.is_pressed[button] = True
            
            # Créer un effet selon le bouton pressé
            self._create_click_effect(event.pos, button)
            
            # Démarrer le drag si c'est le bouton gauche
            if button == MouseButton.LEFT.value:
                self.mouse_state.is_dragging = True
                self.mouse_state.drag_start = event.pos
    
    def _handle_mouse_button_up(self, event: pygame.event.Event) -> None:
        """Gère les événements de relâchement des boutons de souris"""
        button_map = {
            1: MouseButton.LEFT.value,
            2: MouseButton.MIDDLE.value,
            3: MouseButton.RIGHT.value
        }
        
        if event.button in button_map:
            button = button_map[event.button]
            self.mouse_state.is_pressed[button] = False
            
            # Arrêter le drag
            if button == MouseButton.LEFT.value:
                self.mouse_state.is_dragging = False
                self.mouse_state.drag_start = None
    
    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        """Gère les événements de mouvement de souris"""
        # Mise à jour automatique via pygame.mouse.get_pos()
        pass
    
    def _create_click_effect(self, position: Tuple[int, int], button: str) -> None:
        """Crée un effet de clic selon le bouton pressé"""
        current_time = time.time()
        
        if button == MouseButton.LEFT.value:
            # Clic gauche -> effet d'ondulation
            effect = ClickEffect(
                position=position,
                effect_type=MouseInteractionType.RIPPLE,
                start_time=current_time,
                duration=1.5,
                max_radius=self.radius * 1.5,
                strength=self.strength
            )
        elif button == MouseButton.RIGHT.value:
            # Clic droit -> effet d'explosion
            effect = ClickEffect(
                position=position,
                effect_type=MouseInteractionType.BURST,
                start_time=current_time,
                duration=0.8,
                max_radius=self.radius * 0.8,
                strength=self.strength * 1.5
            )
        else:
            return  # Pas d'effet pour les autres boutons
        
        self.active_effects.append(effect)
    
    def _update_trail(self) -> None:
        """Met à jour la traînée de positions de la souris"""
        current_time = time.time()
        
        # Ajouter la position actuelle si elle a changé
        if self.mouse_state.position != self.mouse_state.prev_position:
            self.position_trail.append((self.mouse_state.position, current_time))
        
        # Limiter la longueur de la traînée
        if len(self.position_trail) > self.max_trail_length:
            self.position_trail.pop(0)
        
        # Supprimer les positions trop anciennes (> 2 secondes)
        cutoff_time = current_time - 2.0
        self.position_trail = [
            (pos, t) for pos, t in self.position_trail 
            if t > cutoff_time
        ]
    
    def _cleanup_expired_effects(self) -> None:
        """Supprime les effets expirés"""
        self.active_effects = [
            effect for effect in self.active_effects 
            if not effect.is_finished
        ]
    
    def calculate_mouse_force(self, square_pos: Tuple[float, float]) -> Tuple[float, float]:
        """
        Calcule la force exercée par la souris sur un carré.
        
        Args:
            square_pos: Position du carré (x, y)
            
        Returns:
            Tuple[force_x, force_y]: Force à appliquer au carré
        """
        if self.mouse_mode == MouseMode.DISABLED:
            return (0.0, 0.0)
        
        total_force_x = 0.0
        total_force_y = 0.0
        
        # Force de l'interaction principale (curseur)
        if (self.mouse_mode == MouseMode.CONTINUOUS or 
            (self.mouse_mode == MouseMode.HOVER and self._is_hovering())):
            
            force_x, force_y = self._calculate_interaction_force(
                square_pos, self.mouse_state.position, 
                self.interaction_type, self.strength
            )
            total_force_x += force_x
            total_force_y += force_y
        
        # Forces des effets de clic actifs
        for effect in self.active_effects:
            force_x, force_y = self._calculate_interaction_force(
                square_pos, effect.position, 
                effect.effect_type, effect.current_strength
            )
            total_force_x += force_x
            total_force_y += force_y
        
        return (total_force_x, total_force_y)
    
    def _calculate_interaction_force(self, 
                                   square_pos: Tuple[float, float],
                                   source_pos: Tuple[float, float],
                                   interaction_type: MouseInteractionType,
                                   strength: float) -> Tuple[float, float]:
        """Calcule la force d'interaction entre un carré et une source"""
        # Calculer la distance
        dx = square_pos[0] - source_pos[0]
        dy = square_pos[1] - source_pos[1]
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Éviter la division par zéro
        if distance < self.min_distance:
            return (0.0, 0.0)
        
        # Vérifier si dans le rayon d'influence
        if distance > self.radius:
            return (0.0, 0.0)
        
        # Calculer l'atténuation basée sur la distance
        falloff = 1.0 - (distance / self.radius) ** self.falloff_power
        
        # Direction normalisée
        norm_dx = dx / distance
        norm_dy = dy / distance
        
        # Force selon le type d'interaction
        if interaction_type in [MouseInteractionType.ATTRACTION, 
                               MouseInteractionType.RIPPLE]:
            # Attraction vers la source
            force_magnitude = -strength * falloff
        elif interaction_type in [MouseInteractionType.REPULSION, 
                                 MouseInteractionType.BURST]:
            # Répulsion depuis la source
            force_magnitude = strength * falloff
        else:
            force_magnitude = 0.0
        
        return (norm_dx * force_magnitude, norm_dy * force_magnitude)
    
    def _is_hovering(self) -> bool:
        """Vérifie si la souris survole actuellement la zone"""
        # Pour l'instant, considère toujours qu'on survole
        # Peut être étendu pour vérifier des zones spécifiques
        return True
    
    def get_visual_feedback_data(self) -> Dict[str, Any]:
        """
        Retourne les données pour le feedback visuel.
        
        Returns:
            Dictionnaire contenant les données de visualisation
        """
        if not self.show_feedback:
            return {}
        
        feedback_data = {
            'mouse_position': self.mouse_state.position,
            'interaction_radius': self.radius,
            'interaction_type': self.interaction_type,
            'active_effects': [
                {
                    'position': effect.position,
                    'type': effect.effect_type,
                    'radius': effect.current_radius,
                    'strength': effect.current_strength,
                    'progress': effect.progress
                }
                for effect in self.active_effects
            ],
            'trail': [pos for pos, _ in self.position_trail[-10:]]  # 10 dernières positions
        }
        
        return feedback_data
    
    # Méthodes de configuration
    def set_interaction_type(self, interaction_type: MouseInteractionType) -> None:
        """Change le type d'interaction principal"""
        self.interaction_type = interaction_type
    
    def set_mouse_mode(self, mouse_mode: MouseMode) -> None:
        """Change le mode de fonctionnement de la souris"""
        self.mouse_mode = mouse_mode
    
    def set_strength(self, strength: float) -> None:
        """Modifie la force d'interaction (0.0 à 1.0)"""
        self.strength = max(0.0, min(1.0, strength))
    
    def set_radius(self, radius: float) -> None:
        """Modifie le rayon d'influence"""
        self.radius = max(10.0, radius)
    
    def clear_effects(self) -> None:
        """Supprime tous les effets actifs"""
        self.active_effects.clear()
        self.position_trail.clear()