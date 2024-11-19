from pygame import Surface
from pygame.event import Event, post as post_event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.sprite import Group

from asteroids.asteroid import Asteroid
from asteroids.asteroidfield import AsteroidField
from asteroids.circle import Circle
from asteroids.events import CustomEvent
from asteroids.explosion import Particle
from asteroids.itemmanager import ItemManager
from asteroids.items import Item
from asteroids.player import Player
from asteroids.interfaces import IDrawable, IUpdatable
from asteroids.shot import Shot
from asteroids.entityfactory import EntityFactory
from asteroids.stars import Star


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


MIN_LIFETIME = 5


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
        self.__particles = Group()
        self.__despawnable = Group()
        self.__stars = Group()
        self.__items = Group()
        self.__item_manager = Group()

        self.__entity_factory = entity_factory
        self.__screen_size = screen_size

        self.__entity_group_map = {
            Player: [self.__updatable, self.__drawable, self.__player],
            Asteroid: [
                self.__updatable,
                self.__drawable,
                self.__asteroids,
                self.__despawnable,
            ],
            AsteroidField: [self.__updatable],
            Shot: [self.__updatable, self.__drawable, self.__shots, self.__despawnable],
            Particle: [
                self.__updatable,
                self.__drawable,
                self.__particles,
                self.__despawnable,
            ],
            Star: [self.__drawable, self.__stars],
            Item: [self.__drawable, self.__items],
            ItemManager: [self.__updatable, self.__item_manager],
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

        if len(self.__items) == 0:
            for item_manager in self.__item_manager:
                item_manager: ItemManager
                item_manager.update(dt)

        # check for off screen entities
        for entity in self.__despawnable:
            entity: Shot
            if all(
                [
                    out_of_bounds(entity, self.__screen_size),
                    entity.age > MIN_LIFETIME,
                ]
            ):
                entity.kill()

        # check for player collisions
        for player in self.__player:
            for asteroid in self.__asteroids:
                if collided(player, asteroid):
                    event = Event(CustomEvent.PLAYER_KILLED)
                    post_event(event)

        # check for bullet collisions
        for asteroid in self.__asteroids:
            asteroid: Asteroid

            for entity in self.__shots:
                entity: Shot

                if collided(entity, asteroid):
                    entity.kill()
                    asteroid.split()

        for player in self.__player:
            player: Player
            for item in self.__items:
                item: Item
                if collided(player, item):
                    item.kill()
                    item.equip(player)

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
        for sprite in self.__items:
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
                print("registered", event.entity)
