from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="devdaily-tools",
    version="0.3.1",
    author="Shek-YH",
    author_email="yinghaushek001@gmail.com",
    description="A practical CLI toolkit for developer daily workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shek-YH/devdaily-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "rich>=13.0.0",
        "click>=8.0.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "pdf": ["markdown>=3.4.0", "pdfkit>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "devdaily=devdaily.cli:main",
        ],
    },
)
