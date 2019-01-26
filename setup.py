from setuptools import setup

setup(name='tnsdc',
      version='0.1.dev',
      description='A lightweight package for retrieving TNS discoveries and sending alerts.',
      scripts=['bin/tns_check'],
      url='https://github.com/benstahl92/tnsdc',
      author='Benjamin Stahl',
      author_email='benjamin_stahl@berkeley.edu',
      license='MIT',
      packages=['tnsdc'])