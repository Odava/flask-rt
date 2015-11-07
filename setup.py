"""
Flask-rt
-------------

Realtime notification system for model state changes via pusher app
"""
from setuptools import setup, find_packages

setup(
    name='Flask-rt',
    version='1.1',
    url='https://github.com/Odava/flask-rt',
    license='Proprietary',
    author='Steven Osborn',
    author_email='steven@odava.com',
    description='Notifies clients of model state changes via pusher app ',
    long_description=__doc__,
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        'Flask',
        'pusher',
        'sqlalchemy'
    ]
)
