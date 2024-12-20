from enum import Enum
import pygame

from asteroids.types import EventType


class CustomEvent(EventType, Enum):
    ENTITY_CREATED = pygame.event.custom_type()
    GAME_OVER = pygame.event.custom_type()
    ASTEROID_KILLED = pygame.event.custom_type()
    PLAYER_KILLED = pygame.event.custom_type()
