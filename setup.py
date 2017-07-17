from setuptools import setup

setup(
  name='labstack',
  version='0.0.1',
  description='Official Python client library for the LabStack REST API',
  long_description='`<https://github.com/labstack/labstack-python>`_',
  keywords='labstack cube email log mqtt store',
  author='Vishal Rana',
  author_email='vr@labstack.com',
  license='MIT',
  install_requires=[
    'requests==2.18.1'
  ],
  classifiers=[
      'Programming Language :: Python :: 2.6',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.2',
      'Programming Language :: Python :: 3.3',
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6'
  ]
)