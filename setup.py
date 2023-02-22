from setuptools import setup

setup(name='ecgannotate',
      version='0.1.0',
      packages=['ecgannotate'],
      install_requires=[
           'numpy',
           'scipy',
           'PyQt5',
           'pyqtgraph',
           ],
      entry_points={
        'console_scripts': [
            'test_run = ecgannotate.gui:main',
        ]
      },
      )