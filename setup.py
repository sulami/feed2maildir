from setuptools import setup

import feed2maildir

def readme():
    with open('README.rst') as f:
        return f.read()

def deps():
    with open('requirements.txt') as f:
        return f.readlines()

setup(name='feed2maildir',
      version=feed2maildir.VERSION,
      python_requires='>=3.2,<4',
      description='Convert feeds to maildirs',
      long_description=readme(),
      url='https://github.com/sulami/feed2maildir',
      author='Robin Schroer',
      author_email='feed2maildir@sulami.xyz',
      license='ISC',
      packages=['feed2maildir'],
      test_suite = 'feed2maildir.tests',
      zip_safe=False,
      install_requires=deps(),
      scripts=['scripts/feed2maildir',],
      classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: ISC License (ISCL)',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Internet',
          'Topic :: Utilities',
      ]
      )

