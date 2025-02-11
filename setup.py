from setuptools import setup, find_packages


with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name='pictelligence',
    version='1.0.2',
    packages=find_packages(),
    install_requires=install_requires,
    package_data={'pictelligence': ['tags/*.txt', 'sample_photos/*']},
    include_package_data=True
)
