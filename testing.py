import asyncio
import websockets

async def test_connection():
    async with websockets.connect('ws://localhost:8000/ws/chat/room1/') as websocket:
        await websocket.send("Hello World!")
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(test_connection())
