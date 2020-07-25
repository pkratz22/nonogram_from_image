from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='RS_vs_PS',
    version='0.1',
    description='Get nonogram as array from image',
    long_description=readme,
    author='Peter Kratz',
    author_email='pkratz22@gmail.com',
    url='https://github.com/pkratz22/nonogram_from_image',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)