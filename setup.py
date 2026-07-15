from setuptools import setup, find_packages

setup(
    name="blackjack-casino",
    version="1.0.0",
    author="trupio882",
    author_email="trupio882@gmail.com",
    description="Console Blackjack game with multiple players and tables",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trupio882/blackjack-casino",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "blackjack-casino=main:main",
        ],
    },
)