from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
requires = open(os.path.join(here, 'requirements.txt')).read()
readme = open(os.path.join(here, 'README.txt')).read()

setup(
    name='pgsql2gist',
    version='0.2.2',
    author='Matthew Kenny',
    author_email='matthewkenny AT gmail DOT com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Intended Audience :: Developers'
    ],
    packages=['pgsql2gist'],
    entry_points = {
        'console_scripts': ['pgsql2gist=pgsql2gist.command_line:main'],
    },
    url='https://github.com/mattmakesmaps/pgsql2gist',
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    keywords='gis gists postgis postgresql geojson',
    description='like pgsql2shp, but for github gists',
    long_description=readme,
    install_requires=requires,
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    include_package_data=True
)
