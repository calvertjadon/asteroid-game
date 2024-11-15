from pygame import Surface
from pygame.event import Event, post as post_event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group

from asteroids.asteroid import Asteroid
from asteroids.asteroidfield import AsteroidField
from asteroids.circle import Circle
from asteroids.events import CustomEvent
from asteroids.player import Player
from asteroids.interfaces import IDrawable, IUpdatable
from asteroids.shot import Shot
from asteroids.entityfactory import EntityFactory


def collided(e1: Circle, e2: Circle) -> bool:
    return e1.center.distance_to(e2.center) < e1.radius + e2.radius


def out_of_bounds(circle: Circle, bounds: Rect) -> bool:
    return any(
        [
            circle.center.x + circle.radius < bounds.left,
            circle.center.x - circle.radius > bounds.right,
            circle.center.y + circle.radius < bounds.top,
            circle.center.y - circle.radius > bounds.bottom,
        ]
    )


class EntityManager:
    __updatable: Group
    __drawable: Group
    __entity_factory: EntityFactory
    __entity_group_map: dict[type, list[Group]]
    __screen_size: Rect

    def __init__(self, screen_size: Rect, entity_factory: EntityFactory) -> None:
        self.__updatable = Group()
        self.__drawable = Group()
        self.__player = Group()
        self.__asteroids = Group()
        self.__shots = Group()

        self.__entity_factory = entity_factory
        self.__screen_size = screen_size

        self.__entity_group_map = {
            Player: [self.__updatable, self.__drawable, self.__player],
            Asteroid: [self.__updatable, self.__drawable, self.__asteroids],
            AsteroidField: [self.__updatable],
            Shot: [self.__updatable, self.__drawable, self.__shots],
        }

    def register(self, entity: IUpdatable | IDrawable) -> None:
        for type_, groups in self.__entity_group_map.items():
            if isinstance(entity, type_):
                for group in groups:
                    group.add(entity)

    def update(self, dt: float) -> None:
        for sprite in self.__updatable:
            sprite: IUpdatable
            sprite.update(dt)

        # check for off screen entities
        for shot in self.__shots:
            shot: Shot
            if out_of_bounds(shot, self.__screen_size):
                shot.kill()

        # check for player collisions
        for player in self.__player:
            for asteroid in self.__asteroids:
                if collided(player, asteroid):
                    event = Event(CustomEvent.GAME_OVER)
                    post_event(event)

        # check for bullet collisions
        for asteroid in self.__asteroids:
            asteroid: Asteroid

            for shot in self.__shots:
                shot: Shot

                if collided(shot, asteroid):
                    shot.kill()
                    asteroid.split()

    def reset(self) -> None:
        # for sprite in self.__updatable:
        #     sprite.kill()
        # for sprite in self.__drawable:
        #     sprite.kill()
        for sprite in self.__player:
            sprite.kill()
        for sprite in self.__asteroids:
            sprite.kill()
        for sprite in self.__shots:
            sprite.kill()

        center = Vector2(self.__screen_size.center)
        self.__entity_factory.create_player(center)

    def draw(self, surface: Surface) -> None:
        for sprite in self.__drawable:
            sprite: IDrawable
            sprite.draw(surface)

    def handle(self, event: Event) -> None:
        match event.type:
            case CustomEvent.ENTITY_CREATED:
                self.register(event.entity)
