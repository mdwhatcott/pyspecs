import os
from pyspecs._runner import _step_runner


def main():
    _step_runner.load_steps(os.getcwd())


if __name__ == '__main__':
    main()