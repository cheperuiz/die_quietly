import os
import signal

from fastapi import FastAPI
from shared_memory_dict import SharedMemoryDict

app = FastAPI()
smd = SharedMemoryDict(name='broker', size=1000)
if 'ids' not in smd:
    smd['ids'] = {}
smd['ids'] += f"api-{os.getpid()};"


def sigterm_handler(_signo, _stack_frame):
    smd.cleanup()
    exit(0)


signal.signal(signal.SIGTERM, sigterm_handler)

def pids_by_task(ids):
    pids = {}
    for record in ids.split(";"):
        if record:
            parts = record.split("-")
            _id = '-'.join(parts[:-1])
            pid = parts[-1]
            pids[_id] = pid
    return pids

@app.get("/tasks")
async def get_tasks():
    smd = SharedMemoryDict(name='broker', size=1000)
    return pids_by_task(smd['ids'])

@app.post("/kill")
async def kill(task_id: str):
    smd = SharedMemoryDict(name='broker', size=1000)
    if task_id not in smd:
        return {'status': 'error', 'message': 'task not found'}
    smd[task_id] = 'die'
    return {'status': 'ok'}

@app.post("/bomb")
async def bomb(task_id: str):
    smd = SharedMemoryDict(name='broker', size=1000)
    if task_id not in smd:
        return {'status': 'error', 'message': 'task not found'}
    smd[task_id] = 'bomb'
    return {'status': 'ok'}

@app.post("/greet")
async def greet(task_id: str):
    smd = SharedMemoryDict(name='broker', size=1000)
    if task_id not in smd:
        return {'status': 'error', 'message': 'task not found'}
    smd[task_id] = 'greet'
    print(smd[task_id])
    return {'status': 'ok'}

