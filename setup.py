import os

from setuptools import setup


def read(f):
    here = os.path.abspath(os.path.dirname(__file__))
    return open(os.path.join(here, f), encoding='utf-8').read().strip()


setup(
    name='djed.templates',
    version='0.1.dev0',
    description='Template layers for Pyramid',
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.txt'))),
    classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Djed developers',
    author_email='djedproject@googlegroups.com',
    url='https://github.com/djedproject/djed.templates',
    license='ISC License (ISCL)',
    keywords='djed pyramid templates layer renderer',
    packages=['djed.templates'],
    include_package_data = True,
    install_requires=[
        'pyramid >= 1.4',
        'pyramid_chameleon',
        'setuptools',
    ],
    extras_require={
        'testing': [
            'djed.testing',
        ],
    },
    entry_points={
        'console_scripts': [
            'djed-templates = djed.templates.script:main',
        ],
    },
    test_suite = 'nose.collector',
  )
