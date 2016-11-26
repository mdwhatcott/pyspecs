"""
Because I always forget, here's how to submit to PyPI:

# python setup.py register sdist upload

"""

from distutils.core import setup
import pyspecs


setup(
    name='pyspecs',
    version=pyspecs.__version__,
    packages=['pyspecs'],
    scripts=['scripts/run_pyspecs.py'],
    url='https://github.com/mdwhatcott/pyspecs',
    license='MIT',
    author='Michael Whatcott',
    author_email='mdwhatcott+pyspecs@gmail.com',
    description='Concise BDD in python',
    long_description='pyspecs is a testing framework that strives to achieve '
                     'more readable specifications (tests) by leveraging '
                     'some fancy syntactic sugar and auto-discovery of '
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
