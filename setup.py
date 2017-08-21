from setuptools import setup

setup(
  name='labstack',
  version='0.5.5',
  description='Official Python client library for the LabStack platform',
  long_description='`<https://github.com/labstack/labstack-python>`_',
  keywords='labstack cube email log mqtt store',
  url='https://github.com/labstack/labstack-python',
  author='Vishal Rana',
  author_email='vr@labstack.com',
  license='MIT',
  packages=['labstack'],
  install_requires=[
    'apscheduler==3.3.1',
    'requests==2.18.1',
    'arrow==0.10.0'
  ],
  classifiers=[
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6'
  ]
)
