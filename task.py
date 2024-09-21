import os
import signal
from uuid import uuid4
from time import sleep

from shared_memory_dict import SharedMemoryDict


def sigterm_handler(_signo, _stack_frame):
    print("SIGTERM received, exiting")
    smd[my_task_id] = 'die'


signal.signal(signal.SIGTERM, sigterm_handler)
smd = SharedMemoryDict(name='broker', size=1000)

my_task_id = str(uuid4())
print(f"starting task {my_task_id}",flush=True)

if 'ids' not in smd:
    smd['ids'] = ""
smd['ids'] += my_task_id+f"-{os.getpid()};"

while True:
    if my_task_id not in smd:
        smd[my_task_id] = ''
    if smd[my_task_id] == 'die':
        print(f"task {my_task_id} is dying",flush=True)
        smd.pop(my_task_id)
        smd.cleanup()
        break
    if smd[my_task_id] == 'greet':
        print(f"task {my_task_id} is greeting",flush=True)
        smd[my_task_id] = ''
    if smd[my_task_id] == 'bomb':
        smd[my_task_id] = ''
        raise Exception("bomb")
    sleep(0.1)

