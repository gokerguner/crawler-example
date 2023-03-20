from setuptools import setup

setup(
    name='myapp',
    version='1.0',
    description='My application',
    packages=['config', 'db'],
    py_modules=['crawler', 'run'],
    package_data={'config': ['*.json'], 'db': ['*.txt']},
    entry_points={
        'console_scripts': [
            'myapp = run:main',
        ],
    },
)

