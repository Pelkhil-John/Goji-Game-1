import pygame
import math
import random

WIDTH, HEIGHT = 1360,700
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 40
MAX_VEL = 10
PROJECTILE_VEL = 40

FONT = pygame.font.SysFont("calibri", 100)
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("pew pew")
entities = []
projectiles = []
score = 0