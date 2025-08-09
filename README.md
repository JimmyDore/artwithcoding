# 🎨 Distorsion Movement - Interactive Generative Art Engine

**Distorsion Movement** is a real-time generative art platform that creates mesmerizing visual experiences through geometrically deformed grids. The system generates dynamic, interactive artwork by applying mathematical distortions to regular grids of multiple geometric shapes (squares, circles, triangles, hexagons, pentagons, stars, diamonds)

[![Watch the demo on YouTube](https://img.youtube.com/vi/GWTRef1pFJo/0.jpg)](https://www.youtube.com/watch?v=GWTRef1pFJo)

## 🎯 Project Overview

### What It Does
The project creates animated grids of geometric shapes where each shape can be:
- **Multiple shape types** including squares, circles, triangles, hexagons, pentagons, stars, diamonds, and fractal Koch snowflakes
- **Geometrically distorted** using 20 mathematical functions (sine waves, Perlin noise, circular patterns, spiral warps, lens effects, moiré patterns, etc.)
- **Dynamically colored** using 20 schemes (rainbow, gradient, neon, cyberpunk, thermal, vaporwave, etc.)
- **Interactively controlled** through keyboard shortcuts and parameters
- **Mixed or uniform** shape distribution across the grid

### How It Works Technically

The core architecture follows a modular design with clear separation of concerns:

1. **Grid Generation**: Creates a regular NxN grid of geometric shapes with base positions
2. **Shape System**: Supports 7 different shape types with unified rendering architecture
3. **Distortion Engine**: Applies mathematical transformations to deform shape positions and orientations
4. **Color System**: Generates dynamic colors based on position, time, and color animation input
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


## 🏗️ Project Structure

```
distorsion_movement/
├── __init__.py              # Package entry point & public API
├── deformed_grid.py         # Main DeformedGrid class
├── enums.py                 # Type definitions (DistortionType, ColorScheme, ShapeType)
├── shapes.py                # Shape rendering system (7 shape types)
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

#### 🌈 **`colors.py`** - Color Generation
- 10 different color schemes (monochrome, gradient, rainbow, neon, etc.)
- Position-based color calculations
- Time-based color animations
- HSV/RGB color space conversions

#### 🌀 **`distortions.py`** - Geometric Engine 
- 7 distortion algorithms (random, sine, Perlin, circular, swirl, ripple, flow)
- Mathematical transformation functions
- Parameter generation for each square
- Time-based animation calculations

#### 🎮 **`demos.py`** - Usage Examples
- Pre-configured demonstration functions
- Shape-specific demos (stars, hexagons, triangles, etc.)
- Mixed vs single shape mode examples
- Simple API for quick setup
- Command-line interface with multiple demo options

#### 📝 **`enums.py`** - Type Safety
- `DistortionType`: RANDOM, SINE, PERLIN, CIRCULAR, SWIRL, RIPPLE, FLOW, PULSE, CHECKERBOARD, CHECKERBOARD_DIAGONAL, TORNADO, SPIRAL, SHEAR, LENS, SPIRAL_WAVE, NOISE_ROTATION, CURL_WARP, FRACTAL_NOISE, MOIRE, KALEIDOSCOPE_TWIST
- `ColorScheme`: MONOCHROME, BLACK_WHITE_RADIAL, BLACK_WHITE_ALTERNATING, GRADIENT, RAINBOW, COMPLEMENTARY, PASTEL, NEON, ANALOGOUS, CYBERPUNK, AURORA_BOREALIS, INFRARED_THERMAL, DUOTONE_ACCENT, DESERT, METALLICS, REGGAE, SUNSET, POP_ART, VAPORWAVE, CANDY_SHOP
- `ShapeType`: SQUARE, CIRCLE, TRIANGLE, HEXAGON, PENTAGON, STAR, DIAMOND, KOCH_SNOWFLAKE

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
    color_animation=True                       # Animate colors
)

grid.run_interactive()
```

## 🎛️ Interactive Controls

| Key | Action |
|-----|--------|
| `F` | Toggle fullscreen/windowed mode |
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
- **Koch Snowflake**: Fractal snowflake patterns with recursive geometry

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
- **Pulse**: Rhythmic radial breathing with wave-like pulsations
- **Checkerboard**: Alternating directional movement in grid pattern
- **Checkerboard Diagonal**: Diagonal tug-of-war between neighboring cells
- **Tornado**: Swirling vortex with increased rotation near center
- **Spiral**: Galaxy-like spiral motion with radius oscillation
- **Shear**: Horizontal/vertical skewing with wave propagation
- **Lens**: Dynamic magnification effect with moving focus point
- **Spiral Wave**: Combined circular ripples with rotational motion
- **Noise Rotation**: Positions stable, rotation driven by smooth noise field
- **Curl Warp**: Divergence-free swirling vector fields
- **Fractal Noise**: Multi-octave organic terrain-like distortions
- **Moiré**: Interference patterns from overlapping wave frequencies
- **Kaleidoscope Twist**: Radial symmetry with mirrored sectors and melting

### Color Schemes
- **Monochrome**: Single color variations
- **Black White Radial**: Center-to-edge black and white distribution
- **Black White Alternating**: Classic checkerboard pattern
- **Gradient**: Smooth diagonal color transitions
- **Rainbow**: Full spectrum cycling
- **Complementary**: Alternating opposite colors
- **Pastel**: Soft, muted tones
- **Neon**: Bright, electric colors
- **Analogous**: Harmonious neighboring hues with subtle variations
- **Cyberpunk**: Neon magenta and cyan with deep purple accents
- **Aurora Borealis**: Flowing teal, green, and purple like northern lights
- **Infrared Thermal**: Classic thermal imaging progression (blue→cyan→green→yellow→orange→red→white)
- **Duotone Accent**: Two main colors with rare bright yellow accent pops
- **Desert**: Sandy beige, warm orange, and muted brown tones
- **Metallics**: Smooth blends between gold, silver, and bronze
- **Reggae**: Green, yellow, and red in radial distribution
- **Sunset**: Warm gradient from yellow through orange and pink to purple
- **Pop Art**: Bright primary colors with bold black/white outlines
- **Vaporwave**: Soft pastel neons in lavender, cyan, peach, and pink
- **Candy Shop**: Sweet bubblegum pink, mint green, and lemon yellow

## 🔧 Dependencies

Install with:
```bash
pip install -r requirements.txt
```


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
# - Integration testing
```

## 🛣️ Development Roadmap

The project has an extensive roadmap for future enhancements (see `TODO.md`):

## 🏆 Key Features

✅ **Real-time Performance**: 60fps rendering with thousands of shapes  
✅ **Multiple Shape Types**: 8 geometric shapes (squares, circles, triangles, hexagons, pentagons, stars, diamonds, Koch snowflakes)  
✅ **Flexible Shape Modes**: Single shape or mixed shape grids  
✅ **Modular Architecture**: Clean separation of concerns, easily extensible  
✅ **Interactive Controls**: Live parameter adjustment and shape cycling  
✅ **Rich Visual Combinations**: 8 shapes × 20 distortions × 20 colors = 3,200 combinations  
✅ **Cross-platform**: Works on Windows, macOS, Linux  
✅ **Comprehensive Testing**: Full unit test coverage  
✅ **Fullscreen Support**: Immersive viewing experience

## 🤝 Contributing

The project is designed for easy extension:
- Add new distortion algorithms in `distortions.py`
- Create new shape types in `shapes.py`
- Create new color schemes in `colors.py`
- Build new demo configurations in `demos.py`
- Extend shape interactions and morphing capabilities

---

**Distorsion Movement** transforms mathematical concepts into living, breathing art that responds to user interaction. With support for multiple geometric shapes, flexible rendering modes, and comprehensive interactive controls, it's both a technical showcase of real-time graphics programming and a creative tool for generating endless visual experiences.
