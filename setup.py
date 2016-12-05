#!/usr/bin/env python

from distutils.core import setup

import setuptools

setuptools  # Just for my editor

setup(name="Folivora",
      version="0.0.1",
      description="Tools to save energy with CT50 radio thermostats",
      author="Joerg Rings",
      author_email="mail@joergrings.com",
      url="https://github.com/jrings/folivora",
      packages=["folivora", "web"],
      )
