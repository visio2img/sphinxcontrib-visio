from setuptools import setup

setup(
    name='visioimg',
    version='1.0.0',
    author='Yassu',
    author_email='yassumath@gmail.com',
    url='https://github.com/yassu/VisioInRst',
    description='Python reStructuredText directive for embedding visio image',
    license='MIT',
    packages=['visioimg'],
    install_requires=[
        'visio2img'
    ],
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    ]
)
