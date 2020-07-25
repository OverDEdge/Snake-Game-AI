try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'An AI adaption of my version of a Snake Game with Pygame',
    'author': 'Niklas Moberg',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'niklasm85@gmail.com',
    'version': '0.1',
    'install_requires': ['pygame', 'neat'],
    'packages': ['snake'],
    'scripts': [],
    'name': 'SnakeGameAi'
}


setup(**config)
