#!/usr/bin/env python
from distutils.core import setup

install_requires = [
    "awsiotsdk",
    "paho-mqtt",
    "planetmint-ipld",
]

setup(
    name='aws-iot',
    version='1.0',
    description='An application to interact with the IoT services from AWS',
    author='Christian Dienbauer',
    author_email='christian.dienbauer@gmx.at',
    packages=['src'],
    install_requires=install_requires,
)
