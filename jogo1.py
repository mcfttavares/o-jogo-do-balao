import pygame
import random
import math

# Pygame setup
pygame.init()

# Constants for game states
START, PLAYING, GAME_OVER = "START", "PLAYING", "GAME_OVER"
game_state = START

# Colors
custom_colour = (133, 218, 255)
custom_colour2 = (250, 56, 79)

# Screen setup
screen_width = 720
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("O Balão do João")

# Font setup
title_font = pygame.font.Font("Barlow-SemiBoldItalic.ttf", 90)
start_font = pygame.font.Font("Barlow-SemiBoldItalic.ttf", 74)
game_over_font = pygame.font.Font("Barlow-SemiBoldItalic.ttf", 74)
score_font = pygame.font.Font("Barlow-LightItalic.ttf", 65)
title_text = title_font.render('O Balão do João', True, custom_colour2)
start_text = start_font.render('START', True, custom_colour2)
game_over_text = game_over_font.render('GAME OVER!', True, custom_colour2)
title_rect = title_text.get_rect(center=(screen_width // 2, 270))
start_rect = start_text.get_rect(center=(screen_width // 2, screen_height * 2 // 3))
game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
back_to_menu_text = start_font.render('Back to Menu', True, custom_colour2)
back_to_menu_rect = back_to_menu_text.get_rect(center=(screen_width // 2, screen_height * 2 // 3))

# Clock setup
clock = pygame.time.Clock()
dt = 0

# Image setup
balao = pygame.image.load("obalaodojoao (1).png").convert_alpha()
balao = pygame.transform.scale(balao, (75, 187.5))
cloud_img = pygame.image.load("nuvem-removebg-preview.png").convert_alpha()
cloud_img = pygame.transform.scale(cloud_img, (230, 190))
badcloud_img = pygame.image.load("nuvem-removebg-preview (1) (2).png").convert_alpha()
badcloud_img = pygame.transform.scale(badcloud_img, (180, 110))
marvota_img = pygame.image.load("marvota.png").convert_alpha()
marvota_img = pygame.transform.scale(marvota_img, (160, 100))
fundo_start = pygame.image.load("fundo.png")

# Initial player position
player_pos = pygame.Vector2((screen_width - balao.get_width()) / 2, (1500 - balao.get_height()) / 2)

# Store cloud positions
clouds = []
bad_clouds = []
game_over_clouds = []

# Game over cloud setup
GRID_COLS = 3
GRID_ROWS = 4
NUM_GAME_OVER_CLOUDS = 10

# Marvota setup
marvota_pos = pygame.Vector2(random.randint(0, screen_width - marvota_img.get_width()), 0)
marvota_speed = 650  # Adjust this value to make it faster than clouds

# Score setup
score = 0
highest_score = 0
score_event = pygame.USEREVENT + 1
pygame.time.set_timer(score_event, 400)

# Generate random cloud positions
def create_cloud(y_range, is_bad=False):
    while True:
        x = random.randint(0, screen_width - (badcloud_img.get_width() if is_bad else cloud_img.get_width()))
        y = random.randint(y_range[0], y_range[1])
        
        # Check for overlap
        overlap = False
        for (existing_x, existing_y, _) in clouds + bad_clouds:
            distance = math.sqrt((x - existing_x) ** 2 + (y - existing_y) ** 2)
            if distance < 200:
                overlap = True
                break
        
        if not overlap:
            return x, y, is_bad

# Initial clouds
num_clouds = 10
num_bad_clouds = 2
cloud_height = cloud_img.get_height()
for i in range(num_clouds):
    y_range = (-cloud_height + (i * screen_height // num_clouds), -cloud_height + ((i + 1) * screen_height // num_clouds))
    if i < num_bad_clouds:
        bad_clouds.append(create_cloud(y_range, is_bad=True))
    else:
        clouds.append(create_cloud(y_range))

# Check for collisions
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Update game over clouds
def update_game_over_clouds():
    global game_over_clouds
    
    cell_width = screen_width // GRID_COLS
    cell_height = screen_height // GRID_ROWS

    # Create new clouds if needed
    while len(game_over_clouds) < NUM_GAME_OVER_CLOUDS:
        grid_x = random.randint(0, GRID_COLS - 1)
        grid_y = random.randint(0, GRID_ROWS - 1)
        
        x = random.randint(grid_x * cell_width, (grid_x + 1) * cell_width - cloud_img.get_width())
        y = random.randint(grid_y * cell_height, (grid_y + 1) * cell_height - cloud_img.get_height())
        
        # Check for minimum distance
        if all(math.hypot(x - cx, y - cy) > 200 for cx, cy in game_over_clouds):
            game_over_clouds.append([x, y])
    
    # Update cloud positions
    for i, (x, y) in enumerate(game_over_clouds):
        y -= 1  # Move upwards
        if y < -cloud_img.get_height():
            # Reset cloud to bottom if it goes off screen
            grid_x = random.randint(0, GRID_COLS - 1)
            x = random.randint(grid_x * cell_width, (grid_x + 1) * cell_width - cloud_img.get_width())
            y = screen_height
        game_over_clouds[i] = [x, y]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_state == START:
                    game_state = PLAYING
                    score = 0  # Reset score when game starts
            elif event.key == pygame.K_SPACE:
                if game_state == GAME_OVER:
                    game_state = START
                    # Update highest score
                    if score > highest_score:
                        highest_score = score
                    # Reset game state
                    player_pos = pygame.Vector2((screen_width - balao.get_width()) / 2, (1600 - balao.get_height()) / 2)
                    clouds = []
                    bad_clouds = []
                    game_over_clouds = []
                    for i in range(num_clouds):
                        y_range = (-cloud_height + (i * screen_height // num_clouds), -cloud_height + ((i + 1) * screen_height // num_clouds))
                        if i < num_bad_clouds:
                            bad_clouds.append(create_cloud(y_range, is_bad=True))
                        else:
                            clouds.append(create_cloud(y_range))
                    marvota_pos = pygame.Vector2(random.randint(0, screen_width - marvota_img.get_width()), 0)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if game_state == START and start_rect.collidepoint(event.pos):
                game_state = PLAYING
                score = 0  # Reset score when game starts
            elif game_state == GAME_OVER and back_to_menu_rect.collidepoint(event.pos):
                game_state = START
                # Update highest score
                if score > highest_score:
                    highest_score = score
                # Reset game state
                player_pos = pygame.Vector2((screen_width - balao.get_width()) / 2, (1600 - balao.get_height()) / 2)
                clouds = []
                bad_clouds = []
                game_over_clouds = []
                for i in range(num_clouds):
                    y_range = (-cloud_height + (i * screen_height // num_clouds), -cloud_height + ((i + 1) * screen_height // num_clouds))
                    if i < num_bad_clouds:
                        bad_clouds.append(create_cloud(y_range, is_bad=True))
                    else:
                        clouds.append(create_cloud(y_range))
                marvota_pos = pygame.Vector2(random.randint(0, screen_width - marvota_img.get_width()), 0)
        
        elif event.type == score_event and game_state == PLAYING:
            score += 1

    # Clear screen
    screen.fill(custom_colour)

    if game_state == START:
        # Start screen
        screen.blit(fundo_start, (0, 0))  # Draw start screen background
        screen.blit(title_text, title_rect)  # Draw game title
        screen.blit(start_text, start_rect)  # Draw 'START' text
        
        # Draw highest score
        highest_score_text = score_font.render(f'Highest Score: {highest_score}', True, custom_colour2)
        highest_score_rect = highest_score_text.get_rect(center=(screen_width // 2, 400))
        screen.blit(highest_score_text, highest_score_rect)

    elif game_state == PLAYING:
        # Draw clouds
        for i, (cloud_x, cloud_y, is_bad) in enumerate(clouds + bad_clouds):
            cloud_y += 1  

            # Reset clouds to the top
            if cloud_y > screen_height:
                new_y_range = (-cloud_height, 0)
                if is_bad:
                    bad_clouds[i - len(clouds)] = create_cloud(new_y_range, is_bad=True)
                else:
                    clouds[i] = create_cloud(new_y_range)
            else:
                if is_bad:
                    bad_clouds[i - len(clouds)] = (cloud_x, cloud_y, is_bad)
                else:
                    clouds[i] = (cloud_x, cloud_y, is_bad)

            # Draw cloud
            cloud_to_draw = badcloud_img if is_bad else cloud_img
            screen.blit(cloud_to_draw, (cloud_x, cloud_y))

        # Ensure there are always three bad clouds
        while len(bad_clouds) < num_bad_clouds:
            new_y_range = (-cloud_height, 0)
            bad_clouds.append(create_cloud(new_y_range, is_bad=True))

        # Update marvota position
        marvota_pos.y += marvota_speed * dt
        if marvota_pos.y > screen_height:
            marvota_pos.x = player_pos.x  # Set marvota's x position to the balloon's x position
            marvota_pos.y = 0

        # Draw marvota
        screen.blit(marvota_img, marvota_pos)

        # Draw balloon
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_pos.x -= 650 * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_pos.x += 650 * dt

        player_pos.x = max(0, min(player_pos.x, screen_width - balao.get_width()))
        screen.blit(balao, player_pos)

        # Check for collisions with bad clouds and marvota
        balloon_rect = pygame.Rect(player_pos.x, player_pos.y, balao.get_width(), balao.get_height() / 4)
        for cloud_x, cloud_y, is_bad in bad_clouds:
            if is_bad:
                bad_cloud_rect = pygame.Rect(cloud_x, cloud_y, badcloud_img.get_width(), badcloud_img.get_height())
                if check_collision(balloon_rect, bad_cloud_rect):
                    game_state = GAME_OVER
                    break

        marvota_rect = pygame.Rect(marvota_pos.x, marvota_pos.y, marvota_img.get_width(), marvota_img.get_height())
        if check_collision(balloon_rect, marvota_rect):
            game_state = GAME_OVER

        # Draw score
        score_text = score_font.render(f'{score}', True, custom_colour2)
        screen.blit(score_text, (602, 15))

    elif game_state == GAME_OVER:
        # Update and draw game over clouds
        update_game_over_clouds()
        for cloud_x, cloud_y in game_over_clouds:
            screen.blit(cloud_img, (cloud_x, cloud_y))
        
        # Game over screen
        screen.blit(game_over_text, game_over_rect)  # Draw 'GAME OVER' text
        screen.blit(back_to_menu_text, back_to_menu_rect)  # Draw 'Back to Menu' text
        
        # Draw final score
        final_score_text = score_font.render(f'Your Score: {score}', True, custom_colour2)
        final_score_rect = final_score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
        screen.blit(final_score_text, final_score_rect)

    # Update display
    pygame.display.flip()

    # Limits FPS to 120
    dt = clock.tick(120) / 1000

pygame.quit()
