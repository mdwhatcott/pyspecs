from distutils.core import setup


setup(
    name='pyspecs',
    version='1.0',
    packages=['pyspecs', 'tests'],
    scripts=['bin/pyspecs'],
    url='http://github.com/mdwhatcott/pyspecs',
    license='GPL',
    author='Michael Whatcott',
    author_email='mdwhatcott+pyspecs@gmail.com',
    description='Minimalistic BDD in Python',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Documentation',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ]
)
