"""
Web-compatible version of the deformed grid generative art application.
This file is required by pygbag for web deployment.
"""

import asyncio
import pygame
import sys
import os

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from distorsion_movement.deformed_grid import DeformedGrid
from distorsion_movement.enums import DistortionType, ColorScheme, ShapeType

# Global variables for the game state
grid = None
running = True
distortion_types = None
current_distortion_index = 0
color_schemes = None  
current_color_index = 0

def init_game():
    """Initialize the game - called once at startup"""
    global grid, distortion_types, color_schemes, current_distortion_index, current_color_index
    
    print("🎨 Initializing Deformed Grid Web App...")
    print("🌐 Running in web browser mode")
    
    # Create the deformed grid with web-optimized settings
    # (DeformedGrid will handle pygame initialization)
    grid = DeformedGrid(
        dimension=32,  # Smaller for better web performance
        cell_size=16,
        canvas_size=(800, 600),  # Fixed size for web
        distortion_strength=0.3,
        distortion_fn="circular",
        color_scheme="rainbow",
        color_animation=True,
        audio_reactive=False,  # Disable audio for web compatibility
        shape_type="square",
        mixed_shapes=False
    )
    
    # Initialize control arrays
    distortion_types = [t.value for t in DistortionType]
    color_schemes = [c.value for c in ColorScheme]
    
    # Find current indices
    try:
        current_distortion_index = distortion_types.index(grid.distortion_fn)
    except ValueError:
        current_distortion_index = 0
        
    try:
        current_color_index = color_schemes.index(grid.color_scheme)
    except ValueError:
        current_color_index = 0
    
    print("🎮 Controls:")
    print("- SPACE: Change distortion type")
    print("- C: Change color scheme") 
    print("- A: Toggle color animation")
    print("- H: Change shape type")
    print("- Shift+H: Toggle mixed shapes")
    print("- +/-: Adjust distortion intensity")
    print("- R: Regenerate parameters")
    print("- I: Toggle help")
    print("- D: Toggle status display")

def handle_events():
    """Handle pygame events"""
    global running, current_distortion_index, current_color_index, distortion_types, color_schemes
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Change distortion type
                current_distortion_index = (current_distortion_index + 1) % len(distortion_types)
                grid.distortion_fn = distortion_types[current_distortion_index]
                print(f"Distortion: {grid.distortion_fn}")
            elif event.key == pygame.K_c:
                # Change color scheme
                current_color_index = (current_color_index + 1) % len(color_schemes)
                grid.color_scheme = color_schemes[current_color_index]
                grid._generate_base_colors()
                print(f"Color scheme: {grid.color_scheme}")
            elif event.key == pygame.K_a:
                # Toggle color animation
                grid.color_animation = not grid.color_animation
                status = "enabled" if grid.color_animation else "disabled"
                print(f"Color animation: {status}")
            elif event.key == pygame.K_h and (pygame.key.get_pressed()[pygame.K_LSHIFT] or pygame.key.get_pressed()[pygame.K_RSHIFT]):
                # Toggle mixed shapes mode (Shift+H)
                grid.mixed_shapes = not grid.mixed_shapes
                grid._generate_shape_types()
                mode = "mixed shapes" if grid.mixed_shapes else "single shape"
                print(f"Mode: {mode} ({grid.shape_type})")
            elif event.key == pygame.K_h:
                # Change shape type (H alone)
                shape_types = [s.value for s in ShapeType]
                current_shape_index = shape_types.index(grid.shape_type) if grid.shape_type in shape_types else 0
                current_shape_index = (current_shape_index + 1) % len(shape_types)
                grid.shape_type = shape_types[current_shape_index]
                grid._generate_shape_types()
                print(f"Shape: {grid.shape_type}")
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                # Increase distortion intensity
                grid.distortion_strength = min(1.0, grid.distortion_strength + 0.1)
                grid.base_distortion_strength = grid.distortion_strength
                print(f"Intensity: {grid.distortion_strength:.1f}")
            elif event.key == pygame.K_MINUS:
                # Decrease distortion intensity
                grid.distortion_strength = max(0.0, grid.distortion_strength - 0.1)
                grid.base_distortion_strength = grid.distortion_strength
                print(f"Intensity: {grid.distortion_strength:.1f}")
            elif event.key == pygame.K_r:
                # Regenerate parameters
                grid._generate_distortions()
                grid._generate_base_colors()
                grid._generate_shape_types()
                print("Parameters regenerated")
            elif event.key == pygame.K_i:
                # Toggle help display
                grid.show_help = not grid.show_help
                status = "shown" if grid.show_help else "hidden"
                print(f"Help: {status}")
            elif event.key == pygame.K_d:
                # Toggle status display
                grid.show_status = not grid.show_status
                status = "shown" if grid.show_status else "hidden"
                print(f"Status: {status}")

async def main():
    """Main async game loop - required by pygbag"""
    global grid, running
    
    # Initialize the game
    init_game()
    
    # Main game loop
    while running:
        # Handle events
        handle_events()
        
        # Update game state
        grid.update()
        
        # Render the frame
        grid.render()
        
        # CRITICAL: This await is required for pygbag web compatibility
        await asyncio.sleep(0)
    
    # Cleanup when exiting
    print("🔄 Cleaning up...")
    if grid.audio_analyzer:
        grid.audio_analyzer.stop_audio_capture()
    
    pygame.quit()

# Entry point - required by pygbag
if __name__ == "__main__":
    # This will be called by pygbag
    asyncio.run(main())