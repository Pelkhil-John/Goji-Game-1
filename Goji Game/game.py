import pygame
import random
import math
pygame.init()
import music_reader as m
import constants as c



m.BG_music.play  (-1)
projectiles = []
hitbox = pygame.rect.Rect
player = pygame.Rect(c.WIDTH/2 - c.PLAYER_WIDTH/2, c.HEIGHT/2 - c.PLAYER_HEIGHT/2, c.PLAYER_WIDTH, c.PLAYER_HEIGHT)


class Entity:

    x, y = 0, 0
    on_screen = True
    rect = pygame.Rect(x,y,x,y)
    color = ((211,211,211))

    def __init__(self, x=random.random()*c.WIDTH, y=random.random()*c.HEIGHT, width=c.PLAYER_WIDTH, height=c.PLAYER_HEIGHT):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class Projectile:

    P_WIDTH, P_HEIGHT = 10,10

    rect: pygame.rect.Rect
    vel: tuple

    def __init__(self, vel:tuple):
        self.rect = pygame.rect.Rect(c.WIDTH/2,c.HEIGHT/2, self.P_WIDTH, self.P_HEIGHT)
        self.vel = vel

    def move(self, vel_x, vel_y):
        self.rect.x += (self.vel[0] * math.cos(self.vel[1])) - vel_x
        self.rect.y += (self.vel[0] * math.sin(self.vel[1])) - vel_y

def fire(dir):
    global projectiles
    projectiles.append(Projectile((c.PROJECTILE_VEL,-math.radians(dir))))

def find_collisions_p():
    for ent in c.entities:
        if player.colliderect(ent):
            c.entities.remove(ent)


def draw(player):
    # WIN.blit()
    c.WIN.fill((0, 0, 0))
    pygame.draw.rect(c.WIN, (90,90,90), player)
    for ent in c.entities:
        pygame.draw.rect(c.WIN, ent.color, ent.rect)
    for proj in projectiles:
        pygame.draw.rect(c.WIN, 'blue', proj.rect)
    c.WIN.blit(c.FONT.render(str(c.score), False, ((255, 255, 255))), (0,0))
    pygame.display.update()
    if c.score > 30:
        for proj in projectiles:
            pygame.draw.rect(c.WIN, 'red', proj.rect)


def is_on_screen(ent):
    if ent.rect.right < 0 or ent.rect.left > c.WIDTH or ent.rect.bottom < 0 or ent.rect.top > c.HEIGHT:
        ent.on_screen = False
    return ent.on_screen


def rolling_add(ent):
    if not is_on_screen(ent):
        if ent.rect.right < 0:
            c.entities.append(Entity(c.WIDTH, random.random()*c.HEIGHT))
        elif ent.rect.left > c.WIDTH:
            c.entities.append(Entity(0-c.PLAYER_WIDTH, random.random()*c.HEIGHT))
        elif ent.rect.bottom < 0:
            c.entities.append(Entity(random.random()*c.WIDTH, c.HEIGHT))
        elif ent.rect.top > c.HEIGHT:
            c.entities.append(Entity(random.random()*c.WIDTH, 0-c.PLAYER_HEIGHT))


def update_position(vel_x, vel_y):
    for ent in c.entities:
        ent.x -= vel_x
        ent.y -= vel_y
        ent.update()
        if ent.on_screen:
            rolling_add(ent)
    for proj in projectiles:
        proj.move(vel_x, vel_y)


def dropkick(direction):
    player.h = c.PLAYER_WIDTH
    player.w = c.PLAYER_HEIGHT
    player.x += 5


def main():
    for _ in range(100):
        c.entities.append(Entity(random.random()*c.WIDTH, random.random()*c.HEIGHT))
    clock = pygame.time.Clock()
    firing = False
    kicking = False
    kick_count = 0
    fire_count = 0
    while True:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit(0)
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_3:
                    if not firing :
                        firing = True
                        m.Atomic_Heat_Ray.play(0)
                if event.key == pygame.K_2:
                    if not kicking:
                        kicking = True
            #         fire(get_direction(player.center, mouse_pos))
            #         m.Atomic_Heat_Ray.play(0)
            #         firing = True
            # if event.type == pygame.KEYUP and event.key == pygame.K_4:
            #     if firing:
            #         fire(get_direction(player.center,mouse_pos))
            #         firing = False

 
        keys = pygame.key.get_pressed()
        vel_x, vel_y = 0, 0
        if keys[pygame.K_a]:
            vel_x -= c.MAX_VEL
        if keys[pygame.K_d]:
            vel_x += c.MAX_VEL
        if keys[pygame.K_s]:
            vel_y += c.MAX_VEL
        if keys[pygame.K_w]:
            vel_y -= c.MAX_VEL
        if keys[pygame.K_r]:
            m.Heisei.play(0)
        # if keys[pygame.K_SPACE]:
        #     fire(get_direction(player.center, mouse_pos))
        if math.sqrt(math.pow(vel_x, 2) + math.pow(vel_y, 2)) > c.MAX_VEL:
            vel_x, vel_y = vel_x/math.sqrt(2), vel_y/math.sqrt(2)
        update_position(vel_x, vel_y)
        for proj in projectiles:
            find_collisions_b(proj)
        if firing:
            fire(get_direction(player.center, mouse_pos))
            fire_count += 1
            if fire_count > 310:
                firing = False
                fire_count = 0
        if kicking:
            find_collisions_p()
            for ent in c.entities:
                if player.colliderect(ent):
                    c.score += 1
            dropkick(get_direction(player.center, mouse_pos))
            kick_count += 1
            if kick_count > 50:
                kicking = False
                kick_count = 0
                player.h = c.PLAYER_HEIGHT
                player.w = c.PLAYER_WIDTH
                update_position(player.centerx - c.WIDTH/2, player.centery -c.HEIGHT )
                player.center = (c.WIDTH/2,c.HEIGHT/2)
        draw(player)

def get_direction(center:tuple, target:tuple) -> int:
    if target[0] - center[0] == 0:
        target = (target[0] + 1, target[1])
    if target[0] - center[0] > 0:
        angle = math.degrees(math.atan((center[1]-target[1])/(target[0]-center[0])))
    else:
        angle = 180 + math.degrees(math.atan((target[1]-center[1])/(center[0]-target[0])))
    return angle % 360

def find_collisions_b(projectile):
    global projectiles
    c.PROJECTILE_VEL
    for ent in c.entities:
        if projectile.rect.colliderect(ent):
            c.score += 1
            c.entities.remove(ent)
            projectiles.remove(projectile)
            return True


if __name__ == "__main__":
    main()