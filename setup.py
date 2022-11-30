from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name='aniparse',
    version='1.1.1',
    description="An anime video filename parser",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/MeGaNeKoS/aniparse',
    license='License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    author='めがねこ',
    author_email='evictory91+pypackages@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=find_packages(),
    keywords=['anime', 'filename parser']
)
