import os
import time


def idle(action, working):
    state = 0
    while True:
        new_state = sum(_checksums(working))
        if state != new_state:
            action()
            state = new_state
        time.sleep(.75)


def _checksums(working):
    for root, dirs, files in os.walk(working):
        for f in files:
            if f.endswith('.py'):
                stats = os.stat(os.path.join(root, f))
                yield stats.st_mtime + stats.st_size