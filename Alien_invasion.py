import sys
import os
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import pygame.font
from time import sleep


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load('assets\ship.bmp')
       # self.image = pygame.image.load(os.path.join('Users', 'david', 'desktop','python','game', 'ship.bmp'))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        # movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        pygame.display.flip()

    def center_ship(self):
        self.center = self.screen_rect.centerx

class Bullet(Sprite):
    def __init__(self, ai_setting, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,ai_setting.bullet_width, ai_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor
    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('assets/F_Alien.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
            
class Button:
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width, self.height = 200, 50
        self.button_color = (0, 250, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 28)
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (230,230,230)
        '''Ship settings'''
        self.ship_speed_factor = 1.5 
        self.ship_limit = 3
        '''Bullet setting'''
        self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_allowed = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        '''Alien setting'''
        self.fleet_drop_speed = 10
        
        self.speedup_scale = 1.1
        self.pause_game = False
        #self.high_score = highscore()
        #how quickly the alien killed point increase
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        '''speed increase for asset'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        #score_database(self.alien_points, self.high_score)
        
#def score_database(alien_score, high_score):
#    with open('highest_score.txt', 'w') as score:
#        if alien_score > high_score:
#            score.write(str(alien_score))
#            print(alien_score)

#def highscore():
#    high_score = 0
#    return high_score


class Gamestats:
    '''Track statistics for Alien Invasion'''
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_ships()
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
    def prep_score(self):
        rounded_score = int(round(self.stats.score, -1))
        self.score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render('Score: '+ self.score_str,True, self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    def prep_high_score(self):
        #high_score = 0
       # try:    
    
       #     with open('high_score.txt', 'r') as high_score:
       #         high_score = int(high_score.read())
                #print(high_score)
                
      #  except FileNotFoundError:
       #     with open('high_score.txt', 'w') as high_score:
        #        high_score.write(str(check_high_score(self.stats, self)))

        self.high_score_image = self.font.render('{:,}'.format(self.stats.high_score), True, self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        

    def prep_level(self):
        '''Turn the level into a rendered image'''
        self.level_image = self.font.render(str('Level: '+str(self.stats.level)), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10+ship_number*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

def check_high_score(stats, sb):
    '''checks for the highest score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
    return stats.high_score

def check_keydown_events(event, ai_setting, screen, stats, play_button, ship, bullets):
    '''Return key is pressed'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_setting.bullet_allowed:
            new_bullet = Bullet(ai_setting, screen, ship)
            bullets.add(new_bullet)
    elif event.key == pygame.K_p:
        stats.game_active = True
        pygame.mouse.set_visible(False)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    '''Return False if key is not pressed'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
        
def check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets):
    '''keyboard and mouse events'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_setting, screen,  stats, play_button, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_setting.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
    elif button_clicked and stats.game_active:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, game_over):
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def get_number_aliens_x(ai_settings, alien_width):
    '''returns the number of alien created on a line'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''return the number of row occupied by the aliens'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''create an alien'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien.rect.height + alien.rect.height * row_number
    alien.rect.y = alien.y
    alien.add(aliens)

def create_fleet(ai_settings, screen, ship, aliens):
    '''create a fleet of an alien that appears on the screen at a time'''
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    '''checks if the an alien as touched any side of of the screen'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''alien hitting the ship directly'''
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)

def run_game():
    pygame.init()
    clock = pygame.time.Clock()
    ai_setting = Settings()
    screen = pygame.display.set_mode(
        (ai_setting.screen_width, ai_setting.screen_height))
    ship = Ship(ai_setting, screen)
    stats = Gamestats(ai_setting)
    sb = Scoreboard(ai_setting, screen, stats)
    play_button = Button(ai_setting, screen, 'P - Play')
    game_over = Button(ai_setting, screen, 'Game Over!')
    bullets = Group()
    aliens = Group()
    pygame.display.set_caption('Alien Invasion')
    #alien = Alien(ai_setting, screen)
    create_fleet(ai_setting, screen, ship, aliens)
  
    while True:
        screen.fill(ai_setting.bg_color)
        clock.tick(90)
        check_events(ai_setting, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            update_bullets(ai_setting, screen, stats, sb, ship, aliens, bullets)
            bullets.update()
            update_aliens(ai_setting, stats, sb, screen, ship, aliens, bullets)
        update_screen(ai_setting, screen, stats, sb, ship, aliens, bullets, play_button, game_over)

        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        #print(len(bullets))
        if stats.ships_left == 0:
            game_over.draw_button()
            pygame.time.delay(5000)
            break
        #print(stats.score)
    run_game()

run_game()

