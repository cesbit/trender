"""setup.py

Upload to PyPI, Thx to: http://peterdowns.com/posts/first-time-with-pypi.html

python setup.py sdist
twine upload --repository pypitest dist/trender-x.x.x.tar.gz
twine upload --repository pypi dist/trender-x.x.x.tar.gz
"""
from distutils.core import setup

VERSION = '1.0.9'

setup(
    name='trender',
    packages=['trender'],
    version=VERSION,
    description='Template Render Engine written in pure Python',
    author='Jeroen van der Heijden',
    author_email='jeroen@cesbit.com',
    url='https://github.com/transceptor-technology/trender',
    download_url='https://github.com/transceptor-technology/'
                 'trender/tarball/{}'.format(VERSION),
    keywords=['template', 'engine', 'render'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML'
    ],
)
