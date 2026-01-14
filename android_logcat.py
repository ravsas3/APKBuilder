import subprocess
import asyncio
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    process = subprocess.Popen(["adb", "logcat"], stdout=subprocess.PIPE, text=True)
    for line in iter(process.stdout.readline, ''):
        await ws.send_text(line)
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)