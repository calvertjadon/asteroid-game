import sys

from typing import Sequence

from asteroids.config import Config
from asteroids.game import Game


def main(argv: Sequence[str] = sys.argv[1:]):
    config = Config()
    game = Game(config)
    game.run()


if __name__ == "__main__":
    main()
