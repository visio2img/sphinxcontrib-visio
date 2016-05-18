from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Environment :: Win32 (MS Windows)',
    'Framework :: Sphinx :: Extension',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Documentation',
    'Topic :: Documentation :: Sphinx',
    'Topic :: Multimedia :: Graphics :: Graphics Conversion',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

setup(
    name='sphinxcontrib-visio',
    version='2.1.2',
    description='Sphinx "visio" extension; embed MS-Visio file (.vsd, .vsdx)',
    long_description=open('README.rst').read(),
    author='Yassu',
    author_email='mathyassu@gmail.com',
    maintainer='Takeshi KOMIYA',
    maintainer_email='i.tkomiya@gmail.com',
    url='https://github.com/visio2img/sphinxcontrib-visio',
    classifiers=classifiers,
    packages=['sphinxcontrib'],
    namespace_packages=['sphinxcontrib'],
    install_requires=[
        'Sphinx >= 1.0.0',
        'visio2img >= 1.2.0',
        'sphinxcontrib-imagehelper'
    ],
    tests_require=[
        'sphinx-testing >= 0.3.0',
    ],
)
