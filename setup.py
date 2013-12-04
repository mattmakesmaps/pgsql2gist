from distutils.core import setup

setup(
    name='pgsql2gist',
    version='0.2.0',
    author='Matthew Kenny',
    author_email='matthewkenny AT gmail DOT com',
    packages=['pgsql2gist'],
    scripts=['pgsql2gist.py'],
    url='https://github.com/mattmakesmaps/pgsql2gist',
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    description='like pgsql2shp, but for github gists',
    long_description=open('README.txt').read(),
    install_requires=['psycopg2']
)
