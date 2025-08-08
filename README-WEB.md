# 🌐 Deformed Grid - Web Deployment Guide

This guide shows how to run the Deformed Grid generative art application in web browsers using [pygbag](https://github.com/pygame-web/pygbag).

## 🚀 Quick Start

### 1. Install pygbag

```bash
pip install pygbag --user --upgrade
```

### 2. Run the web version

From the project root directory:

```bash
pygbag .
```

This will:
- Build the web-compatible version
- Start a local web server
- Open your browser to `http://localhost:8000`

## 🎮 Controls

The web version supports all the same controls as the desktop version:

### Navigation & Interface
- **SPACE**: Change distortion type
- **C**: Change color scheme  
- **A**: Toggle color animation
- **H**: Change shape type
- **Shift+H**: Toggle mixed shapes mode
- **+/-**: Adjust distortion intensity
- **R**: Regenerate parameters
- **I**: Toggle help display
- **D**: Toggle status display

### Features Available in Web Mode
- ✅ All distortion types (circular, sine, perlin, random, etc.)
- ✅ All color schemes (rainbow, neon, fire, ocean, etc.)
- ✅ All shape types (squares, circles, triangles, hexagons, pentagons, stars, diamonds)
- ✅ Color animations
- ✅ Real-time parameter adjustments
- ✅ Interactive controls

### Features Disabled in Web Mode
- ❌ Audio reactivity (microphone not accessible in web browsers)
- ❌ GIF recording (numpy/imageio not available)
- ❌ Image saving (file system access limited)

## 🔧 Advanced Options

### Custom Build Options

```bash
# Build only (don't run server)
pygbag --build .

# Custom port
pygbag --port 8080 .

# Different app name
pygbag --app_name "Generative Art" .

# Build for itch.io
pygbag --archive .
```

### Performance Settings

For better web performance, the main.py uses optimized settings:
- Grid dimension: 48x48 (instead of 64x64)
- Cell size: 12px
- Canvas size: 800x600
- Audio reactivity: disabled

## 📂 File Structure for Web

The web deployment uses this structure:

```
artwithcoding/
├── main.py                 # 🌐 Web entry point (required by pygbag)
├── distorsion_movement/    # Core modules (web-compatible)
│   ├── deformed_grid.py    # Main application (with web adaptations)
│   ├── colors.py           # Color generation
│   ├── distortions.py      # Distortion algorithms  
│   ├── shapes.py           # Shape rendering
│   └── enums.py            # Type definitions
└── requirements-web.txt    # Minimal dependencies
```

## 🔄 Development Workflow

### Testing Locally

```bash
# 1. Test the desktop version first
python distorsion_movement/demos.py

# 2. Test the web version
pygbag .

# 3. Navigate to http://localhost:8000
```

### Making Changes

1. Edit the code in `distorsion_movement/` modules
2. The `main.py` file handles web compatibility automatically
3. Test with `pygbag .`

### Debugging

Use the browser's developer console to see any JavaScript errors or Python print statements.

## 🎨 Available Demos

The web version automatically starts with an optimized configuration similar to:

```python
# Equivalent to this desktop demo:
grid = create_deformed_grid(
    dimension=48,
    cell_size=12, 
    distortion_strength=0.5,
    distortion_fn="circular",
    color_scheme="rainbow",
    color_animation=True,
    shape_type="square"
)
```

## 🌟 Tips for Web Users

1. **Performance**: The web version is optimized for smooth performance in browsers
2. **Mobile**: Works on mobile devices with touch controls
3. **Sharing**: You can host the generated files on any web server
4. **Fullscreen**: Use F11 in your browser for fullscreen experience

## 🔗 Deployment

### For itch.io

```bash
pygbag --archive .
# This creates build/web.zip ready for itch.io upload
```

### For GitHub Pages

```bash
pygbag --build .
# Upload the contents of build/web/ to your GitHub Pages repository
```

### For Custom Server

```bash
pygbag --build .
# Copy build/web/ contents to your web server
```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**: Make sure you're running from the project root directory
2. **Black screen**: Check browser console for JavaScript errors
3. **Slow performance**: Try reducing grid dimension in main.py
4. **Controls not working**: Make sure the canvas has focus (click on it)

### Browser Compatibility

- ✅ Chrome/Chromium 81+ (recommended)
- ✅ Firefox 79+
- ✅ Safari 14+
- ✅ Edge 81+

### Mobile Support

- ✅ iOS Safari 14+
- ✅ Chrome Mobile 81+
- ✅ Firefox Mobile 79+

The web version automatically adapts to different screen sizes and input methods.

## 🎯 Next Steps

1. Try the live demo: Run `pygbag .` and explore the controls
2. Customize the settings in `main.py` for your preferences  
3. Deploy to itch.io or your website to share with others
4. Contribute improvements back to the project!

---

Happy creative coding! 🎨✨