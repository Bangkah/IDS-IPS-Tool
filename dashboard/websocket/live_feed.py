import os
import asyncio
from fastapi import WebSocket

async def live_feed(websocket: WebSocket):
    await websocket.accept()
    log_path = os.path.abspath("ids_ips.log")
    if not os.path.exists(log_path):
        open(log_path, "a").close()
    with open(log_path, "r") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                await websocket.send_text(line.strip())
            else:
                await asyncio.sleep(1)
