from distutils.core import setup

setup(
    name='FinChart',
    version='0.1',
    author='hantian.pang',
    packages=[
    ],
    install_requires=[
        'numpy', 'scipy', 'pandas',
        'tabulate', 'arrow',
        'psycopg2', 'pymongo', 'diskcache',
        'PyQt5', 'PyQtChart',
        'schedule',
        'requests', 'beautifulsoup4', 'urllib3', 'lxml',
        'arch'
    ],
    extras_require={
        'CTP': ['PyCTP'],
        'TSA': ['TorchTSA'],
    },
)
