# New Shapes Implementation Plan

## Overview
We're extending the DeformedGrid system to support multiple shape types beyond just squares. This will add visual variety and enable shape morphing animations.

## Current System Analysis
- **Current Shape**: Only squares (drawn as rotated polygons)
- **Rendering Method**: `_draw_deformed_square()` in `DeformedGrid` class
- **Drawing**: Uses `pygame.draw.polygon()` for rotated squares
- **Position System**: Each cell has (x, y, rotation) from distortion engine
- **Colors**: Handled by `ColorGenerator` with various schemes

## Implementation Plan

### Phase 1: Core Shape System
1. **Add ShapeType Enum** (`enums.py`)
   - SQUARE (current default)
   - CIRCLE
   - TRIANGLE
   - HEXAGON
   - STAR
   - PENTAGON
   - DIAMOND

2. **Create Shape Renderer Module** (`shapes.py`)
   - Abstract base class for shape rendering
   - Concrete implementations for each shape type
   - Support for rotation, size, and position
   - Consistent interface: `draw(surface, x, y, rotation, size, color)`

### Phase 2: Grid Integration
3. **Extend DeformedGrid Class**
   - Add `shape_type` parameter to constructor
   - Replace `_draw_deformed_square()` with `_draw_shape()`
   - Support shape mixing (different shapes per cell)
   - Add shape change controls to interactive mode

4. **Update Demos**
   - Add shape showcase to fullscreen demo
   - Allow cycling through shape types
   - Show mixed shape grids

### Phase 3: Advanced Features
5. **Shape Morphing System**
   - Interpolation between different shapes
   - Breathing/pulsing animations
   - Size variation for depth perception
   - Time-based morphing patterns

6. **Shape Variations**
   - Variable polygon sides (3-12)
   - Star shapes with different point counts
   - Organic shapes using bezier curves
   - Custom polygon definitions

## Technical Details

### Shape Renderer Architecture
```python
class ShapeRenderer:
    @staticmethod
    def draw_circle(surface, x, y, rotation, size, color):
        # pygame.draw.circle() implementation
    
    @staticmethod
    def draw_triangle(surface, x, y, rotation, size, color):
        # Calculate triangle vertices with rotation
    
    @staticmethod
    def draw_hexagon(surface, x, y, rotation, size, color):
        # Calculate hexagon vertices with rotation
    
    # ... other shapes
```

### Grid Integration
- Replace `_draw_deformed_square()` with `_draw_shape()`
- Add shape selection logic
- Support per-cell shape types (for mixed grids)
- Maintain backward compatibility

### Controls Extension
- **H**: Cycle through shape types (H for sHapes)
- **Shift+H**: Toggle mixed shape mode
- **Ctrl+H**: Enable shape morphing
- Existing controls remain unchanged (S still saves images)

## Implementation Steps

### Step 1: Shape Type Enum
- Add `ShapeType` enum to `enums.py`
- Write unit tests for enum

### Step 2: Shape Renderer Module
- Create `shapes.py` with all shape drawing functions
- Implement 7 basic shapes with rotation support
- Write comprehensive unit tests

### Step 3: Grid Modification
- Add shape_type parameter to DeformedGrid
- Replace square-specific code with generic shape rendering
- Add shape cycling to interactive controls
- Update constructor and parameter handling

### Step 4: Demo Updates
- Modify fullscreen demo to showcase shapes
- Add shape cycling demonstration
- Show mixed shape grids

### Step 5: Advanced Features
- Implement shape morphing system
- Add size variation algorithms
- Create breathing/pulsing animations

## Testing Strategy
- Unit tests for each shape renderer function
- Integration tests for grid with different shapes
- Visual regression tests (save/compare images)
- Performance tests (rendering speed with different shapes)
- Interactive testing of all new controls

## File Structure Changes
```
distorsion_movement/
├── enums.py              # Add ShapeType enum
├── shapes.py             # NEW: Shape rendering module
├── deformed_grid.py      # Modified: Add shape support
├── demos.py              # Modified: Add shape demos
└── tests/
    ├── test_enums.py     # Add ShapeType tests
    ├── test_shapes.py    # NEW: Shape renderer tests
    ├── test_deformed_grid.py  # Modified: Add shape tests
    └── test_integration.py    # Modified: Add shape integration tests
```

## Success Criteria
1. ✅ All 7 basic shapes render correctly with rotation
2. ✅ Shape cycling works in interactive mode
3. ✅ Mixed shape grids display properly
4. ✅ Performance remains acceptable (60 FPS target)
5. ✅ All unit tests pass with 95%+ coverage
6. ✅ Backward compatibility maintained
7. ✅ Demo showcases all new features effectively

## Future Enhancements (Beyond Initial Implementation)
- 3D-looking shapes with perspective
- Text characters as shapes
- Fractal shapes with recursive patterns
- Shape physics (collision, gravity)
- User-defined custom shapes
- Shape particle systems