# 🎨 Distorsion Movement - Interactive Generative Art Engine

**Distorsion Movement** is a real-time generative art platform that creates mesmerizing visual experiences through geometrically deformed grids. The system generates dynamic, interactive artwork by applying mathematical distortions to regular grids of colored squares, with optional audio-reactive capabilities for music visualization.

## 🎯 Project Overview

### What It Does
The project creates animated grids of squares where each square can be:
- **Geometrically distorted** using mathematical functions (sine waves, Perlin noise, circular patterns)
- **Dynamically colored** using various schemes (rainbow, gradient, neon, temperature-based, etc.)
- **Audio-reactive** to music and sound input in real-time
- **Interactively controlled** through keyboard shortcuts and parameters

### How It Works Technically

The core architecture follows a modular design with clear separation of concerns:

1. **Grid Generation**: Creates a regular NxN grid of squares with base positions
2. **Distortion Engine**: Applies mathematical transformations to deform square positions and orientations
3. **Color System**: Generates dynamic colors based on position, time, and audio input
4. **Audio Analysis**: Real-time FFT analysis of microphone input to extract bass, mids, highs, and beat detection
5. **Rendering**: Real-time pygame-based visualization with 60fps target

### Mathematical Foundation

The distortions are based on several mathematical approaches:
- **Sine Wave Distortions**: `sin(x * frequency + phase) * amplitude`
- **Perlin Noise**: Smooth, organic-looking deformations
- **Circular Distortions**: Radial distortions from center points
- **Random Static**: Controlled randomness for chaotic effects

Audio reactivity maps frequency bands to visual parameters:
- 🥁 **Bass (20-250Hz)** → Distortion intensity
- 🎸 **Mids (250Hz-4kHz)** → Color hue rotation  
- ✨ **Highs (4kHz+)** → Brightness boosts
- 💥 **Beat detection** → Flash effects
- 📢 **Overall volume** → Animation speed

## 🏗️ Project Structure

```
distorsion_movement/
├── __init__.py              # Package entry point & public API
├── deformed_grid.py         # Main DeformedGrid class (366 lines)
├── enums.py                 # Type definitions (DistortionType, ColorScheme)
├── audio_analyzer.py        # Real-time audio analysis & FFT processing
├── colors.py                # Color generation algorithms
├── distortions.py           # Geometric distortion algorithms
├── demos.py                 # Demo functions & usage examples
├── test_modules.py          # Unit tests
├── improvements.md          # Future development roadmap
├── README_modules.md        # Detailed module documentation
└── README.md               # This file
```

### Module Responsibilities

#### 🎨 **`deformed_grid.py`** - Core Engine (366 lines)
- Main `DeformedGrid` class that orchestrates everything
- Pygame rendering loop and event handling
- Grid generation and position calculations
- Animation timing and state management
- Fullscreen/windowed mode switching
- Interactive controls (keyboard shortcuts)

#### 🎵 **`audio_analyzer.py`** - Audio Processing
- Real-time microphone input capture using PyAudio
- FFT analysis for frequency separation
- Beat detection algorithms
- Thread-safe audio data sharing
- Graceful degradation when audio libraries unavailable

#### 🌈 **`colors.py`** - Color Generation
- 10 different color schemes (monochrome, gradient, rainbow, neon, etc.)
- Position-based color calculations
- Time-based color animations
- Audio-reactive color modulation
- HSV/RGB color space conversions

#### 🌀 **`distortions.py`** - Geometric Engine 
- 4 distortion algorithms (random, sine, Perlin, circular)
- Mathematical transformation functions
- Parameter generation for each square
- Time-based animation calculations
- Audio-reactive distortion intensity

#### 🎮 **`demos.py`** - Usage Examples
- Pre-configured demonstration functions
- Simple API for quick setup
- Different preset combinations
- Command-line interface

#### 📝 **`enums.py`** - Type Safety
- `DistortionType`: RANDOM, SINE, PERLIN, CIRCULAR
- `ColorScheme`: MONOCHROME, GRADIENT, RAINBOW, COMPLEMENTARY, TEMPERATURE, PASTEL, NEON, OCEAN, FIRE, FOREST

## 🚀 Quick Start

### Basic Usage
```python
from distorsion_movement import quick_demo

# Launch with default settings
quick_demo()
```

### Advanced Configuration
```python
from distorsion_movement import DeformedGrid, DistortionType, ColorScheme

# Create custom grid
grid = DeformedGrid(
    dimension=64,                           # 64x64 grid
    cell_size=12,                          # 12px squares
    distortion_strength=0.7,               # 70% distortion
    distortion_fn=DistortionType.SINE.value,     # Sine wave distortion
    color_scheme=ColorScheme.NEON.value,         # Neon colors
    audio_reactive=True,                   # Enable audio reactivity
    color_animation=True                   # Animate colors
)

grid.run_interactive()
```

### Available Demo Functions
```python
from distorsion_movement import quick_demo, fullscreen_demo, audio_reactive_demo

quick_demo()           # Basic windowed demo
fullscreen_demo()      # Immersive fullscreen experience  
audio_reactive_demo()  # Music visualization demo
```

## 🎛️ Interactive Controls

| Key | Action |
|-----|--------|
| `F` | Toggle fullscreen/windowed mode |
| `M` | Toggle audio reactivity on/off |
| `C` | Cycle through color schemes |
| `D` | Cycle through distortion types |
| `+/-` | Increase/decrease distortion intensity |
| `A` | Toggle color animation |
| `R` | Reset to default parameters |
| `ESC` | Exit application |

## 🎨 Available Visual Modes

### Distortion Types
- **Random**: Static chaotic displacement
- **Sine**: Smooth wave-based deformations
- **Perlin**: Organic, noise-based distortions  
- **Circular**: Radial distortions from center

### Color Schemes
- **Monochrome**: Single color variations
- **Gradient**: Smooth color transitions
- **Rainbow**: Full spectrum cycling
- **Complementary**: Alternating opposite colors
- **Temperature**: Cool to warm transitions
- **Pastel**: Soft, muted tones
- **Neon**: Bright, electric colors
- **Ocean**: Blue-green aquatic themes
- **Fire**: Red-orange-yellow flames
- **Forest**: Green-brown natural tones

## 🔧 Dependencies

### Required
```
pygame>=2.1.0
numpy>=1.21.0
```

### Optional (for audio reactivity)
```
pyaudio>=0.2.11
scipy>=1.7.0
```

Install with:
```bash
pip install pygame numpy
# For audio features:
pip install pyaudio scipy
```

## 🎵 Audio-Reactive Features

When audio reactivity is enabled, the system:
- Captures real-time microphone input
- Performs FFT analysis to separate frequency bands
- Maps audio characteristics to visual parameters
- Detects beats for synchronized flash effects
- Smooths audio data to prevent jarring transitions

**Note**: Audio features require additional dependencies and microphone permissions.

## 🧪 Testing

Run the test suite:
```bash
cd distorsion_movement
python test_modules.py
```

## 🛣️ Development Roadmap

The project has an extensive roadmap for future enhancements (see `improvements.md`):

### Phase 1 (High Priority)
- Mouse interaction (attraction/repulsion effects)
- Additional shape types (circles, triangles, polygons)
- Motion blur and glow effects
- GIF/MP4 export capabilities
- Preset scene system

### Phase 2 (Advanced Features)
- Particle systems and trailing effects
- GPU acceleration for performance
- Web version using WebGL
- VR/AR support for immersive experiences
- Neural network integration for AI-generated patterns

### Phase 3 (Experimental)
- Real-time data visualization integration
- Collaborative multi-user experiences
- Biometric integration (heart rate, brainwaves)
- Advanced physics simulation

## 🏆 Key Features

✅ **Real-time Performance**: 60fps rendering with thousands of squares  
✅ **Modular Architecture**: Clean separation of concerns, easily extensible  
✅ **Audio Reactivity**: Professional-grade music visualization  
✅ **Interactive Controls**: Live parameter adjustment  
✅ **Multiple Visual Modes**: 4 distortion types × 10 color schemes = 40 combinations  
✅ **Cross-platform**: Works on Windows, macOS, Linux  
✅ **Graceful Degradation**: Works without audio libraries  
✅ **Fullscreen Support**: Immersive viewing experience  

## 🎨 Use Cases

- **Live Music Visualization**: DJ performances, concerts, parties
- **Digital Art Creation**: Generative art projects, installations
- **Meditation/Relaxation**: Calming visual experiences
- **Educational**: Mathematics and programming demonstrations
- **Screensaver**: Beautiful ambient desktop backgrounds
- **Content Creation**: Background visuals for videos, streams

## 🤝 Contributing

The project is designed for easy extension:
- Add new distortion algorithms in `distortions.py`
- Create new color schemes in `colors.py`
- Enhance audio analysis in `audio_analyzer.py`
- Build new demo configurations in `demos.py`

---

**Distorsion Movement** transforms mathematical concepts into living, breathing art that responds to sound and user interaction. It's both a technical showcase of real-time graphics programming and a creative tool for generating endless visual experiences.
