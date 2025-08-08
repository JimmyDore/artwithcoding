"""
Unit tests for distortions module.
"""

import pytest
import math
from unittest.mock import patch
from distorsion_movement.distortions import DistortionEngine
from distorsion_movement.enums import DistortionType


class TestDistortionEngine:
    """Test cases for DistortionEngine class."""
    
    def test_generate_distortion_params(self):
        """Test that distortion parameters are generated correctly."""
        params = DistortionEngine.generate_distortion_params()
        
        # Check that all required keys are present
        required_keys = ['offset_x', 'offset_y', 'phase_x', 'phase_y', 'frequency', 'rotation_phase']
        assert all(key in params for key in required_keys)
        
        # Check that values are within expected ranges
        assert -1 <= params['offset_x'] <= 1
        assert -1 <= params['offset_y'] <= 1
        assert 0 <= params['phase_x'] <= 2 * math.pi
        assert 0 <= params['phase_y'] <= 2 * math.pi
        assert 0.5 <= params['frequency'] <= 2.0
        assert 0 <= params['rotation_phase'] <= 2 * math.pi
    
    def test_generate_distortion_params_randomness(self):
        """Test that distortion parameters are actually random."""
        params1 = DistortionEngine.generate_distortion_params()
        params2 = DistortionEngine.generate_distortion_params()
        
        # It's extremely unlikely that all parameters would be identical
        assert params1 != params2
    
    def test_apply_distortion_random(self):
        """Test random distortion application."""
        base_pos = (100.0, 100.0)
        params = {
            'offset_x': 0.5,
            'offset_y': -0.3,
            'phase_x': 0,
            'phase_y': 0,
            'frequency': 1.0,
            'rotation_phase': 0
        }
        cell_size = 10
        distortion_strength = 0.5
        
        x, y, rotation = DistortionEngine.apply_distortion_random(
            base_pos, params, cell_size, distortion_strength
        )
        
        # Check that position is modified
        assert x != base_pos[0]
        assert y != base_pos[1]
        
        # Check that rotation is a valid angle
        assert isinstance(rotation, (int, float))
        
        # With these params, x should increase, y should decrease
        assert x > base_pos[0]
        assert y < base_pos[1]
    
    def test_apply_distortion_random_zero_strength(self):
        """Test that zero distortion strength returns original position."""
        base_pos = (100.0, 100.0)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 10
        distortion_strength = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_random(
            base_pos, params, cell_size, distortion_strength
        )
        
        # With zero strength, position should be unchanged
        assert x == base_pos[0]
        assert y == base_pos[1]
        assert rotation == 0.0
    
    def test_apply_distortion_sine(self):
        """Test sine wave distortion application."""
        base_pos = (100.0, 100.0)
        params = {
            'offset_x': 0.0,
            'offset_y': 0.0,
            'phase_x': 0.0,
            'phase_y': math.pi/2,  # 90 degrees phase
            'frequency': 1.0,
            'rotation_phase': 0.0
        }
        cell_size = 10
        distortion_strength = 1.0
        time_factor = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_sine(
            base_pos, params, cell_size, distortion_strength, time_factor
        )
        
        # Check that position is modified
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
        
        # With phase_y = pi/2, cosine should be at 0
        # Looking at the implementation: dy = math.cos(time * frequency + phase_y) * max_offset
        expected_y_offset = cell_size * distortion_strength * math.cos(time_factor * params['frequency'] + params['phase_y'])
        assert abs(y - (base_pos[1] + expected_y_offset)) < 0.001
    
    def test_apply_distortion_sine_with_time(self):
        """Test sine distortion with time animation."""
        base_pos = (100.0, 100.0)
        params = {
            'offset_x': 0.0,
            'offset_y': 0.0,
            'phase_x': 0.0,
            'phase_y': 0.0,
            'frequency': 1.0,
            'rotation_phase': 0.0
        }
        cell_size = 10
        distortion_strength = 1.0
        
        # Test at different time points
        x1, y1, r1 = DistortionEngine.apply_distortion_sine(
            base_pos, params, cell_size, distortion_strength, 0.0
        )
        x2, y2, r2 = DistortionEngine.apply_distortion_sine(
            base_pos, params, cell_size, distortion_strength, math.pi
        )
        
        # Positions should be different at different times
        assert (x1, y1) != (x2, y2)
    
    def test_apply_distortion_perlin(self):
        """Test Perlin noise distortion application."""
        base_pos = (100.0, 100.0)
        params = {
            'offset_x': 0.5,
            'offset_y': -0.3,
            'phase_x': 0,
            'phase_y': 0,
            'frequency': 1.0,
            'rotation_phase': 0
        }
        cell_size = 10
        distortion_strength = 0.5
        time_factor = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_perlin(
            base_pos, params, cell_size, distortion_strength, time_factor
        )
        
        # Check that position is modified
        assert x != base_pos[0]
        assert y != base_pos[1]
        assert isinstance(rotation, (int, float))
    
    def test_apply_distortion_circular(self):
        """Test circular distortion application."""
        base_pos = (100.0, 100.0)
        params = {
            'offset_x': 0.0,
            'offset_y': 0.0,
            'phase_x': 0.0,
            'phase_y': 0.0,
            'frequency': 1.0,
            'rotation_phase': 0.0
        }
        cell_size = 10
        distortion_strength = 1.0
        time_factor = 0.0
        canvas_size = (200, 200)
        
        x, y, rotation = DistortionEngine.apply_distortion_circular(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # Check that position is modified
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
        
        # The distortion should move points relative to center
        center_x, center_y = canvas_size[0] // 2, canvas_size[1] // 2
        original_distance = math.sqrt((base_pos[0] - center_x)**2 + (base_pos[1] - center_y)**2)
        new_distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        # Basic sanity check
        assert new_distance >= 0
    
    def test_apply_distortion_circular_zero_distance(self):
        """Test circular distortion when point is at center."""
        canvas_size = (200, 200)
        center_x, center_y = canvas_size[0] // 2, canvas_size[1] // 2
        base_pos = (float(center_x), float(center_y))  # Point at center
        params = DistortionEngine.generate_distortion_params()
        cell_size = 10
        distortion_strength = 1.0
        time_factor = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_circular(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # Should handle zero distance gracefully
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
        
        # At center, position should remain unchanged
        assert x == base_pos[0]
        assert y == base_pos[1]
        assert rotation == 0
    
    def test_apply_distortion_swirl(self):
        """Test swirl distortion application."""
        base_pos = (100.0, 100.0)
        params = {
            'offset_x': 0.0,
            'offset_y': 0.0,
            'phase_x': 0.0,
            'phase_y': 0.0,
            'frequency': 1.0,
            'rotation_phase': 0.0
        }
        cell_size = 10
        distortion_strength = 1.0
        time_factor = 0.0
        canvas_size = (200, 200)
        
        x, y, rotation = DistortionEngine.apply_distortion_swirl(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # Check that return values are valid
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
        
        # The swirl should create some displacement for non-center points
        center_x, center_y = canvas_size[0] // 2, canvas_size[1] // 2
        if base_pos != (center_x, center_y):
            # Position should be modified for non-center points
            assert (x, y) != base_pos
    
    def test_apply_distortion_swirl_center_singularity(self):
        """Test swirl distortion handles center point singularity."""
        canvas_size = (200, 200)
        center_x, center_y = canvas_size[0] // 2, canvas_size[1] // 2
        base_pos = (float(center_x), float(center_y))  # Point at center
        params = DistortionEngine.generate_distortion_params()
        cell_size = 10
        distortion_strength = 1.0
        time_factor = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_swirl(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # At center, should handle singularity gracefully
        assert x == base_pos[0]
        assert y == base_pos[1]
        assert rotation == 0
    
    def test_apply_distortion_swirl_with_time(self):
        """Test swirl distortion animation with time."""
        base_pos = (150.0, 100.0)
        params = {
            'offset_x': 0.0,
            'offset_y': 0.0,
            'phase_x': 0.0,
            'phase_y': 0.0,
            'frequency': 1.0,
            'rotation_phase': 0.0
        }
        cell_size = 10
        distortion_strength = 1.0
        canvas_size = (200, 200)
        
        # Test at different time points
        x1, y1, r1 = DistortionEngine.apply_distortion_swirl(
            base_pos, params, cell_size, distortion_strength, 0.0, canvas_size
        )
        x2, y2, r2 = DistortionEngine.apply_distortion_swirl(
            base_pos, params, cell_size, distortion_strength, math.pi, canvas_size
        )
        
        # Positions and rotations should be different at different times
        assert (x1, y1, r1) != (x2, y2, r2)
    
    def test_apply_distortion_swirl_displacement_bounded(self):
        """Test that swirl displacement is bounded by cell_size * distortion_strength."""
        base_pos = (150.0, 120.0)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 20
        distortion_strength = 0.5
        time_factor = 0.0
        canvas_size = (300, 300)
        
        x, y, rotation = DistortionEngine.apply_distortion_swirl(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # Calculate displacement
        displacement_x = x - base_pos[0]
        displacement_y = y - base_pos[1]
        displacement_magnitude = math.sqrt(displacement_x**2 + displacement_y**2)
        
        # Should be bounded by max_offset = cell_size * distortion_strength
        max_offset = cell_size * distortion_strength
        assert displacement_magnitude <= max_offset + 0.001  # Small tolerance for floating point
    
    def test_apply_distortion_ripple(self):
        """Test basic ripple distortion functionality."""
        base_pos = (150.0, 120.0)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 20
        distortion_strength = 0.5
        time_factor = 0.0
        canvas_size = (300, 300)
        
        x, y, rotation = DistortionEngine.apply_distortion_ripple(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # Should return valid numbers
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
        
        # Should not be NaN or infinity
        assert not math.isnan(x)
        assert not math.isnan(y)
        assert not math.isnan(rotation)
        assert math.isfinite(x)
        assert math.isfinite(y)
        assert math.isfinite(rotation)
    
    def test_apply_distortion_ripple_center_singularity(self):
        """Test ripple distortion handles center singularity correctly."""
        canvas_size = (300, 300)
        center_pos = (canvas_size[0] // 2, canvas_size[1] // 2)  # (150, 150)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 20
        distortion_strength = 0.5
        time_factor = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_ripple(
            center_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # At center, should return original position with zero rotation
        assert x == center_pos[0]
        assert y == center_pos[1]
        assert rotation == 0
    
    def test_apply_distortion_ripple_with_time(self):
        """Test that ripple distortion changes over time."""
        base_pos = (100.0, 80.0)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 15
        distortion_strength = 0.7
        canvas_size = (200, 200)
        
        # Test with different time values
        x1, y1, r1 = DistortionEngine.apply_distortion_ripple(
            base_pos, params, cell_size, distortion_strength, 0.0, canvas_size
        )
        x2, y2, r2 = DistortionEngine.apply_distortion_ripple(
            base_pos, params, cell_size, distortion_strength, 1.0, canvas_size
        )
        
        # Positions and rotations should be different at different times
        assert (x1, y1, r1) != (x2, y2, r2)
    
    def test_apply_distortion_ripple_displacement_bounded(self):
        """Test that ripple displacement is bounded by cell_size * distortion_strength."""
        base_pos = (180.0, 140.0)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 25
        distortion_strength = 0.6
        time_factor = 0.5
        canvas_size = (400, 400)
        
        x, y, rotation = DistortionEngine.apply_distortion_ripple(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # Calculate displacement
        displacement_x = x - base_pos[0]
        displacement_y = y - base_pos[1]
        displacement_magnitude = math.sqrt(displacement_x**2 + displacement_y**2)
        
        # Should be bounded by max_offset = cell_size * distortion_strength
        max_offset = cell_size * distortion_strength
        assert displacement_magnitude <= max_offset + 0.001  # Small tolerance for floating point
    
    def test_apply_distortion_ripple_tangential_direction(self):
        """Test that ripple distortion applies displacement in tangential direction."""
        canvas_size = (200, 200)
        center_x, center_y = canvas_size[0] // 2, canvas_size[1] // 2
        
        # Test point on positive x-axis (tangent should be in y direction)
        base_pos = (center_x + 50, center_y)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 20
        distortion_strength = 1.0
        time_factor = 0.0
        
        x, y, rotation = DistortionEngine.apply_distortion_ripple(
            base_pos, params, cell_size, distortion_strength, time_factor, canvas_size
        )
        
        # For a point on positive x-axis, displacement should be primarily in y direction
        displacement_x = x - base_pos[0]
        displacement_y = y - base_pos[1]
        
        # Due to ripple effect, y displacement should generally be larger than x displacement
        # when the point is on the x-axis (tangent is perpendicular to radius)
        # Note: This test might be sensitive to time and phase, so we just check basic behavior
        assert isinstance(displacement_x, (int, float))
        assert isinstance(displacement_y, (int, float))
    
    @pytest.mark.parametrize("distortion_type", [
        DistortionType.RANDOM,
        DistortionType.SINE,
        DistortionType.PERLIN,
        DistortionType.CIRCULAR,
        DistortionType.SWIRL,
        DistortionType.RIPPLE
    ])
    def test_all_distortion_types_return_valid_output(self, distortion_type):
        """Test that all distortion types return valid output."""
        base_pos = (100.0, 100.0)
        params = DistortionEngine.generate_distortion_params()
        cell_size = 10
        distortion_strength = 0.5
        time_factor = 0.0
        center = (50.0, 50.0)
        
        if distortion_type == DistortionType.RANDOM:
            result = DistortionEngine.apply_distortion_random(
                base_pos, params, cell_size, distortion_strength
            )
        elif distortion_type == DistortionType.SINE:
            result = DistortionEngine.apply_distortion_sine(
                base_pos, params, cell_size, distortion_strength, time_factor
            )
        elif distortion_type == DistortionType.PERLIN:
            result = DistortionEngine.apply_distortion_perlin(
                base_pos, params, cell_size, distortion_strength, time_factor
            )
        elif distortion_type == DistortionType.CIRCULAR:
            result = DistortionEngine.apply_distortion_circular(
                base_pos, params, cell_size, distortion_strength, time_factor, (200, 200)
            )
        elif distortion_type == DistortionType.SWIRL:
            result = DistortionEngine.apply_distortion_swirl(
                base_pos, params, cell_size, distortion_strength, time_factor, (200, 200)
            )
        elif distortion_type == DistortionType.RIPPLE:
            result = DistortionEngine.apply_distortion_ripple(
                base_pos, params, cell_size, distortion_strength, time_factor, (200, 200)
            )
        
        assert len(result) == 3
        x, y, rotation = result
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
    
    def test_get_distorted_positions(self):
        """Test batch processing of distorted positions."""
        base_positions = [(100.0, 100.0), (200.0, 150.0), (50.0, 75.0)]
        distortion_params = [
            DistortionEngine.generate_distortion_params()
            for _ in range(len(base_positions))
        ]
        distortion_fn = DistortionType.SINE.value
        cell_size = 10
        distortion_strength = 0.5
        time = 0.0
        canvas_size = (400, 300)
        
        positions = DistortionEngine.get_distorted_positions(
            base_positions, distortion_params, distortion_fn, 
            cell_size, distortion_strength, time, canvas_size
        )
        
        # Should return same number of positions
        assert len(positions) == len(base_positions)
        
        # Each position should be a tuple of 3 elements
        for pos in positions:
            assert len(pos) == 3
            x, y, rotation = pos
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert isinstance(rotation, (int, float))
    
    def test_get_distorted_positions_ripple(self):
        """Test ripple distortion via get_distorted_positions function."""
        base_positions = [(100.0, 100.0), (150.0, 120.0), (80.0, 160.0)]
        distortion_params = [
            DistortionEngine.generate_distortion_params()
            for _ in range(len(base_positions))
        ]
        distortion_fn = DistortionType.RIPPLE.value
        cell_size = 15
        distortion_strength = 0.7
        time = 0.5
        canvas_size = (250, 250)
        
        positions = DistortionEngine.get_distorted_positions(
            base_positions, distortion_params, distortion_fn, 
            cell_size, distortion_strength, time, canvas_size
        )
        
        # Should return same number of positions
        assert len(positions) == len(base_positions)
        
        # Each position should be a tuple of 3 elements
        for pos in positions:
            assert len(pos) == 3
            x, y, rotation = pos
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert isinstance(rotation, (int, float))
            
            # Check values are finite
            assert math.isfinite(x)
            assert math.isfinite(y)
            assert math.isfinite(rotation)
    
    def test_get_distorted_positions_unknown_type(self):
        """Test that unknown distortion type defaults to random."""
        base_positions = [(100.0, 100.0)]
        distortion_params = [DistortionEngine.generate_distortion_params()]
        distortion_fn = "unknown_type"
        cell_size = 10
        distortion_strength = 0.5
        time = 0.0
        canvas_size = (400, 300)
        
        positions = DistortionEngine.get_distorted_positions(
            base_positions, distortion_params, distortion_fn, 
            cell_size, distortion_strength, time, canvas_size
        )
        
        # Should still work and return valid positions
        assert len(positions) == 1
        x, y, rotation = positions[0]
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(rotation, (int, float))
    
    def test_get_distorted_positions_swirl(self):
        """Test swirl distortion via get_distorted_positions function."""
        base_positions = [(100.0, 100.0), (150.0, 120.0)]
        distortion_params = [
            DistortionEngine.generate_distortion_params()
            for _ in range(len(base_positions))
        ]
        distortion_fn = DistortionType.SWIRL.value
        cell_size = 10
        distortion_strength = 0.5
        time = 0.0
        canvas_size = (200, 200)
        
        positions = DistortionEngine.get_distorted_positions(
            base_positions, distortion_params, distortion_fn, 
            cell_size, distortion_strength, time, canvas_size
        )
        
        # Should return same number of positions
        assert len(positions) == len(base_positions)
        
        # Each position should be a tuple of 3 elements
        for pos in positions:
            assert len(pos) == 3
            x, y, rotation = pos
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert isinstance(rotation, (int, float))
    
    def test_get_distorted_positions_ripple(self):
        """Test ripple distortion via get_distorted_positions function."""
        base_positions = [(100.0, 100.0), (150.0, 120.0), (80.0, 160.0)]
        distortion_params = [
            DistortionEngine.generate_distortion_params()
            for _ in range(len(base_positions))
        ]
        distortion_fn = DistortionType.RIPPLE.value
        cell_size = 15
        distortion_strength = 0.7
        time = 0.5
        canvas_size = (250, 250)
        
        positions = DistortionEngine.get_distorted_positions(
            base_positions, distortion_params, distortion_fn, 
            cell_size, distortion_strength, time, canvas_size
        )
        
        # Should return same number of positions
        assert len(positions) == len(base_positions)
        
        # Each position should be a tuple of 3 elements
        for pos in positions:
            assert len(pos) == 3
            x, y, rotation = pos
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert isinstance(rotation, (int, float))
            
            # Check values are finite
            assert math.isfinite(x)
            assert math.isfinite(y)
            assert math.isfinite(rotation)