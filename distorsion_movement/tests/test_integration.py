"""
Integration tests for the distorsion_movement package.
"""

import pytest
import pygame
from unittest.mock import patch, MagicMock
from distorsion_movement import (
    DeformedGrid, DistortionType, ColorScheme, AudioAnalyzer,
    ColorGenerator, DistortionEngine, create_deformed_grid
)
from distorsion_movement.demos import quick_demo


@pytest.mark.integration
class TestPackageIntegration:
    """Test integration between different modules."""
    
    @pytest.fixture(autouse=True)
    def setup_pygame(self):
        """Setup pygame for tests."""
        with patch('pygame.init'), \
             patch('pygame.display.set_mode') as mock_display, \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'), \
             patch('pygame.display.Info') as mock_info:
            
            mock_info.return_value.current_w = 1920
            mock_info.return_value.current_h = 1080
            mock_display.return_value = MagicMock()
            yield
    
    def test_package_imports(self):
        """Test that all main components can be imported."""
        # Test that imports work without errors
        assert DeformedGrid is not None
        assert DistortionType is not None
        assert ColorScheme is not None
        assert AudioAnalyzer is not None
        assert ColorGenerator is not None
        assert DistortionEngine is not None
        assert create_deformed_grid is not None
    
    def test_deformed_grid_with_all_distortion_types(self):
        """Test DeformedGrid with all distortion types."""
        for distortion_type in DistortionType:
            grid = DeformedGrid(
                dimension=4,
                distortion_fn=distortion_type.value,
                distortion_strength=0.3
            )
            
            # Should generate valid positions
            positions = grid._get_distorted_positions()
            assert len(positions) == 16
            
            # All positions should be valid
            for pos in positions:
                x, y, rotation = pos
                assert isinstance(x, (int, float))
                assert isinstance(y, (int, float))
                assert isinstance(rotation, (int, float))
    
    def test_deformed_grid_with_all_color_schemes(self):
        """Test DeformedGrid with all color schemes."""
        for color_scheme in ColorScheme:
            grid = DeformedGrid(
                dimension=4,
                color_scheme=color_scheme.value
            )
            
            # Should generate valid colors
            assert len(grid.base_colors) == 16
            
            # All colors should be valid RGB tuples
            for color in grid.base_colors:
                assert isinstance(color, tuple)
                assert len(color) == 3
                r, g, b = color
                assert 0 <= r <= 255
                assert 0 <= g <= 255
                assert 0 <= b <= 255
    
    def test_distortion_engine_color_generator_integration(self):
        """Test integration between DistortionEngine and ColorGenerator."""
        # Generate some positions
        base_positions = [(100, 100), (200, 200), (300, 300)]
        distortion_params = [
            DistortionEngine.generate_distortion_params()
            for _ in range(len(base_positions))
        ]
        
        # Apply distortions
        distorted_positions = DistortionEngine.get_distorted_positions(
            base_positions, distortion_params, DistortionType.SINE.value,
            10, 0.5, 0.0, (400, 400)
        )
        
        # Generate colors for the same positions
        colors = []
        for i, (base_x, base_y) in enumerate(base_positions):
            x_norm = base_x / 400.0
            y_norm = base_y / 400.0
            distance = ((x_norm - 0.5)**2 + (y_norm - 0.5)**2)**0.5
            
            color = ColorGenerator.get_color_for_position(
                ColorScheme.RAINBOW.value, (255, 255, 255),
                x_norm, y_norm, distance, i, 3
            )
            colors.append(color)
        
        # Should have matching number of positions and colors
        assert len(distorted_positions) == len(colors)
        assert len(distorted_positions) == 3
    
    @patch('distorsion_movement.deformed_grid.AudioAnalyzer')
    def test_audio_reactive_integration(self, mock_audio_analyzer):
        """Test audio-reactive functionality integration."""
        mock_analyzer = MagicMock()
        mock_analyzer.get_audio_features.return_value = {
            'bass_level': 0.8,
            'mid_level': 0.5,
            'high_level': 0.3,
            'overall_volume': 0.6,
            'beat_detected': True
        }
        mock_audio_analyzer.return_value = mock_analyzer
        
        grid = DeformedGrid(
            dimension=4,
            audio_reactive=True,
            distortion_strength=0.2
        )
        
        # Should have created audio analyzer
        assert grid.audio_analyzer is not None
        mock_analyzer.start_audio_capture.assert_called_once()
        
        # Should be able to get audio features
        features = grid.audio_analyzer.get_audio_features()
        assert features['bass_level'] == 0.8
        assert features['beat_detected'] is True
    
    def test_create_deformed_grid_function(self):
        """Test the convenience function for creating grids."""
        with patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock'), \
             patch('pygame.display.Info') as mock_info:
            
            mock_info.return_value.current_w = 1920
            mock_info.return_value.current_h = 1080
            
            grid = create_deformed_grid(
                dimension=8,
                distortion_strength=0.3,
                color_scheme="gradient"
            )
            
            assert isinstance(grid, DeformedGrid)
            assert grid.dimension == 8
            assert grid.distortion_strength == 0.3
            assert grid.color_scheme == "gradient"
    
    @patch('pygame.event.get', return_value=[])
    @patch('pygame.display.flip')
    def test_quick_demo_integration(self, mock_flip, mock_events):
        """Test the quick demo function."""
        with patch('pygame.display.set_mode'), \
             patch('pygame.display.set_caption'), \
             patch('pygame.time.Clock') as mock_clock, \
             patch('pygame.display.Info') as mock_info:
            
            mock_info.return_value.current_w = 1920
            mock_info.return_value.current_h = 1080
            mock_clock_instance = MagicMock()
            mock_clock.return_value = mock_clock_instance
            
            # Mock pygame.QUIT event to exit the demo
            mock_quit_event = MagicMock()
            mock_quit_event.type = pygame.QUIT
            mock_events.return_value = [mock_quit_event]
            
            # Mock the run_interactive method to avoid infinite loop
            with patch('distorsion_movement.deformed_grid.DeformedGrid.run_interactive'):
                # Should run without errors
                quick_demo()
    
    def test_enum_integration(self):
        """Test that enums work correctly with the system."""
        # Test DistortionType enum
        for distortion_type in DistortionType:
            params = DistortionEngine.generate_distortion_params()
            
            # Should be able to use enum values
            if distortion_type == DistortionType.RANDOM:
                result = DistortionEngine.apply_distortion_random(
                    (100, 100), params, 10, 0.5
                )
            elif distortion_type == DistortionType.SINE:
                result = DistortionEngine.apply_distortion_sine(
                    (100, 100), params, 10, 0.5, 0.0
                )
            # Add more as needed
            
            if distortion_type in [DistortionType.RANDOM, DistortionType.SINE]:
                assert len(result) == 3
                assert all(isinstance(val, (int, float)) for val in result)
        
        # Test ColorScheme enum
        for color_scheme in ColorScheme:
            color = ColorGenerator.get_color_for_position(
                color_scheme.value, (255, 255, 255), 0.5, 0.5, 0.5, 0, 10
            )
            
            assert isinstance(color, tuple)
            assert len(color) == 3
            assert all(0 <= val <= 255 for val in color)
    
    def test_parameter_validation_integration(self):
        """Test that the system handles edge cases gracefully."""
        # Test with extreme parameters
        grid = DeformedGrid(
            dimension=1,  # Minimum dimension
            cell_size=1,  # Minimum cell size
            canvas_size=(10, 10),  # Small canvas
            distortion_strength=2.0  # High distortion
        )
        
        # Should still work
        assert len(grid.base_positions) == 1
        positions = grid._get_distorted_positions()
        assert len(positions) == 1
    
    def test_color_distortion_consistency(self):
        """Test that colors and distortions are consistently generated."""
        grid = DeformedGrid(dimension=5, color_scheme="rainbow")
        
        # Number of colors should match positions
        assert len(grid.base_colors) == len(grid.base_positions)
        assert len(grid.distortions) == len(grid.base_positions)
        assert len(grid.base_positions) == 25  # 5x5
        
        # Colors should be deterministic for same parameters
        grid2 = DeformedGrid(dimension=5, color_scheme="rainbow")
        assert grid.base_colors == grid2.base_colors
    
    @pytest.mark.slow
    def test_performance_large_grid(self):
        """Test performance with larger grids."""
        # This test checks that large grids can be created without issues
        grid = DeformedGrid(dimension=50)  # 2500 squares
        
        # Should complete without timeout or memory issues
        positions = grid._get_distorted_positions()
        assert len(positions) == 2500
        
        # Basic sanity checks
        for pos in positions[:10]:  # Check first 10 positions
            x, y, rotation = pos
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert isinstance(rotation, (int, float))
    
    def test_module_cleanup(self):
        """Test that modules clean up resources properly."""
        # Test audio analyzer cleanup
        analyzer = AudioAnalyzer()
        analyzer.stop_audio_capture()  # Should not raise error even if not started
        
        # Test grid cleanup (implicit through garbage collection)
        grid = DeformedGrid(dimension=2)
        del grid  # Should not cause issues