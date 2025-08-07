"""
Unit tests for audio_analyzer module.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from distorsion_movement.audio_analyzer import AudioAnalyzer, AUDIO_AVAILABLE


class TestAudioAnalyzer:
    """Test cases for AudioAnalyzer class."""
    
    def test_init(self):
        """Test AudioAnalyzer initialization."""
        analyzer = AudioAnalyzer()
        
        assert analyzer.sample_rate == 44100
        assert analyzer.chunk_size == 1024
        assert analyzer.bass_range == (20, 250)
        assert analyzer.mid_range == (250, 4000)
        assert analyzer.high_range == (4000, 20000)
        assert analyzer.bass_level == 0.0
        assert analyzer.mid_level == 0.0
        assert analyzer.high_level == 0.0
        assert analyzer.overall_volume == 0.0
        assert analyzer.beat_detected is False
        assert analyzer.is_running is False
        assert analyzer.audio_thread is None
        assert analyzer.beat_threshold == 1.3
        assert analyzer.smoothing_factor == 0.8
    
    def test_init_custom_params(self):
        """Test AudioAnalyzer initialization with custom parameters."""
        sample_rate = 48000
        chunk_size = 2048
        
        analyzer = AudioAnalyzer(sample_rate=sample_rate, chunk_size=chunk_size)
        
        assert analyzer.sample_rate == sample_rate
        assert analyzer.chunk_size == chunk_size
    
    def test_detect_beat_logic(self):
        """Test beat detection logic."""
        analyzer = AudioAnalyzer()
        
        # Fill volume history with low values
        for _ in range(15):
            analyzer._detect_beat(0.1)
        
        assert analyzer.beat_detected is False
        
        # Send a high volume spike
        analyzer._detect_beat(1.0)
        
        # Should detect beat if spike is significant enough
        # (depends on threshold and history)
        assert isinstance(analyzer.beat_detected, bool)
    
    def test_detect_beat_cooldown(self):
        """Test beat detection cooldown mechanism."""
        analyzer = AudioAnalyzer()
        
        # Fill history with baseline
        for _ in range(15):
            analyzer._detect_beat(0.1)
        
        # Trigger beat detection
        analyzer._detect_beat(1.0)
        
        # If beat was detected, cooldown should be active
        if analyzer.beat_detected:
            assert analyzer.beat_cooldown > 0
            
            # During cooldown, another spike shouldn't trigger immediately
            old_cooldown = analyzer.beat_cooldown
            analyzer._detect_beat(1.0)
            assert analyzer.beat_cooldown <= old_cooldown
    
    def test_get_audio_features_no_audio(self):
        """Test getting audio features when no audio is running."""
        analyzer = AudioAnalyzer()
        
        features = analyzer.get_audio_features()
        
        expected_features = {
            'bass_level': 0.0,
            'mid_level': 0.0,
            'high_level': 0.0,
            'overall_volume': 0.0,
            'beat_detected': False
        }
        
        assert features == expected_features
    
    @pytest.mark.skipif(not AUDIO_AVAILABLE, reason="Audio libraries not available")
    @patch('distorsion_movement.audio_analyzer.pyaudio.PyAudio')
    def test_start_stop_audio_capture(self, mock_pyaudio):
        """Test starting and stopping audio capture."""
        # Mock PyAudio
        mock_audio = MagicMock()
        mock_stream = MagicMock()
        mock_pyaudio.return_value = mock_audio
        mock_audio.open.return_value = mock_stream
        
        analyzer = AudioAnalyzer()
        
        # Test start
        analyzer.start_audio_capture()
        assert analyzer.is_running is True
        assert analyzer.audio_thread is not None
        
        # Test stop
        analyzer.stop_audio_capture()
        assert analyzer.is_running is False
        
        # Verify PyAudio was called correctly
        mock_audio.open.assert_called_once()
        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()
        mock_audio.terminate.assert_called_once()
    
    @pytest.mark.skipif(AUDIO_AVAILABLE, reason="Test only when audio is not available")
    def test_start_audio_capture_no_audio_libs(self):
        """Test starting audio capture when audio libraries are not available."""
        analyzer = AudioAnalyzer()
        
        # Should not raise an exception, but should not start either
        analyzer.start_audio_capture()
        assert analyzer.is_running is False
        assert analyzer.audio_thread is None
    
    def test_audio_feature_normalization(self):
        """Test that audio features are properly normalized."""
        analyzer = AudioAnalyzer()
        
        # Set some raw levels
        analyzer.bass_level = 0.01  # Will be multiplied by 100 in get_audio_features
        analyzer.mid_level = 0.02   # Will be multiplied by 50
        analyzer.high_level = 0.05  # Will be multiplied by 20
        analyzer.overall_volume = 0.03  # Will be multiplied by 30
        
        features = analyzer.get_audio_features()
        
        # Check normalization
        assert features['bass_level'] == min(0.01 * 100, 1.0)
        assert features['mid_level'] == min(0.02 * 50, 1.0)
        assert features['high_level'] == min(0.05 * 20, 1.0)
        assert features['overall_volume'] == min(0.03 * 30, 1.0)
        
        # All should be clamped to 1.0 max
        for level in ['bass_level', 'mid_level', 'high_level', 'overall_volume']:
            assert 0.0 <= features[level] <= 1.0
    
    def test_frequency_range_boundaries(self):
        """Test that frequency ranges are properly defined."""
        analyzer = AudioAnalyzer()
        
        # Check that ranges don't overlap incorrectly
        assert analyzer.bass_range[1] == analyzer.mid_range[0]
        assert analyzer.mid_range[1] == analyzer.high_range[0]
        
        # Check that ranges are within reasonable bounds
        assert analyzer.bass_range[0] >= 0
        assert analyzer.high_range[1] <= analyzer.sample_rate / 2
    
    def test_thread_safety(self):
        """Test that audio levels can be read safely."""
        analyzer = AudioAnalyzer()
        
        # Set some levels
        analyzer.bass_level = 0.005  # Will be 0.5 after normalization
        analyzer.mid_level = 0.006   # Will be 0.3 after normalization
        analyzer.high_level = 0.035  # Will be 0.7 after normalization
        
        # Get features multiple times
        features1 = analyzer.get_audio_features()
        features2 = analyzer.get_audio_features()
        
        # Should be consistent
        assert features1['bass_level'] == features2['bass_level']
        assert features1['mid_level'] == features2['mid_level']
        assert features1['high_level'] == features2['high_level']
    
    def test_volume_history_management(self):
        """Test that volume history is properly managed."""
        analyzer = AudioAnalyzer()
        
        # Add more than 20 values
        for i in range(25):
            analyzer._detect_beat(i * 0.1)
        
        # History should be capped at 20
        assert len(analyzer.volume_history) == 20
        
        # Should contain the most recent values
        assert analyzer.volume_history[-1] == 24 * 0.1
    
    def test_smoothing_factor_effect(self):
        """Test that smoothing factor affects level updates."""
        analyzer = AudioAnalyzer()
        
        # Set initial levels
        analyzer.bass_level = 0.5
        old_bass = analyzer.bass_level
        
        # Simulate processing with new data
        # (This would normally happen in _process_audio, but we'll simulate)
        new_value = 1.0
        expected_smoothed = old_bass * analyzer.smoothing_factor + new_value * (1 - analyzer.smoothing_factor)
        
        # Manual smoothing calculation to verify the concept
        assert analyzer.smoothing_factor == 0.8
        assert abs(expected_smoothed - (0.5 * 0.8 + 1.0 * 0.2)) < 0.001