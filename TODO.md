## Bugs 
- [X] shift + h is not working
- [X] It seems I cannot go back to monochrome
- [X] Fix or remove useless tests
- [X] Fix the cell size => Should also resize the grid

- Distorsions improvements : 
  - [ ] Fix the lens distortion 
      => Always the same size of lens based on the cell size
      => Solution : the size of the lens should be based on the cell/grid size
  - [ ] Fix the kaleidoscope twist => It's not working well in full screen

- Shapes improvements : 
  - [ ] Koch snowflake => Looks awsome but very laggy

- Colors improvements : 
  - [ ] Aurora borealis could maybe be improved, more red

## Current roadmap

- [X] Global README to explain the project 
- [X] Write a few tests
- [X] Write a task file to run tests and to run the demos
- [X] Additional shape types (circles, triangles)
- [X] Open the command guide with a key
- [X] GIF/MP4 export
- [X] Add new distortion types (swirl, ripple, flow)
- [X] Add options to play with the cell size
- [X] Add the name of the distortion, the intensity, and the number of cells on the screen

- [X] Add an option to export the parameters of the current scene (just export the params.json file) and find a way to load it automatically when the app is launched. Maybe reuse the save image feature, and save a json file with the parameters. Maybe add an option to iterate through all saved scenes.

- [ ] Add new shape types
- [ ] Add new color schemes (inspire from pastel color in archive)
- [ ] Add new distortion types (take a look at the new_distortions_again.md file for more ideas)

- [ ] Get rid of the audio features, it's not working well
- [ ] Add a keyboard shortcut to do previous distorsion/shape/color scheme
- [ ] The menu is too big, on one column, maybe 2 columns now ? 

- [ ] Refactor the shapes, colors, and distorsions to be more modular and easier to add new ones. (one file for each type of distorsion, one file for each shape, one file for each color scheme)

- [ ] Clean up useless stuff in README.md (audio etc...)
- [ ] Clean up useless stuff in TODO.md

- Add in README: 
  - [ ] the new distorsions (from pulse, pulse not included)
  - [ ] the new shapes (from koch snowflake)
  - [ ] the new colors (from analogous)
  - [ ] the size guide (and mention it in the number of combinations possible)
  - [ ] the status display
  - [ ] how a distorsion function works, what parameters and what it basically does (compute next position and rotations based on ...)
  - [ ] the new indicators screen
  - [ ] the saved/load scenes feature

  - [ ] Save as mp4 feature

- [ ] Host on web ? pygbag https://github.com/pygame-web/pygbag
  - in a pull request, not working well
  - maybe need to migrate to webgl and use f*ckin' js ?

- [ ] Mouse interaction (attraction/repulsion)
  - in a pull request, not working well
- [ ] Audio reactive features
  - in a pull request, need to be redone from scratch
- [ ] Motion blur effects
- [ ] Preset scene system
- [ ] Particle systems



# 🎨 Deformed Grid - Epic Improvements Roadmap

## 🎵 **Audio-Reactive Features** - Not working that well
- **Real-time audio analysis** using FFT and pyaudio
- **Frequency separation**: Bass, mids, highs control different visual aspects
- **Beat detection** with synchronized flash effects
- **Audio → Visual mapping**:
  - 🥁 Bass (20-250Hz) → Distortion intensity
  - 🎸 Mids (250Hz-4kHz) → Color hue rotation
  - ✨ Highs (4kHz+) → Brightness boosts
  - 💥 Beat detection → White flash effects
  - 📢 Volume → Animation speed
- **Interactive controls**: Press 'M' to toggle audio reactivity

## 🎨 **Advanced Visual Effects**

### **Particle Systems**
- **Trailing sparks** behind moving squares
- **Glowing halos** around squares based on audio intensity
- **Energy fields** that connect nearby squares
- **Particle explosions** on beat detection
- **Floating particles** that react to distortions

### **Motion Blur & Glow Effects**
- **Motion blur trails** as squares move
- **Neon glow effects** that actually bleed light
- **Bloom/HDR effects** for bright colors
- **Ghost trails** showing previous positions
- **Chromatic aberration** for psychedelic effects

### **Post-Processing Filters**
- **Real-time blur/sharpen** filters
- **Color correction** and saturation boost
- **Vintage film effects** (grain, vignette)
- **Kaleidoscope/mirror** effects
- **Pixelation/retro** filters

## 🖱️ **Interactive Features**

### **Mouse Interaction**
- **Attraction/repulsion** - squares follow or flee from cursor
- **Paint mode** - click and drag to paint colors in real-time
- **Gravity wells** - create distortion fields with mouse clicks
- **Magnetic fields** - squares align like iron filings around cursor
- **Ripple effects** - wave propagation from click points

### **Touch/Multi-touch Support**
- **Tablet compatibility** for touch devices
- **Pinch-to-zoom** for closer inspection
- **Multi-finger gestures** for complex interactions
- **Pressure sensitivity** for drawing effects

## 🔺 **Shape Variety & Morphing**

### **Multiple Shapes**
- **Circles, triangles, hexagons, stars**
- **Custom polygons** with variable sides
- **Organic shapes** using bezier curves
- **3D-looking shapes** with perspective
- **Text characters** as shapes

### **Shape Morphing**
- **Squares → circles** transformation
- **Size variation** for depth perception
- **Shape interpolation** between different forms
- **Breathing/pulsing** shape animations
- **Fractal shapes** with recursive patterns

## 🌪️ **Advanced Distortion Types**

### **New Distortion Algorithms**
- **Spiral/vortex** effects with rotation fields
- **Fluid dynamics** simulation
- **Magnetic field** distortions
- **Gravitational** lensing effects
- **Turbulence** and noise-based distortions

### **Compound Distortions**
- **Multiple distortions** applied simultaneously
- **Distortion layering** with different intensities
- **Time-based distortion** sequences
- **Audio-reactive distortion** switching

## 🎮 **Gaming & Interactive Elements**

### **Preset Scenes**
- **Curated combinations** of colors, distortions, and effects
- **Genre-specific presets** (Electronic, Classical, Rock, etc.)
- **Mood-based themes** (Chill, Energetic, Psychedelic)
- **Time-of-day** adaptive themes

### **Randomization & AI**
- **"Surprise Me"** button for random combinations
- **Genetic algorithms** for evolving patterns
- **AI-generated** color palettes
- **Smart recommendations** based on music genre

## 💾 **Export & Sharing Features**

### **Media Export**
- **GIF/MP4 export** of animations
- **High-resolution rendering** (4K, 8K)
- **Frame-by-frame** export for video editing
- **Live streaming** integration
- **Screenshot burst mode**

### **Data Management**
- **Save/load presets** as JSON files
- **Color palette export** to Adobe/Figma formats
- **Batch generation** of hundreds of variations
- **Session recording** and playback
- **Cloud sync** for settings

## 🚀 **Performance & Technical**

### **Optimization**
- **GPU acceleration** using OpenGL/Metal
- **Multi-threading** for audio processing
- **Level-of-detail** rendering for performance
- **Memory optimization** for large grids
- **60fps guarantee** even with thousands of squares

### **Platform Support**
- **Web version** using WebGL
- **Mobile apps** (iOS/Android)
- **VR/AR support** for immersive experiences
- **Hardware controller** support (MIDI, game controllers)

## 🎯 **Special Effects**

### **Fractal & Mathematical Patterns**
- **Mandelbrot/Julia sets** integration
- **L-systems** for organic growth patterns
- **Cellular automata** (Conway's Game of Life)
- **Strange attractors** (Lorenz, Rössler)
- **Fibonacci spirals** and golden ratio patterns

### **Physics Simulation**
- **Collision detection** between squares
- **Spring systems** connecting squares
- **Fluid dynamics** for liquid-like behavior
- **Gravity simulation** with realistic physics
- **Electromagnetic** field visualization

## 🌈 **Extended Color Systems**

### **Advanced Color Schemes**
- **Perceptually uniform** color spaces (LAB, LUV)
- **Color harmony** rules (triadic, complementary, etc.)
- **Seasonal palettes** that change over time
- **Emotion-based** color mapping
- **Cultural color** themes from around the world

### **Dynamic Color Effects**
- **Color bleeding** between adjacent squares
- **Chromatic aberration** for retro effects
- **Color temperature** shifts
- **Saturation breathing** effects
- **Hue cycling** with musical harmony

## 🎪 **Experimental Features**

### **Generative Art Integration**
- **Style transfer** using neural networks
- **Procedural textures** on squares
- **Algorithmic composition** of patterns
- **Evolutionary art** that improves over time
- **Collaborative evolution** with user feedback

### **Data Visualization**
- **Real-time data** integration (stock prices, weather, etc.)
- **Social media sentiment** visualization
- **Network topology** representation
- **Scientific data** visualization modes
- **Biometric integration** (heart rate, brain waves)
