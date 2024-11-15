from typing import Annotated, Any
from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
    GetJsonSchemaHandler,
)
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, core_schema
import pygame


class __ColorPydanticAnnotation(pygame.Color):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        def validate_from_string(value: str) -> pygame.Color:
            try:
                return pygame.Color(value)
            except ValueError:
                raise ValueError(f"Invalid color string: {value}")

        def validate_from_tuple(value: tuple) -> pygame.Color:
            try:
                return pygame.Color(*value)
            except ValueError:
                raise ValueError(f"Invalid color format: {value}")

        from_string_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_string),
            ]
        )

        from_tuple_schema = core_schema.chain_schema(
            [
                core_schema.tuple_schema(
                    [
                        core_schema.int_schema(),
                        core_schema.int_schema(),
                        core_schema.int_schema(),
                        core_schema.int_schema(),
                    ]
                ),
                core_schema.no_info_plain_validator_function(validate_from_tuple),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=from_string_schema,
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(pygame.Color),
                    from_string_schema,
                    from_tuple_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda c: (c.r, c.g, c.b, c.a)
            ),
        )

    @classmethod
    def __get_pydantic_json_schema__(
        cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        # Use the same schema that would be used for `int`
        return handler(core_schema.str_schema())


Color = Annotated[pygame.Color, __ColorPydanticAnnotation]


class GameConfig(BaseModel):
    fps: int = Field(default=60)


class WindowConfig(BaseModel):
    width: int = Field(default=1280)
    height: int = Field(default=720)
    background_color: Color = Field(default="#000000")
    foreground_color: Color = Field(default="#ffffff")

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(x=self.width / 2, y=self.height / 2)

    @property
    def size(self) -> tuple[int, int]:
        return (self.width, self.height)


class AsteroidConfig(BaseModel):
    min_radius: int = Field(default=20)
    kinds: int = Field(default=3)
    spawn_rate: float = Field(default=0.8)
    color: Color = Field(default="#ffffff")

    @property
    def max_radius(self) -> int:
        return self.min_radius * self.kinds


class ShotConfig(BaseModel):
    radius: float = Field(default=5)
    speed: int = Field(default=500)
    color: Color = Field(default="#ffffff")
    cooldown: float = Field(default=0.3)


class PlayerConfig(BaseModel):
    move_speed: int = Field(default=200)
    radius: float = Field(default=20)
    color: Color = Field(default="#ffffff")
    turn_speed: int = Field(default=300)
    shot: ShotConfig = Field(default_factory=lambda: ShotConfig())


class Config(BaseModel):
    game: GameConfig = Field(default_factory=lambda: GameConfig())
    window: WindowConfig = Field(default_factory=lambda: WindowConfig())
    asteroid: AsteroidConfig = Field(default_factory=lambda: AsteroidConfig())
    player: PlayerConfig = Field(default_factory=lambda: PlayerConfig())
