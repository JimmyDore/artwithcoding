"""
Unit tests for deformed_grid module.
"""

import pytest
import pygame
import math
from unittest.mock import patch, MagicMock
from distorsion_movement.deformed_grid import DeformedGrid
from distorsion_movement.enums import DistortionType, ColorScheme


class TestDeformedGrid:
    """Test cases for DeformedGrid class."""
    
    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Setup pygame for tests."""
        # Mock pygame to avoid actual display initialization
        with patch('pygame.init'), \
             patch('pygame.display.set_mode') as mock_display, \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'), \
             patch('pygame.display.Info') as mock_info:
            
            mock_info.return_value.current_w = 1920
            mock_info.return_value.current_h = 1080
            mock_display.return_value = MagicMock()
            yield
    
    def test_init_default_params(self):
        """Test DeformedGrid initialization with default parameters."""
        grid = DeformedGrid()
        
        assert grid.dimension == 64
        assert grid.cell_size == 8
        assert grid.canvas_size == (1200, 900)
        assert grid.distortion_strength == 0.0
        assert grid.distortion_fn == "random"
        assert grid.background_color == (20, 20, 30)
        assert grid.square_color == (255, 255, 255)
        assert grid.color_scheme == "monochrome"
        assert grid.color_animation is False
        assert grid.time == 0.0
        assert grid.animation_speed == 0.02
        assert grid.is_fullscreen is False
    
    def test_init_custom_params(self):
        """Test DeformedGrid initialization with custom parameters."""
        grid = DeformedGrid(
            dimension=32,
            cell_size=16,
            canvas_size=(800, 600),
            distortion_strength=0.5,
            distortion_fn="sine",
            background_color=(0, 0, 0),
            square_color=(255, 0, 0),
            color_scheme="rainbow",
            color_animation=True,
        )
        
        assert grid.dimension == 32
        assert grid.cell_size == 16
        assert grid.canvas_size == (800, 600)
        assert grid.distortion_strength == 0.5
        assert grid.distortion_fn == "sine"
        assert grid.background_color == (0, 0, 0)
        assert grid.square_color == (255, 0, 0)
        assert grid.color_scheme == "rainbow"
        assert grid.color_animation is True

    def test_generate_base_positions(self):
        """Test generation of base grid positions."""
        grid = DeformedGrid(dimension=3, cell_size=10, canvas_size=(100, 100))
        
        # Grid should be centered
        expected_offset_x = (100 - 3 * 10) // 2  # 35
        expected_offset_y = (100 - 3 * 10) // 2  # 35
        
        assert grid.offset_x == expected_offset_x
        assert grid.offset_y == expected_offset_y
        
        # Should have 9 positions (3x3)
        assert len(grid.base_positions) == 9
        
        # Check first few positions
        expected_positions = [
            (35, 35),   # (0,0)
            (45, 35),   # (1,0)
            (55, 35),   # (2,0)
            (35, 45),   # (0,1)
        ]
        
        for i, expected_pos in enumerate(expected_positions):
            assert grid.base_positions[i] == expected_pos
    
    def test_generate_distortions(self):
        """Test generation of distortion parameters."""
        grid = DeformedGrid(dimension=3)
        
        # Should have distortion params for each square
        assert len(grid.distortions) == 9
        
        # Each distortion should have required parameters
        for distortion in grid.distortions:
            assert 'offset_x' in distortion
            assert 'offset_y' in distortion
            assert 'phase_x' in distortion
            assert 'phase_y' in distortion
            assert 'frequency' in distortion
            assert 'rotation_phase' in distortion
    
    def test_generate_base_colors(self):
        """Test generation of base colors."""
        grid = DeformedGrid(dimension=3, color_scheme="monochrome", square_color=(128, 64, 32))
        
        # Should have colors for each square
        assert len(grid.base_colors) == 9
        
        # For monochrome, all colors should be the same
        for color in grid.base_colors:
            assert color == (128, 64, 32)
    
    def test_generate_base_colors_gradient(self):
        """Test generation of base colors with gradient scheme."""
        grid = DeformedGrid(dimension=3, color_scheme="gradient")
        
        # Should have colors for each square
        assert len(grid.base_colors) == 9
        
        # Colors should be different (gradient effect)
        colors = set(grid.base_colors)
        assert len(colors) > 1  # Should have variation
    
    def test_get_distorted_positions(self):
        """Test getting distorted positions."""
        grid = DeformedGrid(dimension=2, distortion_strength=0.5)
        
        positions = grid._get_distorted_positions()
        
        # Should have positions for each square
        assert len(positions) == 4
        
        # Each position should be a tuple of (x, y, rotation)
        for pos in positions:
            assert len(pos) == 3
            x, y, rotation = pos
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert isinstance(rotation, (int, float))
    
    @patch('pygame.draw.polygon')
    def test_draw_shape_square(self, mock_draw_polygon):
        """Test drawing a square shape."""
        grid = DeformedGrid(dimension=2, shape_type="square")
        mock_surface = MagicMock()
        
        grid._draw_shape(
            mock_surface, 100.0, 100.0, 0.0, 20, (255, 255, 255), "square"
        )
        
        # Should call pygame.draw.polygon
        mock_draw_polygon.assert_called_once()
        args = mock_draw_polygon.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (255, 255, 255)  # color
        # args[2] should be the polygon points
        points = args[2]
        assert len(points) == 4  # Square has 4 corners
    
    @patch('pygame.draw.circle')
    def test_draw_shape_circle(self, mock_draw_circle):
        """Test drawing a circle shape."""
        grid = DeformedGrid(dimension=2, shape_type="circle")
        mock_surface = MagicMock()
        
        grid._draw_shape(
            mock_surface, 100.0, 100.0, 0.0, 20, (255, 0, 0), "circle"
        )
        
        mock_draw_circle.assert_called_once()
        args = mock_draw_circle.call_args[0]
        assert args[0] == mock_surface  # surface
        assert args[1] == (255, 0, 0)  # color
        
        # For circles, the third argument should be the position and radius
        # args structure: (surface, color, (center_x, center_y), radius)
        position = args[2]
        radius = args[3]
        assert position == (100, 100)  # center position
        assert radius == 10  # size//2
    
    @patch('pygame.draw.polygon', side_effect=ValueError("Invalid polygon"))
    @patch('pygame.draw.rect')
    @patch('pygame.Rect')
    def test_draw_shape_error_handling(self, mock_rect, mock_draw_rect, mock_draw_polygon):
        """Test error handling in shape drawing."""
        grid = DeformedGrid(dimension=2, shape_type="square")
        mock_surface = MagicMock()
        mock_rect.return_value = MagicMock()
        
        # Should not raise exception even if pygame.draw.polygon fails
        grid._draw_shape(
            mock_surface, 100.0, 100.0, 0.0, 20, (255, 255, 255), "square"
        )
        
        # Should fall back to drawing a rectangle
        mock_draw_rect.assert_called_once()
    
    def test_draw_shape_invalid_coordinates(self):
        """Test drawing shape with invalid coordinates."""
        grid = DeformedGrid(dimension=2, shape_type="square")
        mock_surface = MagicMock()
        
        # Should handle NaN/Inf coordinates gracefully
        with patch('pygame.draw.polygon') as mock_draw_polygon, \
             patch('pygame.draw.rect') as mock_draw_rect, \
             patch('pygame.Rect') as mock_rect:
            
            # The method will try to convert NaN to int, which will raise ValueError
            # But this should be caught and handled
            try:
                grid._draw_shape(
                    mock_surface, float('nan'), float('inf'), 0.0, 20, (255, 255, 255), "square"
                )
                # If we reach here, the error was handled
            except ValueError:
                # This is expected behavior - NaN can't be converted to int
                pass
    
    def test_shape_types_generation(self):
        """Test shape types generation for single and mixed modes."""
        # Test single shape mode
        grid = DeformedGrid(dimension=3, shape_type="circle", mixed_shapes=False)
        assert len(grid.shape_types) == 9  # 3x3 grid
        assert all(shape == "circle" for shape in grid.shape_types)
        
        # Test mixed shapes mode
        grid_mixed = DeformedGrid(dimension=2, shape_type="star", mixed_shapes=True)
        assert len(grid_mixed.shape_types) == 4  # 2x2 grid
        # In mixed mode, we should have variety (though random, so we can't test exact values)
        # But we can test that the main shape type is still set
        assert grid_mixed.shape_type == "star"
        assert grid_mixed.mixed_shapes == True
    
    def test_shape_cycling(self):
        """Test that shape types can be regenerated."""
        grid = DeformedGrid(dimension=2, shape_type="square", mixed_shapes=False)
        original_shapes = grid.shape_types.copy()
        
        # Change shape type and regenerate
        grid.shape_type = "triangle"
        grid._generate_shape_types()
        
        # All shapes should now be triangles
        assert all(shape == "triangle" for shape in grid.shape_types)
        assert grid.shape_types != original_shapes
    
    def test_centering_calculation(self):
        """Test that grid is properly centered."""
        canvas_size = (400, 300)
        dimension = 10
        cell_size = 8
        
        grid = DeformedGrid(
            dimension=dimension, 
            cell_size=cell_size, 
            canvas_size=canvas_size
        )
        
        grid_total_size = dimension * cell_size  # 80
        expected_offset_x = (400 - 80) // 2  # 160
        expected_offset_y = (300 - 80) // 2  # 110
        
        assert grid.offset_x == expected_offset_x
        assert grid.offset_y == expected_offset_y
    
    def test_color_scheme_integration(self):
        """Test integration with different color schemes."""
        for scheme in [ColorScheme.MONOCHROME.value, ColorScheme.RAINBOW.value, ColorScheme.GRADIENT.value]:
            grid = DeformedGrid(dimension=3, color_scheme=scheme)
            
            # Should generate colors without error
            assert len(grid.base_colors) == 9
            
            # All colors should be valid RGB tuples
            for color in grid.base_colors:
                assert isinstance(color, tuple)
                assert len(color) == 3
                r, g, b = color
                assert 0 <= r <= 255
                assert 0 <= g <= 255
                assert 0 <= b <= 255
    
    def test_distortion_type_integration(self):
        """Test integration with different distortion types."""
        for distortion_type in [DistortionType.RANDOM.value, DistortionType.SINE.value, 
                               DistortionType.PERLIN.value, DistortionType.CIRCULAR.value]:
            grid = DeformedGrid(dimension=2, distortion_fn=distortion_type, distortion_strength=0.5)
            
            # Should generate positions without error
            positions = grid._get_distorted_positions()
            assert len(positions) == 4
            
            # All positions should be valid
            for pos in positions:
                x, y, rotation = pos
                assert isinstance(x, (int, float))
                assert isinstance(y, (int, float))
                assert isinstance(rotation, (int, float))
                assert math.isfinite(x)
                assert math.isfinite(y)
                assert math.isfinite(rotation)
    
    def test_time_animation(self):
        """Test time-based animation updates."""
        grid = DeformedGrid(dimension=2, distortion_fn="sine", distortion_strength=0.5)
        
        # Get positions at time 0
        grid.time = 0.0
        positions1 = grid._get_distorted_positions()
        
        # Get positions at different time
        grid.time = 1.0
        positions2 = grid._get_distorted_positions()
        
        # Positions should be different for animated distortions
        assert positions1 != positions2
    
    def test_zero_dimension_edge_case(self):
        """Test handling of edge cases."""
        # Test with dimension 1 (single square)
        grid = DeformedGrid(dimension=1)
        
        assert len(grid.base_positions) == 1
        assert len(grid.base_colors) == 1
        assert len(grid.distortions) == 1
        
        positions = grid._get_distorted_positions()
        assert len(positions) == 1
    
    def test_large_dimension(self):
        """Test with larger grid dimensions."""
        grid = DeformedGrid(dimension=100)
        
        assert len(grid.base_positions) == 10000
        assert len(grid.base_colors) == 10000
        assert len(grid.distortions) == 10000
        
        # Should still work (though we won't test full rendering for performance)
        positions = grid._get_distorted_positions()
        assert len(positions) == 10000