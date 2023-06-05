import random
import pygame
import sys
import buttons


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= (len(self.player_walk)):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.animation_state()
        self.apply_gravity()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly1, fly2]
            y_pos = 210
        else:
            snail1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail1, snail2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= (len(self.frames)):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


# Setup
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runnin')
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.2)
bg_music.play(loops=-1)
menu_active = True
game_over_active = False
scroll = 0
tiles = 3

# Text font
pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Clock instance
clock = pygame.time.Clock()

# Environment surfaces
sky_surf = pygame.image.load('graphics/Environment/Sky.png').convert()
sky_width = sky_surf.get_width()
ground_surf = pygame.image.load('graphics/Environment/ground.png').convert()

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# Menu/Game over
player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(400, 200))

game_title_surf = pixel_font.render('Runnin', False, (111, 196, 169))
game_title_surf = pygame.transform.rotozoom(game_title_surf, 0, 1.2)
game_title_rect = game_title_surf.get_rect(center=(400, 80))

start_inst_surf = pixel_font.render('Space: jump', False, (111, 196, 169))
start_inst_surf = pygame.transform.rotozoom(start_inst_surf, 0, 1.2)
start_inst_rect = start_inst_surf.get_rect(midleft=(300, 320))

# Button instances
start_button = buttons.Button(pygame.image.load('graphics/Buttons/start_btn.png').convert_alpha(), 150, 300, 0.5)
exit_button = buttons.Button(pygame.image.load('graphics/Buttons/exit_btn.png').convert_alpha(), 520, 300, 0.5)


# Score function
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = pixel_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


# Check collision function
def collisions_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        player.sprite.kill()
        player.add(Player())
        return False
    else:
        return True


# Game loop
while True:
    # Event handler
    for event in pygame.event.get():
        # Quit by clicking X
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_active:
            # Adds new enemy to obstacle group after a 1.5 secs
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacles(random.choice(['fly', 'snail', 'snail', 'snail'])))
        if game_over_active:
            if event.type == pygame.KEYDOWN:
                # Returns to menu by pressing escape
                if event.key == pygame.K_ESCAPE:
                    game_over_active = False
                    menu_active = True
    if game_active:
        # Scrolling sky
        for i in range(0, tiles):
            screen.blit(sky_surf, (i * sky_width + scroll, 0))

        # variable that causes the scrolling effect
        scroll -= 5

        # Resets the sky after scroll reaches the sky width
        if abs(scroll) > sky_width:
            scroll = 0

        # Ground
        screen.blit(ground_surf, (0, 300))
        # Player
        player.draw(screen)
        player.update()
        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()
        # Collisions
        game_active = collisions_sprite()
        # Score
        score = display_score()
        # Changing game state to game over
        if not game_active and not menu_active:
            game_over_active = True
    if menu_active:
        # Menu
        screen.fill((94, 129, 162))

        # Starts game by clicking start
        if start_button.draw(screen):
            game_active = True
            start_time = int(pygame.time.get_ticks() / 1000)

        # Exits game by clicking exit
        if exit_button.draw(screen):
            pygame.quit()
            sys.exit()

        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(game_title_surf, game_title_rect)
        screen.blit(start_inst_surf, start_inst_rect)
        if game_active:
            menu_active = False

    elif game_over_active:
        # Game over
        screen.fill((94, 129, 162))

        # 'Score message' sprite
        score_message_surf = pixel_font.render(f'Your score is: {score}', False, (111, 196, 169))
        score_message_surf = pygame.transform.rotozoom(score_message_surf, 0, 1.2)
        score_message_rect = score_message_surf.get_rect(midleft=(230, 320))

        # 'Return to menu instructions' sprite
        return_menu_surf = pixel_font.render('Escape: Main Menu', False, (111, 196, 169))
        return_menu_surf = pygame.transform.rotozoom(return_menu_surf, 0, 0.5)
        return_menu_rect = return_menu_surf.get_rect(topleft=(20, 30))

        screen.blit(score_message_surf, score_message_rect)
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(game_title_surf, game_title_rect)
        screen.blit(return_menu_surf, return_menu_rect)
        if game_active:
            game_over_active = False

    pygame.display.update()
    clock.tick(60)
