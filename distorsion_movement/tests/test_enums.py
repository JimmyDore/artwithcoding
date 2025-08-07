"""
Unit tests for enums module.
"""

import pytest
from distorsion_movement.enums import DistortionType, ColorScheme


class TestDistortionType:
    """Test cases for DistortionType enum."""
    
    def test_distortion_type_values(self):
        """Test that all distortion types have correct values."""
        assert DistortionType.RANDOM.value == "random"
        assert DistortionType.SINE.value == "sine"
        assert DistortionType.PERLIN.value == "perlin"
        assert DistortionType.CIRCULAR.value == "circular"
    
    def test_distortion_type_count(self):
        """Test that we have the expected number of distortion types."""
        assert len(DistortionType) == 4
    
    def test_distortion_type_iteration(self):
        """Test that we can iterate over all distortion types."""
        types = list(DistortionType)
        assert len(types) == 4
        assert DistortionType.RANDOM in types
        assert DistortionType.SINE in types
        assert DistortionType.PERLIN in types
        assert DistortionType.CIRCULAR in types


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