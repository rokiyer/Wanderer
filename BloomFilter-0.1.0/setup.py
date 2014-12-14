import os

from setuptools import setup

fd = open('./README')
long_desc = fd.read()
fd.close()

setup(name='BloomFilter',
      version = '0.1.0',
      author="Ziang Guo",
      author_email="iziang@yeah.net",
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
      ],  
      py_modules=['bloom'],
      platforms=["Any"],
      license="BSD",
      keywords='A simple implement of bloom filter',
      description="A simple implement of bloom filter",
      long_description=long_desc
)
