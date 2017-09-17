from setuptools import setup

setup(
  name='labstack',
  version='0.7.1',
  description='Official Python client library for the LabStack platform',
  long_description='`<https://github.com/labstack/labstack-python>`_',
  keywords='labstack cube email log mqtt store',
  url='https://github.com/labstack/labstack-python',
  author='Vishal Rana',
  author_email='vr@labstack.com',
  license='MIT',
  packages=['labstack'],
  install_requires=[
    'arrow==0.10.0',
    'paho-mqtt==1.3.0',
    'requests==2.18.1'
  ],
  classifiers=[
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6'
  ]
)
