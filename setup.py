from setuptools import setup

setup(
  name='labstack',
  version='0.31.6',
  description='Official Python client library for the LabStack platform',
  long_description='`<https://github.com/labstack/labstack-python>`_',
  keywords='image compress, image resize, text summary, barcode generate, barcode scan',
  url='https://github.com/labstack/labstack-python',
  author='Vishal Rana',
  author_email='vr@labstack.com',
  license='MIT',
  packages=['labstack'],
  install_requires=[
    'requests==2.18.1'
  ],
  classifiers=[
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6'
  ]
)
