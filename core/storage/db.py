import aiopg.sa


async def pg_context(app):
    conf = app["config"]["postgres"]
    engine = await aiopg.sa.create_engine(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        minsize=conf["minsize"],
        maxsize=conf["maxsize"],
    )
    app["db"] = engine

    yield

    app["db"].close()
    await app["db"].wait_closed()
