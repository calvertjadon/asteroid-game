from typing import Sequence, TypeAlias
from pygame import Vector2


Coordinate: TypeAlias = tuple[float, float] | Sequence[float] | Vector2
Triangle: TypeAlias = tuple[Coordinate, Coordinate, Coordinate]
