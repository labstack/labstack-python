from setuptools import setup

setup(
    name='labstack',
    version='1.0.1',
    description='Official Python client library for the LabStack API',
    long_description='`<https://github.com/labstack/labstack-python>`_',
    keywords='image compress, image resize, text summary, barcode generate, barcode scan',
    url='https://github.com/labstack/labstack-python',
    author='Vishal Rana',
    author_email='vr@labstack.com',
    license='MIT',
    packages=['labstack'],
    install_requires=[
        'requests==2.22.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
