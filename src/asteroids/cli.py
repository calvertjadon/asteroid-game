import sys

from typing import Sequence

from asteroids.config import Config
from asteroids.game import run


def main(argv: Sequence[str] = sys.argv[1:]):
    config = Config()
    run(config)


if __name__ == "__main__":
    main()
