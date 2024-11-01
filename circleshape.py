import pygame
from abc import ABC, abstractmethod


# Base class for game objects
class CircleShape(pygame.sprite.Sprite, ABC):
    def __init__(self, x: float, y: float, radius: float):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)  # type: ignore
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...

    def is_colliding(self, other: "CircleShape") -> bool:
        distance = self.position.distance_to(other.position)
        return distance <= self.radius + other.radius
