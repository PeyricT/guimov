from setuptools import setup, find_packages


setup(
    name='guimov',
    version='0.1.0',
    description='Graphical Interface for Multi-Omics Visualisation (with singlecell data)',
    url='https://gitlab.com/pfgt/sandbox/GUIMOVapp',
    author='Thibaut Peyric',
    author_email='thibaut.peyric@proton.me',
    license='BSD 2-clause',
    packages=find_packages(),
    package_data={'guimov': ['assets/*']},
    install_requires=['dash',
                      'dash_daq',
                      'muon',
                      'scanpy',
                      'plotly',
                      'dash_bootstrap_components',
                      'leidenalg',
                      'pandas',
                      'numpy',
                      'pillow',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
    ],

    entry_points={
        'console_scripts': [
            'guimov_launch = guimov._commands:_commands_guimov_launch',
        ],
    },

)
