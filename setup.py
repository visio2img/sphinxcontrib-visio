from setuptools import setup

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Environment :: Win32 (MS Windows)',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Documentation',
    'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

setup(
    name='sphinxcontrib-visio',
    version='1.0.2',
    description='Sphinx "visio" extension; embed MS-Visio file (.vsd, .vsdx)',
    long_description=open('README.rst').read(),
    author='Yassu',
    author_email='yassumath@gmail.com',
    maintainer='Takeshi KOMIYA',
    maintainer_email='i.tkomiya@gmail.com',
    url='https://github.com/visio2img/sphinxcontrib-visio',
    classifiers=classifiers,
    packages=['sphinxcontrib'],
    namespace_packages=['sphinxcontrib'],
    install_requires=[
        'Sphinx >= 1.0.0',
        'visio2img >= 1.2.0'
    ],
    tests_require=[
        'sphinx-testing',
    ],
)
