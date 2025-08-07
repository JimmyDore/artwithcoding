"""
Unit tests for mouse_interactions module.
"""

import pytest
import time
from unittest.mock import MagicMock, patch
import pygame

from distorsion_movement.enums import MouseInteractionType, MouseMode, MouseButton
from distorsion_movement.mouse_interactions import (
    MouseInteractionEngine, MouseState, ClickEffect
)


class TestMouseState:
    """Test cases for MouseState class."""
    
    def test_mouse_state_initialization(self):
        """Test that MouseState initializes with correct defaults."""
        state = MouseState()
        
        assert state.position == (0, 0)
        assert state.prev_position == (0, 0)
        assert state.is_dragging is False
        assert state.drag_start is None
        assert isinstance(state.is_pressed, dict)
        assert len(state.is_pressed) == 3
        assert state.is_pressed[MouseButton.LEFT.value] is False
        assert state.is_pressed[MouseButton.RIGHT.value] is False
        assert state.is_pressed[MouseButton.MIDDLE.value] is False
    
    def test_mouse_state_custom_initialization(self):
        """Test MouseState with custom initial values."""
        state = MouseState(
            position=(100, 200),
            prev_position=(90, 190),
            is_dragging=True,
            drag_start=(50, 60)
        )
        
        assert state.position == (100, 200)
        assert state.prev_position == (90, 190)
        assert state.is_dragging is True
        assert state.drag_start == (50, 60)


class TestClickEffect:
    """Test cases for ClickEffect class."""
    
    def test_click_effect_initialization(self):
        """Test that ClickEffect initializes correctly."""
        start_time = time.time()
        effect = ClickEffect(
            position=(100.0, 100.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=start_time,
            duration=1.0,
            max_radius=50.0,
            strength=0.7
        )
        
        assert effect.position == (100.0, 100.0)
        assert effect.effect_type == MouseInteractionType.RIPPLE
        assert effect.start_time == start_time
        assert effect.duration == 1.0
        assert effect.max_radius == 50.0
        assert effect.strength == 0.7
    
    def test_click_effect_progress_calculation(self):
        """Test progress calculation over time."""
        start_time = time.time()
        effect = ClickEffect(
            position=(0.0, 0.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=start_time,
            duration=1.0
        )
        
        # Initially should be near 0
        assert 0.0 <= effect.progress <= 0.1
        
        # After half duration, should be around 0.5
        effect.start_time = start_time - 0.5
        assert 0.4 <= effect.progress <= 0.6
        
        # After full duration, should be 1.0
        effect.start_time = start_time - 1.0
        assert effect.progress == 1.0
        
        # After more than duration, should be capped at 1.0
        effect.start_time = start_time - 2.0
        assert effect.progress == 1.0
    
    def test_click_effect_is_finished(self):
        """Test finished state detection."""
        start_time = time.time()
        effect = ClickEffect(
            position=(0.0, 0.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=start_time,
            duration=0.5
        )
        
        # Should not be finished initially
        assert not effect.is_finished
        
        # Should be finished after duration
        effect.start_time = start_time - 0.6
        assert effect.is_finished
    
    def test_click_effect_current_properties(self):
        """Test current radius and strength calculations."""
        start_time = time.time() - 0.5  # Half way through
        effect = ClickEffect(
            position=(0.0, 0.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=start_time,
            duration=1.0,
            max_radius=100.0,
            strength=1.0
        )
        
        # At 50% progress
        assert 45.0 <= effect.current_radius <= 55.0
        assert 0.45 <= effect.current_strength <= 0.55


class TestMouseInteractionEngine:
    """Test cases for MouseInteractionEngine class."""
    
    @pytest.fixture
    def engine(self):
        """Create a basic MouseInteractionEngine for testing."""
        return MouseInteractionEngine(
            interaction_type=MouseInteractionType.ATTRACTION,
            mouse_mode=MouseMode.CONTINUOUS,
            strength=0.5,
            radius=100.0
        )
    
    def test_engine_initialization(self, engine):
        """Test that MouseInteractionEngine initializes correctly."""
        assert engine.interaction_type == MouseInteractionType.ATTRACTION
        assert engine.mouse_mode == MouseMode.CONTINUOUS
        assert engine.strength == 0.5
        assert engine.radius == 100.0
        assert engine.show_feedback is True
        assert isinstance(engine.mouse_state, MouseState)
        assert len(engine.active_effects) == 0
        assert len(engine.position_trail) == 0
    
    def test_engine_configuration_methods(self, engine):
        """Test configuration setter methods."""
        # Test interaction type change
        engine.set_interaction_type(MouseInteractionType.REPULSION)
        assert engine.interaction_type == MouseInteractionType.REPULSION
        
        # Test mouse mode change
        engine.set_mouse_mode(MouseMode.CLICK_ONLY)
        assert engine.mouse_mode == MouseMode.CLICK_ONLY
        
        # Test strength change
        engine.set_strength(0.8)
        assert engine.strength == 0.8
        
        # Test strength bounds
        engine.set_strength(1.5)  # Should be capped at 1.0
        assert engine.strength == 1.0
        
        engine.set_strength(-0.5)  # Should be capped at 0.0
        assert engine.strength == 0.0
        
        # Test radius change
        engine.set_radius(150.0)
        assert engine.radius == 150.0
        
        # Test radius minimum
        engine.set_radius(5.0)  # Should be at least 10.0
        assert engine.radius == 10.0
    
    def test_force_calculation_basic(self, engine):
        """Test basic force calculations."""
        # Set mouse position
        engine.mouse_state.position = (0, 0)
        
        # Test force at mouse position (should be 0 due to min_distance)
        force = engine.calculate_mouse_force((0.0, 0.0))
        assert force == (0.0, 0.0)
        
        # Test force at distance 50 (within radius)
        force = engine.calculate_mouse_force((50.0, 0.0))
        assert force[0] < 0  # Attraction should pull towards mouse (negative)
        assert force[1] == 0.0
        
        # Test force outside radius
        force = engine.calculate_mouse_force((150.0, 0.0))
        assert force == (0.0, 0.0)
    
    def test_force_calculation_repulsion(self):
        """Test repulsion force calculations."""
        engine = MouseInteractionEngine(
            interaction_type=MouseInteractionType.REPULSION,
            strength=1.0,
            radius=100.0
        )
        engine.mouse_state.position = (0, 0)
        
        # Test repulsion force
        force = engine.calculate_mouse_force((50.0, 0.0))
        assert force[0] > 0  # Repulsion should push away from mouse (positive)
        assert force[1] == 0.0
    
    def test_force_calculation_disabled_mode(self, engine):
        """Test that disabled mode returns zero forces."""
        engine.set_mouse_mode(MouseMode.DISABLED)
        engine.mouse_state.position = (0, 0)
        
        force = engine.calculate_mouse_force((50.0, 0.0))
        assert force == (0.0, 0.0)
    
    @patch('pygame.event.Event')
    def test_mouse_button_down_handling(self, mock_event, engine):
        """Test mouse button down event handling."""
        # Create mock event
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 1  # Left button
        mock_event.pos = (100, 100)
        
        initial_effects = len(engine.active_effects)
        engine._handle_mouse_button_down(mock_event)
        
        # Should have created a new effect
        assert len(engine.active_effects) == initial_effects + 1
        assert engine.mouse_state.is_pressed[MouseButton.LEFT.value] is True
        assert engine.mouse_state.is_dragging is True
        assert engine.mouse_state.drag_start == (100, 100)
    
    @patch('pygame.event.Event')
    def test_mouse_button_up_handling(self, mock_event, engine):
        """Test mouse button up event handling."""
        # First press the button
        engine.mouse_state.is_pressed[MouseButton.LEFT.value] = True
        engine.mouse_state.is_dragging = True
        engine.mouse_state.drag_start = (50, 50)
        
        # Create mock release event
        mock_event.type = pygame.MOUSEBUTTONUP
        mock_event.button = 1  # Left button
        
        engine._handle_mouse_button_up(mock_event)
        
        assert engine.mouse_state.is_pressed[MouseButton.LEFT.value] is False
        assert engine.mouse_state.is_dragging is False
        assert engine.mouse_state.drag_start is None
    
    def test_click_effect_creation(self, engine):
        """Test click effect creation for different buttons."""
        initial_count = len(engine.active_effects)
        
        # Test left click (should create ripple)
        engine._create_click_effect((100, 100), MouseButton.LEFT.value)
        assert len(engine.active_effects) == initial_count + 1
        assert engine.active_effects[-1].effect_type == MouseInteractionType.RIPPLE
        
        # Test right click (should create burst)
        engine._create_click_effect((200, 200), MouseButton.RIGHT.value)
        assert len(engine.active_effects) == initial_count + 2
        assert engine.active_effects[-1].effect_type == MouseInteractionType.BURST
        
        # Test middle click (should not create effect)
        engine._create_click_effect((300, 300), MouseButton.MIDDLE.value)
        assert len(engine.active_effects) == initial_count + 2
    
    def test_trail_update(self, engine):
        """Test mouse trail updating."""
        # Simulate mouse movement
        engine.mouse_state.prev_position = (0, 0)
        engine.mouse_state.position = (10, 10)
        
        initial_trail_length = len(engine.position_trail)
        engine._update_trail()
        
        # Should have added position to trail
        assert len(engine.position_trail) == initial_trail_length + 1
        assert engine.position_trail[-1][0] == (10, 10)
    
    def test_effects_cleanup(self, engine):
        """Test expired effects cleanup."""
        # Add an expired effect
        old_time = time.time() - 10.0
        expired_effect = ClickEffect(
            position=(0.0, 0.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=old_time,
            duration=1.0
        )
        engine.active_effects.append(expired_effect)
        
        # Add a current effect
        current_effect = ClickEffect(
            position=(0.0, 0.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=time.time(),
            duration=1.0
        )
        engine.active_effects.append(current_effect)
        
        assert len(engine.active_effects) == 2
        engine._cleanup_expired_effects()
        
        # Should have removed only the expired effect
        assert len(engine.active_effects) == 1
        assert engine.active_effects[0] == current_effect
    
    def test_clear_effects(self, engine):
        """Test clearing all effects."""
        # Add some effects
        engine.active_effects.append(ClickEffect(
            position=(0.0, 0.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=time.time()
        ))
        engine.position_trail.append(((100, 100), time.time()))
        
        engine.clear_effects()
        
        assert len(engine.active_effects) == 0
        assert len(engine.position_trail) == 0
    
    def test_visual_feedback_data(self, engine):
        """Test visual feedback data generation."""
        # Set up some data
        engine.mouse_state.position = (150, 200)
        engine.active_effects.append(ClickEffect(
            position=(100.0, 100.0),
            effect_type=MouseInteractionType.RIPPLE,
            start_time=time.time()
        ))
        engine.position_trail.append(((120, 130), time.time()))
        
        feedback = engine.get_visual_feedback_data()
        
        assert 'mouse_position' in feedback
        assert feedback['mouse_position'] == (150, 200)
        assert 'interaction_radius' in feedback
        assert feedback['interaction_radius'] == engine.radius
        assert 'interaction_type' in feedback
        assert feedback['interaction_type'] == engine.interaction_type
        assert 'active_effects' in feedback
        assert len(feedback['active_effects']) == 1
        assert 'trail' in feedback
    
    def test_visual_feedback_disabled(self):
        """Test that visual feedback can be disabled."""
        engine = MouseInteractionEngine(show_feedback=False)
        feedback = engine.get_visual_feedback_data()
        
        assert feedback == {}


class TestMouseInteractionIntegration:
    """Integration tests for mouse interactions."""
    
    @pytest.mark.integration
    def test_full_interaction_cycle(self):
        """Test a complete interaction cycle."""
        engine = MouseInteractionEngine(
            interaction_type=MouseInteractionType.ATTRACTION,
            strength=0.8,
            radius=100.0
        )
        
        # Simulate mouse movement and click
        engine.mouse_state.position = (50, 50)
        
        # Create a click effect
        engine._create_click_effect((50, 50), MouseButton.LEFT.value)
        
        # Calculate forces for nearby squares
        test_positions = [
            (0.0, 0.0),    # Close to mouse
            (25.0, 25.0),  # Medium distance
            (75.0, 75.0),  # Edge of range
            (150.0, 150.0) # Outside range
        ]
        
        forces = [engine.calculate_mouse_force(pos) for pos in test_positions]
        
        # Verify force characteristics
        assert forces[0] != (0.0, 0.0)  # Should have force
        assert forces[1] != (0.0, 0.0)  # Should have force
        assert forces[2] != (0.0, 0.0)  # Should have force (from click effect)
        assert forces[3] == (0.0, 0.0)  # Should have no force (too far)
        
        # Verify effects are working
        assert len(engine.active_effects) == 1
        assert not engine.active_effects[0].is_finished
    
    @pytest.mark.integration 
    def test_multiple_effects_combination(self):
        """Test combining multiple click effects."""
        engine = MouseInteractionEngine()
        
        # Create multiple effects
        engine._create_click_effect((0, 0), MouseButton.LEFT.value)
        engine._create_click_effect((100, 0), MouseButton.RIGHT.value)
        
        assert len(engine.active_effects) == 2
        
        # Test force at midpoint (should be affected by both)
        force = engine.calculate_mouse_force((50.0, 0.0))
        assert force != (0.0, 0.0)
    
    @pytest.mark.unit
    def test_force_calculation_edge_cases(self):
        """Test edge cases in force calculations."""
        engine = MouseInteractionEngine(radius=100.0, strength=1.0)
        engine.mouse_state.position = (0, 0)
        
        # Test exactly at boundary
        force = engine.calculate_mouse_force((100.0, 0.0))
        assert force == (0.0, 0.0)  # Should be zero at exact boundary
        
        # Test just inside boundary
        force = engine.calculate_mouse_force((99.0, 0.0))
        assert force != (0.0, 0.0)  # Should have some force
        
        # Test very close to mouse (min_distance protection)
        force = engine.calculate_mouse_force((0.5, 0.0))
        assert force == (0.0, 0.0)  # Should be zero due to min_distance