from setuptools import setup, find_packages

setup(
    name="preparelatexforsubmission",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "prepare-latex-submission=preparelatexforsubmission.main:main",
        ],
    },
    author="Flavio Piccoli",
    author_email="dros1986@gmail.com",
    description="A tool to flatten directories and update paths in LaTeX projects for journal submission.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dros1986/preparelatexforsubmission",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
