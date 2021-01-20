import setuptools

with open("README.md", "r", encoding='utf-8') as f:
  long_description = f.read()

setuptools.setup(
  name="six-presence",
  version="v2.1.2",
  author="Matthew Kevin Amadeus",
  description="SIX presence function.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/mkamadeus/SIX-Automated-Presence",
  packages=setuptools.find_packages(),
  install_requires=[
    'beautifulsoup4',
    'requests',
    'html5lib'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)