# 🎨 Distorsion Movement - Interactive Generative Art Engine

**Distorsion Movement** is a real-time generative art platform that creates mesmerizing visual experiences through geometrically deformed grids. The system generates dynamic, interactive artwork by applying mathematical distortions to regular grids of multiple geometric shapes (squares, circles, triangles, hexagons, pentagons, stars, diamonds), with optional audio-reactive capabilities for music visualization.

[![Watch the demo on YouTube](https://img.youtube.com/vi/GWTRef1pFJo/0.jpg)](https://www.youtube.com/watch?v=GWTRef1pFJo)

## 🎯 Project Overview

### What It Does
The project creates animated grids of geometric shapes where each shape can be:
- **Multiple shape types** including squares, circles, triangles, hexagons, pentagons, stars, and diamonds
- **Geometrically distorted** using mathematical functions (sine waves, Perlin noise, circular patterns)
- **Dynamically colored** using various schemes (rainbow, gradient, neon, temperature-based, etc.)
- **Audio-reactive** to music and sound input in real-time
- **Interactively controlled** through keyboard shortcuts and parameters
- **Mixed or uniform** shape distribution across the grid

### How It Works Technically

The core architecture follows a modular design with clear separation of concerns:

1. **Grid Generation**: Creates a regular NxN grid of geometric shapes with base positions
2. **Shape System**: Supports 7 different shape types with unified rendering architecture
3. **Distortion Engine**: Applies mathematical transformations to deform shape positions and orientations
4. **Color System**: Generates dynamic colors based on position, time, and audio input
5. **Audio Analysis**: Real-time FFT analysis of microphone input to extract bass, mids, highs, and beat detection
6. **Rendering**: Real-time pygame-based visualization with 60fps target

### Mathematical Foundation

The distortions are based on several mathematical approaches:
- **Sine Wave Distortions**: `sin(x * frequency + phase) * amplitude`
- **Perlin Noise**: Smooth, organic-looking deformations
- **Circular Distortions**: Radial distortions from center points
- **Swirl Distortions**: Rotational vortex effects around the canvas center
- **Ripple Distortions**: Concentric waves with tangential displacement
- **Flow Distortions**: Curl-noise vector fields for organic movement
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
├── deformed_grid.py         # Main DeformedGrid class
├── enums.py                 # Type definitions (DistortionType, ColorScheme, ShapeType)
├── shapes.py                # Shape rendering system (7 shape types)
├── audio_analyzer.py        # Real-time audio analysis & FFT processing
├── colors.py                # Color generation algorithms
├── distortions.py           # Geometric distortion algorithms
├── demos.py                 # Demo functions & usage examples
├── tests/                   # Comprehensive unit tests
│   ├── test_shapes.py       # Shape rendering tests
│   ├── test_enums.py        # Enum validation tests
│   ├── test_deformed_grid.py # Grid functionality tests
│   └── ...                  # Other test modules
└── README.md               # This file
```

### Module Responsibilities

#### 🎨 **`deformed_grid.py`** - Core Engine
- Main `DeformedGrid` class that orchestrates everything
- Pygame rendering loop and event handling
- Grid generation and position calculations
- Shape type management and rendering coordination
- Animation timing and state management
- Fullscreen/windowed mode switching
- Interactive controls (keyboard shortcuts, shape cycling)

#### 🔷 **`shapes.py`** - Shape Rendering System
- Unified rendering architecture for 7 geometric shapes
- Rotation and scaling support for all shape types
- Mathematically precise shape generation (triangles, hexagons, stars, etc.)
- Consistent interface with fallback error handling
- Optimized drawing functions using pygame primitives

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
- 7 distortion algorithms (random, sine, Perlin, circular, swirl, ripple, flow)
- Mathematical transformation functions
- Parameter generation for each square
- Time-based animation calculations
- Audio-reactive distortion intensity

#### 🎮 **`demos.py`** - Usage Examples
- Pre-configured demonstration functions
- Shape-specific demos (stars, hexagons, triangles, etc.)
- Mixed vs single shape mode examples
- Simple API for quick setup
- Command-line interface with multiple demo options

#### 📝 **`enums.py`** - Type Safety
- `DistortionType`: RANDOM, SINE, PERLIN, CIRCULAR, SWIRL, RIPPLE, FLOW
- `ColorScheme`: MONOCHROME, GRADIENT, RAINBOW, COMPLEMENTARY, TEMPERATURE, PASTEL, NEON, OCEAN, FIRE, FOREST
- `ShapeType`: SQUARE, CIRCLE, TRIANGLE, HEXAGON, PENTAGON, STAR, DIAMOND

## 🚀 Quick Start

### Basic Usage
```python
from distorsion_movement import quick_demo

# Launch with default settings
quick_demo()
```

### Advanced Configuration
```python
from distorsion_movement import DeformedGrid, DistortionType, ColorScheme, ShapeType

# Create custom grid with shapes
grid = DeformedGrid(
    dimension=64,                               # 64x64 grid
    cell_size=12,                              # 12px shapes
    distortion_strength=0.7,                   # 70% distortion
    distortion_fn=DistortionType.SINE.value,   # Sine wave distortion
    color_scheme=ColorScheme.NEON.value,       # Neon colors
    shape_type=ShapeType.STAR.value,           # Star shapes
    mixed_shapes=False,                        # Single shape type
    audio_reactive=True,                       # Enable audio reactivity
    color_animation=True                       # Animate colors
)

grid.run_interactive()
```

### Shape Configuration Examples
```python
# Mixed shapes grid (variety of shapes)
mixed_grid = DeformedGrid(
    dimension=80,
    shape_type="hexagon",      # Base shape type
    mixed_shapes=True,         # Enable shape variety
    color_scheme="rainbow"
)

# Single shape type (all circles)
circle_grid = DeformedGrid(
    dimension=60,
    shape_type="circle",       # Only circles
    mixed_shapes=False,        # Uniform shapes
    distortion_fn="circular"
)
```

### Available Demo Functions
```python
from distorsion_movement.demos import (
    quick_demo, fullscreen_demo, audio_reactive_demo,
    star_demo, hexagon_demo, triangle_demo, shapes_showcase_demo
)

quick_demo()           # Basic windowed demo
fullscreen_demo()      # Mixed shapes fullscreen experience  
star_demo()            # Star shapes only
hexagon_demo()         # Hexagon patterns
triangle_demo()        # Triangle formations
shapes_showcase_demo() # Mixed shapes showcase
audio_reactive_demo()  # Music visualization with hexagons
```

## 🎛️ Interactive Controls

| Key | Action |
|-----|--------|
| `F` | Toggle fullscreen/windowed mode |
| `M` | Toggle audio reactivity on/off |
| `C` | Cycle through color schemes |
| `SPACE` | Cycle through distortion types |
| `H` | **NEW**: Cycle through shape types |
| `Shift+H` | **NEW**: Toggle mixed/single shape mode |
| `+/-` | Increase/decrease distortion intensity |
| `A` | Toggle color animation |
| `R` | Reset and regenerate all parameters |
| `S` | Save current image as PNG |
| `ESC` | Exit application |

## 🎨 Available Visual Modes

### Shape Types
- **Square**: Classic rectangular shapes (original)
- **Circle**: Perfect circular forms
- **Triangle**: Equilateral triangular shapes
- **Hexagon**: Six-sided geometric patterns
- **Pentagon**: Five-sided polygonal forms
- **Star**: Five-pointed star shapes
- **Diamond**: Rotated square formations

### Shape Modes
- **Single Shape**: All cells use the same shape type (uniform grid)
- **Mixed Shapes**: Random variety of shapes across the grid (dynamic variety)

### Distortion Types
- **Random**: Static chaotic displacement
- **Sine**: Smooth wave-based deformations
- **Perlin**: Organic, noise-based distortions  
- **Circular**: Radial distortions from center
- **Swirl**: Rotational vortex effects with periodic waves
- **Ripple**: Concentric wave patterns with tangential movement
- **Flow**: Smooth curl-noise vector fields for organic flow

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

Run the comprehensive test suite:
```bash
# Run all tests
python -m pytest distorsion_movement/tests/ -v

# Run specific test modules
python -m pytest distorsion_movement/tests/test_shapes.py -v      # Shape rendering tests
python -m pytest distorsion_movement/tests/test_enums.py -v       # Enum validation tests
python -m pytest distorsion_movement/tests/test_deformed_grid.py -v # Grid functionality tests

# Test coverage includes:
# - Shape rendering and rotation
# - Grid generation and management
# - Color schemes and animations
# - Distortion algorithms
# - Audio analysis components
# - Integration testing
```

## 🛣️ Development Roadmap

The project has an extensive roadmap for future enhancements (see `TODO.md`):

### Phase 1 (High Priority)
- Mouse interaction (attraction/repulsion effects)
- ✅ **COMPLETED**: Multiple shape types (circles, triangles, hexagons, stars, etc.)
- Motion blur and glow effects
- GIF/MP4 export capabilities
- Preset scene system
- Shape morphing and transformation animations

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

✅ **Real-time Performance**: 60fps rendering with thousands of shapes  
✅ **Multiple Shape Types**: 7 geometric shapes (squares, circles, triangles, hexagons, pentagons, stars, diamonds)  
✅ **Flexible Shape Modes**: Single shape or mixed shape grids  
✅ **Modular Architecture**: Clean separation of concerns, easily extensible  
✅ **Audio Reactivity**: Professional-grade music visualization  
✅ **Interactive Controls**: Live parameter adjustment and shape cycling  
✅ **Rich Visual Combinations**: 7 shapes × 7 distortions × 10 colors = 490 combinations  
✅ **Cross-platform**: Works on Windows, macOS, Linux  
✅ **Comprehensive Testing**: Full unit test coverage  
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
- Create new shape types in `shapes.py`
- Create new color schemes in `colors.py`
- Enhance audio analysis in `audio_analyzer.py`
- Build new demo configurations in `demos.py`
- Extend shape interactions and morphing capabilities

---

**Distorsion Movement** transforms mathematical concepts into living, breathing art that responds to sound and user interaction. With support for multiple geometric shapes, flexible rendering modes, and comprehensive interactive controls, it's both a technical showcase of real-time graphics programming and a creative tool for generating endless visual experiences.
