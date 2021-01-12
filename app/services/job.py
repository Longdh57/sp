import asyncio

from app.main import app

loop = asyncio.get_event_loop()


@app.on_event("startup")
async def startup_event():
    print('Hello Long...')
