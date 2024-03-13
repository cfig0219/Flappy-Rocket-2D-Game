import pygame
import random
import sys
import math
import pygame.mixer # for sounds

# Initialize Pygame
pygame.init()

# Set the window dimensions
windowWidth = 800
windowHeight = 600

# Set the bird properties
birdWidth = 80
birdHeight = 80
birdHitboxWidth = 40  # Reduced hitbox width
birdHitboxHeight = 40  # Reduced hitbox height
birdX = 100
birdY = windowHeight // 2 - birdHeight // 2
gravity = 0.4
jumpStrength = 7

# vertical variation of the planets
vertical_variation = 450  # Adjust this value as needed

# Set the circle properties
circleRadius = 150  # Updated to 150

# Set the colors
white = (255, 255, 255)

# Create the game window
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Flappy Rocket")

# Load the background image
background_image = pygame.image.load("Photos/Stars.jpg")
background_image = pygame.transform.scale(background_image, (windowWidth, windowHeight))

# Load the bird image
bird_image = pygame.image.load("Photos/Spacecraft_center.png")
bird_image = pygame.transform.scale(bird_image, (birdWidth, birdHeight))

# Load the celestial body images
earth_image = pygame.image.load("Photos/Earth_highRes.png")
jupiter_image = pygame.image.load("Photos/Jupiter_highRes.png")
mars_image = pygame.image.load("Photos/Mars_highRes.png")
mercury_image = pygame.image.load("Photos/Mercury_highRes.png")
moon_image = pygame.image.load("Photos/Moon_highRes.png")
neptune_image = pygame.image.load("Photos/Neptune_highRes.png")
saturn_image = pygame.image.load("Photos/Saturn_highRes.png")
uranus_image = pygame.image.load("Photos/Uranus_highRes.png")
venus_image = pygame.image.load("Photos/Venus_highRes.png")

# Resize celestial body images to match the circle radius
earth_image = pygame.transform.scale(earth_image, (2 * circleRadius, 2 * circleRadius))
jupiter_image = pygame.transform.scale(jupiter_image, (3.5 * circleRadius, 3.5 * circleRadius))
mars_image = pygame.transform.scale(mars_image, (1.6 * circleRadius, 1.6 * circleRadius))
mercury_image = pygame.transform.scale(mercury_image, (1.2 * circleRadius, 1.2 * circleRadius))
moon_image = pygame.transform.scale(moon_image, (1.1 * circleRadius, 1.1 * circleRadius))
neptune_image = pygame.transform.scale(neptune_image, (2.4 * circleRadius, 2.4 * circleRadius))
saturn_image = pygame.transform.scale(saturn_image, (7.2 * circleRadius, 3 * circleRadius))
uranus_image = pygame.transform.scale(uranus_image, (2.5 * circleRadius, 2.5 * circleRadius))
venus_image = pygame.transform.scale(venus_image, (2 * circleRadius, 2 * circleRadius))

# Load the font
font = pygame.font.Font(None, 36)

# Clock for controlling game speed
clock = pygame.time.Clock()

def drawCircle(x, gapY, image):
    circleY = gapY + circleRadius
    window.blit(image, (x - circleRadius, circleY - circleRadius))

def displayGameOver():
    game_over_text = font.render("Game Over!", True, white)
    window.blit(game_over_text, (windowWidth // 2 - game_over_text.get_width() // 2, windowHeight // 2 - game_over_text.get_height() // 2))

def checkCollisionCelestialBody(circleX, gapY, image):
    # Calculate the positions of the celestial body object
    celestial_body_x = circleX - circleRadius
    celestial_body_y = gapY

    # Calculate the center of the celestial body
    celestial_center_x = celestial_body_x + circleRadius
    celestial_center_y = celestial_body_y + circleRadius

    # Calculate the distance between the centers of the celestial body and the bird
    bird_center_x = birdX + birdHitboxWidth // 2  # Use birdHitboxWidth for hitbox center calculation
    bird_center_y = birdY + birdHitboxHeight // 2  # Use birdHitboxHeight for hitbox center calculation

    distance_x = bird_center_x - celestial_center_x
    distance_y = bird_center_y - celestial_center_y
    distance = math.sqrt(distance_x * distance_x + distance_y * distance_y)

    # Calculate the radius of the celestial body
    celestial_radius = circleRadius

    # Check for collision based on the distance between the centers and the radius of the celestial body
    return distance < celestial_radius + birdHitboxWidth // 2

# Global variable to track the time when the message was displayed
show_message_start_time = 0
show_message_duration = 3000  # 3 seconds (in milliseconds)

def displayMessageCentered(text):
    # Render the message as text on the window
    message_text = font.render(text, True, white)
    x = windowWidth // 2 - message_text.get_width() // 2
    y = windowHeight // 2 - message_text.get_height() // 2
    window.blit(message_text, (x, y))

def displayTimer(milliseconds):
    global show_message_start_time

    # Convert milliseconds to kilometers
    kilometers = milliseconds * 100

    # Render the distance timer as text on the window
    timer_text = font.render("Distance: {} km".format(kilometers), True, white)
    window.blit(timer_text, (windowWidth - timer_text.get_width() - 10, 10))

    # Check if it's time to show the "Press 'w' to Jump" message
    current_time = pygame.time.get_ticks()
    if show_message_start_time == 0:
        show_message_start_time = current_time

    if current_time - show_message_start_time < show_message_duration:
        # Render the "Press 'w' to Jump" message in the center of the screen
        displayMessageCentered("Press 'w' to Jump")
    if current_time > 4000 and current_time < 8000:
        # Render the "Press 'w' to Jump" message in the center of the screen
        displayMessageCentered("Press Spacebar to Reset")
    else:
        # Reset the start time to 0 to stop displaying the message
        displayMessageCentered("")
        
def main(circleX):
    global birdY, gravity

    gapY = windowHeight // 2
    gapY2 = random.uniform(circleRadius, windowHeight - circleRadius - vertical_variation)

    game_over = False
    score = 0
    
    # explosion
    explosion_image = pygame.image.load("Photos/explosion.png")
    explosion_image = pygame.transform.scale(explosion_image, (birdWidth, birdHeight))
    
    # Load the explosion sound
    explosion_sound = pygame.mixer.Sound("Sound/blast.wav")
    
    # Rocket exhaust sound and image
    exhaust_image = pygame.image.load("Photos/exhaust.png")
    exhaust_image = pygame.transform.scale(exhaust_image, (birdWidth // 2, birdHeight // 2))
    rocket_sound = pygame.mixer.Sound("Sound/rocket.wav")

    # Create lists to store the randomly selected celestial body images for each circle
    celestial_images = [earth_image, jupiter_image, mars_image, mercury_image, moon_image, neptune_image, saturn_image, uranus_image, venus_image]
    selected_celestial_image = random.choice(celestial_images)
    selected_celestial_image2 = random.choice(celestial_images)

    # Variable to store the bird's initial Y position
    initial_birdY = birdY

    # Timer variables
    timer_start = pygame.time.get_ticks()  # Get the initial time
    timer_elapsed = 0

    # Variables to keep track of planet visibility status
    planet1_visible = True
    planet2_visible = True

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Check for 'w' key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            gravity = -jumpStrength

        # Update bird's vertical position
        birdY += gravity
        gravity += 0.3

        # Limit the bird's position to the bottom of the window
        if birdY > windowHeight - birdHeight:
            birdY = windowHeight - birdHeight
            gravity = 0.3  # Reset gravity when the bird hits the ground

        # Limit the bird's position to the top of the window (290)
        if birdY < 0:
            birdY = 0
            gravity = 0.3  # Reset gravity to make the bird fall

        # Check for game over if bird's Y coordinate exceeds 400
        if birdY > 500:
            game_over = True

        # Check for successful pass (score) between the two circles
        if circleX < birdX < circleX + circleRadius:
            if not (gapY < birdY < gapY + circleRadius) and not (gapY2 < birdY < gapY2 + circleRadius):
                score += 1

        # Draw background
        window.blit(background_image, (0, 0))

        # Draw first circle with the selected celestial body image
        if planet1_visible:
            drawCircle(circleX, gapY, selected_celestial_image)

        # Draw second circle with the selected celestial body image
        if planet2_visible:
            drawCircle(circleX + windowWidth // 2, gapY2, selected_celestial_image2)

        # Draw exhaust image to the left of the bird if 'w' key is pressed
        if keys[pygame.K_w]:
            window.blit(exhaust_image, (birdX - birdWidth // 2, birdY + birdHeight // 4))
            rocket_sound.play()  # Play the rocket sound

        # Draw bird
        window.blit(bird_image, (birdX, birdY))

        # Move both circles to the left
        circleX -= 5
        circleX2 = circleX + windowWidth // 2

        # Check for collision with celestial body for both circles
        if checkCollisionCelestialBody(circleX, gapY, selected_celestial_image):
            game_over = True
        if checkCollisionCelestialBody(circleX + windowWidth // 2, gapY2, selected_celestial_image2):
            game_over = True

        # Check if first circle has moved off-screen and reset its position and select a new celestial body image
        if circleX2 + circleRadius < 0:
            circleX = 800 + circleX2 + windowWidth // 2  # horizontal distance
            gapY = random.uniform(circleRadius + 300, windowHeight - circleRadius - vertical_variation)
            gapY2 = random.uniform(circleRadius + 300, windowHeight - circleRadius - vertical_variation)
            selected_celestial_image = random.choice(celestial_images)
            selected_celestial_image2 = random.choice(celestial_images)
            planet1_visible = True
            planet2_visible = True

        # Calculate the bird's height above the initial position
        bird_height_diff = initial_birdY - birdY

        # Calculate and render the timer
        timer_elapsed = pygame.time.get_ticks() - timer_start
        displayTimer(timer_elapsed)

        pygame.display.update()
        clock.tick(60)

    # Game over loop
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_over = False  # Reset the game if spacebar is pressed
                circleX = windowWidth
                birdY = windowHeight // 2 - birdHeight // 2
                gravity = 0.4
                planet1_visible = False
                planet2_visible = False
                main(circleX)  # Restart the game loop

        window.blit(background_image, (0, 0))

        # Draw first circle with the selected celestial body image
        if planet1_visible:
            drawCircle(circleX, gapY, selected_celestial_image)

        # Draw second circle with the selected celestial body image
        if planet2_visible:
            drawCircle(circleX + windowWidth // 2, gapY2, selected_celestial_image2)

        # Check for collision with celestial body for both circles
        if checkCollisionCelestialBody(circleX, gapY, selected_celestial_image):
            game_over = True
            window.blit(explosion_image, (birdX, birdY))  # Display explosion image
            explosion_sound.play()  # Play the explosion sound
        if checkCollisionCelestialBody(circleX + windowWidth // 2, gapY2, selected_celestial_image2):
            game_over = True
            window.blit(explosion_image, (birdX, birdY))  # Display explosion image
            explosion_sound.play()  # Play the explosion sound

        window.blit(bird_image, (birdX, birdY))
        displayGameOver()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    # Set initial circleX value
    circleX = windowWidth

    main(circleX)
