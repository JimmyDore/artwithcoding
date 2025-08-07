"""
Unit tests for enums module.
"""

import pytest
from distorsion_movement.enums import DistortionType, ColorScheme, ShapeType


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


class TestShapeType:
    """Test cases for ShapeType enum."""
    
    def test_shape_type_values(self):
        """Test that all shape types have correct values."""
        assert ShapeType.SQUARE.value == "square"
        assert ShapeType.CIRCLE.value == "circle"
        assert ShapeType.TRIANGLE.value == "triangle"
        assert ShapeType.HEXAGON.value == "hexagon"
        assert ShapeType.STAR.value == "star"
        assert ShapeType.PENTAGON.value == "pentagon"
        assert ShapeType.DIAMOND.value == "diamond"
    
    def test_shape_type_count(self):
        """Test that we have the expected number of shape types."""
        assert len(ShapeType) == 7
    
    def test_shape_type_iteration(self):
        """Test that we can iterate over all shape types."""
        shapes = list(ShapeType)
        assert len(shapes) == 7
        assert ShapeType.SQUARE in shapes
        assert ShapeType.CIRCLE in shapes
        assert ShapeType.TRIANGLE in shapes
        assert ShapeType.HEXAGON in shapes
        assert ShapeType.STAR in shapes
        assert ShapeType.PENTAGON in shapes
        assert ShapeType.DIAMOND in shapes
    
    def test_shape_type_default(self):
        """Test that SQUARE is available as default shape."""
        assert ShapeType.SQUARE in list(ShapeType)
        assert ShapeType.SQUARE.value == "square"