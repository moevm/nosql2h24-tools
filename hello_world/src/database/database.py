from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


async def connect_to_database(uri: str) -> tuple[AsyncIOMotorClient, AsyncIOMotorDatabase]:
    client = AsyncIOMotorClient(uri)
    db = client.get_default_database()
    pong = await db.command("ping")

    if pong.get("ok") != 1:
        raise Exception("Could not connect to database")

    return client, db