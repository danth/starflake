from os import path

from setuptools import find_packages, setup

__version__ = "0.9.0"

# Read long description from README.md
here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as readme:
    long_description = readme.read()


setup(
    name="starflake",
    version=__version__,
    description="A game about chemicals, played through a Discord bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Thwaites",
    author_email="danthwaites30@btinternet.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="Discord bot game chemical reaction",
    url="https://github.com/danth/starflake",
    project_urls={
        "Bug Reports": "https://github.com/danth/starflake/issues",
        "Source": "https://github.com/danth/starflake",
    },
    packages=find_packages(),
    python_requires=">=3.6,<4",
    install_requires=[
        "chickennuggets >=1,<2",
        "discord.py >=1.2.5,<2",
        "discordhealthcheck >=0.0.7,<1",
    ],
    entry_points={
        "console_scripts": [
            "starflake=starflake.__main__:launch",
        ],
    },
)
