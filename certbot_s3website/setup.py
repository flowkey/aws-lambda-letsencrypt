from distutils.core import setup
from setuptools import find_packages

setup(
    name='certbot-s3website',
    version='0.0.1',
    description="",
    packages=find_packages(),
    entry_points={
        'certbot.plugins': [
            'auth = certbot_s3website:Authenticator',
            'installer = certbot_s3website:Installer',
        ],
    },
)
