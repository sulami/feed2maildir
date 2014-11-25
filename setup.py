from setuptools import setup

import feed2maildir

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='feed2maildir',
      version=feed2maildir.VERSION,
      description='Convert feeds to maildirs',
      long_description=readme(),
      url='https://github.com/sulami/feed2maildir',
      author='Robin Schroer',
      author_email='sulami@peerwire.org',
      license='ISC',
      packages=['feed2maildir'],
      zip_safe=False,
      classifiers=[
          'Development Status :: 3 - Alpha',
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

