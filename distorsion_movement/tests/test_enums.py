"""
Unit tests for enums module.
"""

import pytest
from distorsion_movement.enums import (
    DistortionType, ColorScheme, MouseInteractionType, MouseMode, MouseButton
)


class TestDistortionType:
    """Test cases for DistortionType enum."""
    
    def test_distortion_type_values(self):
        """Test that all distortion types have correct values."""
        assert DistortionType.RANDOM.value == "random"
        assert DistortionType.SINE.value == "sine"
        assert DistortionType.PERLIN.value == "perlin"
        assert DistortionType.CIRCULAR.value == "circular"
        assert DistortionType.MOUSE_ATTRACTION.value == "mouse_attraction"
        assert DistortionType.MOUSE_REPULSION.value == "mouse_repulsion"
    
    def test_distortion_type_count(self):
        """Test that we have the expected number of distortion types."""
        assert len(DistortionType) == 6
    
    def test_distortion_type_iteration(self):
        """Test that we can iterate over all distortion types."""
        types = list(DistortionType)
        assert len(types) == 6
        assert DistortionType.RANDOM in types
        assert DistortionType.SINE in types
        assert DistortionType.PERLIN in types
        assert DistortionType.CIRCULAR in types
        assert DistortionType.MOUSE_ATTRACTION in types
        assert DistortionType.MOUSE_REPULSION in types


class TestColorScheme:
    """Test cases for ColorScheme enum."""
    
    def test_color_scheme_values(self):
        """Test that all color schemes have correct values."""
        assert ColorScheme.MONOCHROME.value == "monochrome"
        assert ColorScheme.GRADIENT.value == "gradient"
        assert ColorScheme.RAINBOW.value == "rainbow"
        assert ColorScheme.COMPLEMENTARY.value == "complementary"
        assert ColorScheme.TEMPERATURE.value == "temperature"
        assert ColorScheme.PASTEL.value == "pastel"
        assert ColorScheme.NEON.value == "neon"
        assert ColorScheme.OCEAN.value == "ocean"
        assert ColorScheme.FIRE.value == "fire"
        assert ColorScheme.FOREST.value == "forest"
    
    def test_color_scheme_count(self):
        """Test that we have the expected number of color schemes."""
        assert len(ColorScheme) == 10
    
    def test_color_scheme_iteration(self):
        """Test that we can iterate over all color schemes."""
        schemes = list(ColorScheme)
        assert len(schemes) == 10
        assert ColorScheme.MONOCHROME in schemes
        assert ColorScheme.RAINBOW in schemes
        assert ColorScheme.NEON in schemes


class TestMouseInteractionType:
    """Test cases for MouseInteractionType enum."""
    
    def test_mouse_interaction_type_values(self):
        """Test that all mouse interaction types have correct values."""
        assert MouseInteractionType.ATTRACTION.value == "attraction"
        assert MouseInteractionType.REPULSION.value == "repulsion"
        assert MouseInteractionType.RIPPLE.value == "ripple"
        assert MouseInteractionType.BURST.value == "burst"
        assert MouseInteractionType.TRAIL.value == "trail"
        assert MouseInteractionType.DRAG.value == "drag"
        assert MouseInteractionType.NONE.value == "none"
    
    def test_mouse_interaction_type_count(self):
        """Test that we have the expected number of mouse interaction types."""
        assert len(MouseInteractionType) == 7
    
    def test_mouse_interaction_type_iteration(self):
        """Test that we can iterate over all mouse interaction types."""
        types = list(MouseInteractionType)
        assert len(types) == 7
        assert MouseInteractionType.ATTRACTION in types
        assert MouseInteractionType.REPULSION in types
        assert MouseInteractionType.RIPPLE in types
        assert MouseInteractionType.BURST in types
        assert MouseInteractionType.TRAIL in types
        assert MouseInteractionType.DRAG in types
        assert MouseInteractionType.NONE in types


class TestMouseMode:
    """Test cases for MouseMode enum."""
    
    def test_mouse_mode_values(self):
        """Test that all mouse modes have correct values."""
        assert MouseMode.CONTINUOUS.value == "continuous"
        assert MouseMode.CLICK_ONLY.value == "click_only"
        assert MouseMode.HOVER.value == "hover"
        assert MouseMode.DISABLED.value == "disabled"
    
    def test_mouse_mode_count(self):
        """Test that we have the expected number of mouse modes."""
        assert len(MouseMode) == 4
    
    def test_mouse_mode_iteration(self):
        """Test that we can iterate over all mouse modes."""
        modes = list(MouseMode)
        assert len(modes) == 4
        assert MouseMode.CONTINUOUS in modes
        assert MouseMode.CLICK_ONLY in modes
        assert MouseMode.HOVER in modes
        assert MouseMode.DISABLED in modes


class TestMouseButton:
    """Test cases for MouseButton enum."""
    
    def test_mouse_button_values(self):
        """Test that all mouse buttons have correct values."""
        assert MouseButton.LEFT.value == "left"
        assert MouseButton.RIGHT.value == "right"
        assert MouseButton.MIDDLE.value == "middle"
        assert MouseButton.WHEEL_UP.value == "wheel_up"
        assert MouseButton.WHEEL_DOWN.value == "wheel_down"
    
    def test_mouse_button_count(self):
        """Test that we have the expected number of mouse buttons."""
        assert len(MouseButton) == 5
    
    def test_mouse_button_iteration(self):
        """Test that we can iterate over all mouse buttons."""
        buttons = list(MouseButton)
        assert len(buttons) == 5
        assert MouseButton.LEFT in buttons
        assert MouseButton.RIGHT in buttons
        assert MouseButton.MIDDLE in buttons
        assert MouseButton.WHEEL_UP in buttons
        assert MouseButton.WHEEL_DOWN in buttons