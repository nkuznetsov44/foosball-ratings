import asyncio
from aiopg.sa import create_engine
from core.entities.player import Player
from core.entities.match import Match, Team, MatchSet


async def main():
    async with create_engine(user='ratings', database='ratings_core', host='localhost', password='ratings') as engine:
        async with engine.acquire() as conn:
            player = Player(
                first_name='Nikita',
                last_name='Kuznetsov'
            )
            session.add(player)
            session.commit()
            print(player)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
