from setuptools import setup

setup(
    name='skrub-wreckers',

    description='Skrub wreckers MASLAB code',
    url='https://github.com/skrub-wreckers/software',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='maslab',
    packages=['sw'],
    install_requires=['tamproxy', 'opencv-python', 'pygame', 'scipy', 'numpy'],
)
