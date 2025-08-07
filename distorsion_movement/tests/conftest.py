"""
Shared test fixtures and configuration for distorsion_movement tests.
"""

import pytest
import pygame
from unittest.mock import patch, MagicMock


@pytest.fixture
def mock_pygame():
    """Mock pygame for tests that don't need actual display."""
    with patch('pygame.init'), \
         patch('pygame.display.set_mode') as mock_display, \
         patch('pygame.display.set_caption'), \
         patch('pygame.time.Clock'), \
         patch('pygame.display.Info') as mock_info:
        
        mock_info.return_value.current_w = 1920
        mock_info.return_value.current_h = 1080
        mock_display.return_value = MagicMock()
        yield


@pytest.fixture
def sample_distortion_params():
    """Provide sample distortion parameters for testing."""
    return {
        'offset_x': 0.5,
        'offset_y': -0.3,
        'phase_x': 0.0,
        'phase_y': 1.57,  # π/2
        'frequency': 1.0,
        'rotation_phase': 0.0
    }


@pytest.fixture
def sample_positions():
    """Provide sample positions for testing."""
    return [
        (100.0, 100.0),
        (200.0, 150.0),
        (300.0, 200.0),
        (150.0, 250.0)
    ]


@pytest.fixture
def sample_colors():
    """Provide sample RGB colors for testing."""
    return [
        (255, 0, 0),      # Red
        (0, 255, 0),      # Green
        (0, 0, 255),      # Blue
        (255, 255, 255)   # White
    ]


@pytest.fixture
def sample_mouse_positions():
    """Provide sample mouse positions for testing."""
    return [
        (0, 0),
        (100, 100), 
        (200, 150),
        (50, 75)
    ]


@pytest.fixture
def mock_pygame_events():
    """Mock pygame events for mouse interaction testing."""
    return []


# Configure pytest markers
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "audio: Tests requiring audio hardware")
    config.addinivalue_line("markers", "slow: Slow tests that take more than a few seconds")


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location and name."""
    for item in items:
        # Mark integration tests
        if "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Mark audio tests
        if "audio" in item.name.lower() or "test_audio" in item.nodeid:
            item.add_marker(pytest.mark.audio)
        
        # Mark slow tests
        if "large" in item.name.lower() or "performance" in item.name.lower():
            item.add_marker(pytest.mark.slow)
        
        # Mark remaining tests as unit tests if not already marked
        if not any(mark.name in ['integration', 'audio', 'slow'] for mark in item.iter_markers()):
            item.add_marker(pytest.mark.unit)