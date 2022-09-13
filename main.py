import asyncio
from code.game import Game

if __name__ == "__main__":
    game = Game()
    # game.run()
    asyncio.run(game.run())
