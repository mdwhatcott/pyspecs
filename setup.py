from distutils.core import setup
from pyspecs import __version__

setup(
    name='pyspecs',
    version=__version__,
    packages=['pyspecs'],
    scripts=[
        'bin/pyspecs_.py',
        'bin/pyspecs_idle.py'],
    entry_points={
        'console_scripts': [
            'pyspecs = pyspecs._program:main',
            'pyspecs_idle = pyspecs._idle:main',
        ]
    },
    url='http://github.com/mdwhatcott/pyspecs',
    license='GPL',
    author='Michael Whatcott',
    author_email='mdwhatcott+pyspecs@gmail.com',
    description='Minimalistic BDD in Python',
    long_description='pyspecs is a testing framework that strives to achieve '
                     'more readable specifications (tests) by leveraging '
                     'some fancy syntactic sugar and auto-discovery of ' \
                     'tests/specs.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Programming Language :: Python',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ]
)
