"""
Flask-rt
-------------

Realtime notification system for model state changes via pusher app
"""
from setuptools import setup


setup(
    name='Flask-rt',
    version='1.0',
    url='https://github.com/Odava/flask-rt',
    license='Proprietary',
    author='Steven Osborn',
    author_email='steven@odava.com',
    description='Notifies clients of model state changes via pusher app ',
    long_description=__doc__,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'pusher'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
