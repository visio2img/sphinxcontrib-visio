from setuptools import setup

setup(
    name='sphinxcontrib-visio',
    version='1.0.2',
    author='Yassu',
    author_email='yassumath@gmail.com',
    maintainer='Takeshi KOMIYA',
    maintainer_email='i.tkomiya@gmail.com',
    url='https://github.com/visio2img/sphinxcontrib-visio',
    description='Python reStructuredText directive for embedding visio image',
    license='apachae2',
    packages=['sphinxcontrib'],
    install_requires=[
        'visio2img >= 1.2.0'
    ],
    namespace_packages=['sphinxcontrib'],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ]
)
