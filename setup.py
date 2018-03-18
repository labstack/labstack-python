from setuptools import setup

setup(
  name='labstack',
  version='0.21.1',
  description='Official Python client library for the LabStack platform',
  long_description='`<https://github.com/labstack/labstack-python>`_',
  keywords='api, testing, monitoring, analytics',
  url='https://github.com/labstack/labstack-python',
  author='Vishal Rana',
  author_email='vr@labstack.com',
  license='MIT',
  packages=['labstack'],
  install_requires=[
    'requests==2.18.4',
    'psutil==5.4.3',
    'APScheduler==3.5.1'
  ],
  extra_requires=[
    'Flask==0.12.2'
  ],
  classifiers=[
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ]
)
