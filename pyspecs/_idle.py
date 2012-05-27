import os
import sys
import time


def main():
    working_dir = os.getcwd()
    idle(run_specs, working_dir)


def idle(action, working):
    spec_runs = 0
    state = 0
    while True:
        new_state = sum(checksums(working))
        if state != new_state:
            spec_runs += 1
            action(spec_runs)
            state = new_state
        time.sleep(.75)


def run_specs(runs):
    number = ' {} '.format(runs)
    half_delimiter = '=' * ((80 - len(number)) / 2)
    print '\n{0}{1}{0}\n'.format(half_delimiter, number)
    os.system('pyspecs ' + ' '.join(sys.argv[1:]))


def checksums(working):
    for root, dirs, files in os.walk(working):
        for f in files:
            if f.endswith('.py'):
                stats = os.stat(os.path.join(root, f))
                yield stats.st_mtime + stats.st_size


if __name__ == '__main__':
    main()