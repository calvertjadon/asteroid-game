import random
from typing import Callable
from pygame import Vector2
from pygame.event import Event

from asteroids.asteroid import Asteroid
from asteroids.config import AsteroidConfig
from asteroids.entity import Entity
from asteroids.events import CustomEvent


class AsteroidField(Entity):
    __config: AsteroidConfig
    __spawn_timer: float
    __max: Vector2
    __edges: list[tuple[Vector2, Callable[[float], Vector2]]]

    def __init__(self, max_: Vector2, config: AsteroidConfig) -> None:
        super().__init__()

        self.__max = max_
        self.__spawn_timer = 0.0
        self.__config = config
        self.__edges = [
            (
                Vector2(1, 0),
                lambda y: Vector2(-self.__config.max_radius, y * self.__max.y),
            ),
            (
                Vector2(-1, 0),
                lambda y: Vector2(
                    self.__max.x + self.__config.max_radius, y * self.__max.y
                ),
            ),
            (
                Vector2(0, 1),
                lambda x: Vector2(x * self.__max.x, -self.__config.max_radius),
            ),
            (
                Vector2(0, -1),
                lambda x: Vector2(
                    x * self.__max.x, self.__max.y + self.__config.max_radius
                ),
            ),
        ]

    def spawn(self, radius: float, center: Vector2, velocity: Vector2) -> None:
        asteroid = Asteroid(center, radius, self.__config.color)
        asteroid._velocity = velocity

    def handle(self, event: Event) -> None:
        assert event.type == CustomEvent.ASTEROID_KILLED

        old: Asteroid = event.asteroid
        if old.radius <= self.__config.min_radius:
            return

        angle = random.uniform(20, 50)
        v1 = Vector2(old.velocity).rotate(angle) * 1.2
        v2 = Vector2(old.velocity).rotate(-angle)

        self.spawn(
            radius=old.radius - self.__config.min_radius,
            center=Vector2(old.center),
            velocity=v1,
        )

        self.spawn(
            radius=old.radius - self.__config.min_radius,
            center=Vector2(old.center),
            velocity=v2,
        )

    def update(self, dt: float) -> None:
        self.__spawn_timer += dt
        if self.__spawn_timer > self.__config.spawn_rate:
            self.__spawn_timer = 0.0

            edge = random.choice(self.__edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            center = edge[1](random.uniform(0, 1))
            kind = random.randint(1, self.__config.kinds)

            self.spawn(self.__config.min_radius * kind, center, velocity)
