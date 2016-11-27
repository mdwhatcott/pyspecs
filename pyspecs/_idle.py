import os
import sys
import time
from ._runner import _StepRunner
from ._reporting import ConsoleReporter
from ._registry import Registry
from ._decorators import wait_keyboard_interrupt


@wait_keyboard_interrupt
def watch(path):
    working = os.path.abspath(path)
    os.chdir(working)
    sys.path.append(working)
    repetitions = 0
    state = 0
    while True:
        new_state = sum(_checksums(working))
        if state != new_state:
            repetitions += 1
            _display_repetitions_banner(repetitions)
            print('Running tests...')
            run(working)
            state = new_state
        time.sleep(.75)

def run(path):
    sys.path.append(path)

    print('running', path)

    registry = Registry()

    step_runner = _StepRunner()
    step_runner.load_steps(path, registry)

    reporter = ConsoleReporter(registry)
    reporter.render(step_runner)

def _checksums(working):
    for root, dirs, files in os.walk(working):
        if dirs.startswith('.'):
            continue
        for f in files:
            if f.endswith('.py'):
                stats = os.stat(os.path.join(root, f))
                yield stats.st_mtime + stats.st_size


def _display_repetitions_banner(repetitions):
    number = ' {} '.format(repetitions)
    half_delimiter = (EVEN if not repetitions % 2 else ODD) * \
                     ((80 - len(number)) / 2)
    print('\n{0}{1}{0}\n'.format(half_delimiter, number))


EVEN = '='
ODD = '-'
