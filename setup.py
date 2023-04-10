from setuptools import setup, find_packages

setup(name='ecgannotate',
      version='0.2.0',
      packages=['ecgannotate'],
      install_requires=[
           'numpy',
           'scipy',
           'PyQt5',
           'pyqtgraph',
           'py-ecg-detectors',
           ],
      entry_points={
        'console_scripts': [
            'ecgannotate=ecgannotate.gui:runGUI',
        ],
        },
      )