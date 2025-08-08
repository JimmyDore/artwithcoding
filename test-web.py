"""
Minimal test version for debugging web deployment issues.
"""

import asyncio
import pygame
import math

# Global variables
screen = None
clock = None
running = True
time = 0.0

def init_game():
    """Initialize pygame for web"""
    global screen, clock
    
    print("🎨 Initializing minimal test...")
    
    # Initialize pygame
    pygame.init()
    
    # Create display - use standard web-friendly size
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test Web App")
    
    # Create clock
    clock = pygame.time.Clock()
    
    print("✅ Pygame initialized successfully")

def handle_events():
    """Handle pygame events"""
    global running
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                print("Space key pressed!")

def render():
    """Render a simple animated scene"""
    global screen, time
    
    # Clear screen with dark blue background
    screen.fill((20, 30, 60))
    
    # Draw a simple animated circle
    center_x = 400
    center_y = 300
    radius = 50 + int(30 * math.sin(time))
    
    # Rainbow color based on time
    r = int(128 + 127 * math.sin(time))
    g = int(128 + 127 * math.sin(time + 2.094))  # 2π/3
    b = int(128 + 127 * math.sin(time + 4.188))  # 4π/3
    color = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    pygame.draw.circle(screen, color, (center_x, center_y), radius)
    
    # Draw some text
    try:
        font = pygame.font.Font(None, 36)
        text = font.render("Web Test - Press SPACE", True, (255, 255, 255))
        text_rect = text.get_rect(center=(400, 100))
        screen.blit(text, text_rect)
    except:
        # Fallback if font fails
        pass
    
    # Update display
    pygame.display.flip()

def update():
    """Update game state"""
    global time
    time += 0.05

async def main():
    """Main async game loop - required by pygbag"""
    global running, clock
    
    # Initialize the game
    init_game()
    
    print("🚀 Starting main loop...")
    
    # Main game loop
    while running:
        # Handle events
        handle_events()
        
        # Update game state
        update()
        
        # Render the frame
        render()
        
        # Control frame rate
        clock.tick(60)
        
        # CRITICAL: This await is required for pygbag web compatibility
        await asyncio.sleep(0)
    
    # Cleanup when exiting
    print("🔄 Cleaning up...")
    pygame.quit()

# Entry point - required by pygbag
if __name__ == "__main__":
    # This will be called by pygbag
    asyncio.run(main())