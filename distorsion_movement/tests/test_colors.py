"""
Unit tests for colors module.
"""

import pytest
import math
from distorsion_movement.colors import ColorGenerator
from distorsion_movement.enums import ColorScheme


class TestColorGenerator:
    """Test cases for ColorGenerator class."""
    
    def test_get_color_monochrome(self):
        """Test monochrome color scheme returns the base color."""
        base_color = (255, 128, 64)
        color = ColorGenerator.get_color_for_position(
            ColorScheme.MONOCHROME.value, base_color, 0.5, 0.5, 0.5, 10, 64
        )
        assert color == base_color
    
    def test_get_color_gradient(self):
        """Test gradient color scheme."""
        base_color = (255, 255, 255)
        
        # Test corner positions
        color_top_left = ColorGenerator.get_color_for_position(
            ColorScheme.GRADIENT.value, base_color, 0.0, 0.0, 0.0, 0, 64
        )
        color_bottom_right = ColorGenerator.get_color_for_position(
            ColorScheme.GRADIENT.value, base_color, 1.0, 1.0, 1.0, 63, 64
        )
        
        # Colors should be different
        assert color_top_left != color_bottom_right
        
        # Check RGB values are in valid range
        for color in [color_top_left, color_bottom_right]:
            r, g, b = color
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255
    
    def test_get_color_rainbow(self):
        """Test rainbow color scheme."""
        base_color = (255, 255, 255)
        
        # Test different positions
        colors = []
        for i in range(5):
            x_norm = i / 4.0
            y_norm = 0.5
            color = ColorGenerator.get_color_for_position(
                ColorScheme.RAINBOW.value, base_color, x_norm, y_norm, 0.5, i, 64
            )
            colors.append(color)
            
            # Check RGB values are in valid range
            r, g, b = color
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255
        
        # Colors should be different across the spectrum
        assert len(set(colors)) > 1
    
    def test_get_color_complementary(self):
        """Test complementary color scheme."""
        base_color = (255, 255, 255)
        
        color1 = ColorGenerator.get_color_for_position(
            ColorScheme.COMPLEMENTARY.value, base_color, 0.0, 0.0, 0.0, 0, 64
        )
        color2 = ColorGenerator.get_color_for_position(
            ColorScheme.COMPLEMENTARY.value, base_color, 1.0, 1.0, 1.0, 63, 64
        )
        
        # Colors should be different
        assert color1 != color2
        
        # Check RGB values are in valid range
        for color in [color1, color2]:
            r, g, b = color
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255
    
    def test_get_color_temperature(self):
        """Test temperature color scheme."""
        base_color = (255, 255, 255)
        
        # Test cold (center) vs hot (edge) positions
        color_center = ColorGenerator.get_color_for_position(
            ColorScheme.TEMPERATURE.value, base_color, 0.5, 0.5, 0.0, 32, 64
        )
        color_edge = ColorGenerator.get_color_for_position(
            ColorScheme.TEMPERATURE.value, base_color, 0.0, 0.0, 1.0, 0, 64
        )
        
        # Colors should be different
        assert color_center != color_edge
        
        # Check RGB values are in valid range
        for color in [color_center, color_edge]:
            r, g, b = color
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255
    
    @pytest.mark.parametrize("color_scheme", [
        ColorScheme.PASTEL.value,
        ColorScheme.NEON.value,
        ColorScheme.MONOCHROME.value,
        ColorScheme.BLACK_WHITE_RADIAL.value,
    ])
    def test_all_color_schemes_return_valid_rgb(self, color_scheme):
        """Test that all color schemes return valid RGB values."""
        base_color = (255, 255, 255)
        
        # Test multiple positions
        for x_norm in [0.0, 0.5, 1.0]:
            for y_norm in [0.0, 0.5, 1.0]:
                distance_to_center = math.sqrt((x_norm - 0.5)**2 + (y_norm - 0.5)**2)
                index = int(x_norm * 64 + y_norm * 64 * 64)
                
                color = ColorGenerator.get_color_for_position(
                    color_scheme, base_color, x_norm, y_norm, 
                    distance_to_center, index, 64
                )
                
                # Check that color is a tuple of 3 integers
                assert isinstance(color, tuple)
                assert len(color) == 3
                
                r, g, b = color
                assert isinstance(r, int)
                assert isinstance(g, int)
                assert isinstance(b, int)
                assert 0 <= r <= 255
                assert 0 <= g <= 255
                assert 0 <= b <= 255
    
    def test_color_consistency(self):
        """Test that same inputs produce same colors."""
        base_color = (128, 128, 128)
        x_norm, y_norm = 0.3, 0.7
        distance_to_center = 0.5
        index = 20
        dimension = 64
        
        color1 = ColorGenerator.get_color_for_position(
            ColorScheme.RAINBOW.value, base_color, x_norm, y_norm, 
            distance_to_center, index, dimension
        )
        color2 = ColorGenerator.get_color_for_position(
            ColorScheme.RAINBOW.value, base_color, x_norm, y_norm, 
            distance_to_center, index, dimension
        )
        
        assert color1 == color2
    
    def test_color_variation_by_position(self):
        """Test that different positions produce different colors for most schemes."""
        base_color = (128, 128, 128)
        
        # Test schemes that should vary by position (excluding monochrome)
        varying_schemes = [
            ColorScheme.GRADIENT.value,
            ColorScheme.RAINBOW.value,
            ColorScheme.COMPLEMENTARY.value,
            ColorScheme.TEMPERATURE.value
        ]
        
        for scheme in varying_schemes:
            color1 = ColorGenerator.get_color_for_position(
                scheme, base_color, 0.0, 0.0, 0.0, 0, 64
            )
            color2 = ColorGenerator.get_color_for_position(
                scheme, base_color, 1.0, 1.0, 1.0, 63, 64
            )
            
            # Colors should be different for different positions
            assert color1 != color2, f"Scheme {scheme} should vary by position"
    
    def test_edge_cases(self):
        """Test edge cases and boundary values."""
        base_color = (0, 0, 0)
        
        # Test with extreme values
        color = ColorGenerator.get_color_for_position(
            ColorScheme.RAINBOW.value, base_color, 0.0, 0.0, 0.0, 0, 1
        )
        
        assert isinstance(color, tuple)
        assert len(color) == 3
        r, g, b = color
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255
        
        # Test with maximum values
        color = ColorGenerator.get_color_for_position(
            ColorScheme.RAINBOW.value, base_color, 1.0, 1.0, 1.0, 999, 1000
        )
        
        assert isinstance(color, tuple)
        assert len(color) == 3
        r, g, b = color
        assert 0 <= r <= 255
        assert 0 <= g <= 255
        assert 0 <= b <= 255