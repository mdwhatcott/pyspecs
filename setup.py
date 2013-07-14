from distutils.core import setup
from os.path import join, basename, splitext
import os
import pyspecs


project = pyspecs.__name__
root = os.getcwd()
modules = [splitext(basename(f))[0] for f in os.listdir(root)
           if f.endswith('.py') and f != 'setup.py']
scripts = [join('bin', f)
           for f in os.listdir(join(root, 'bin'))]

setup(
    name=project,
    version=pyspecs.__version__,
    py_modules=modules,
    scripts=scripts,
    url='https://github.com/mdwhatcott/{0}'.format(project),
    license='GPL',
    author='Michael Whatcott',
    author_email='mdwhatcott+{0}@gmail.com'.format(project),
    description='Concise BDD in python',
    long_description='{0} is a testing framework that strives to achieve '
                     'more readable specifications (tests) by leveraging '
                     'some fancy syntactic sugar and auto-discovery of '
                     'tests/specs.'.format(project),
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
