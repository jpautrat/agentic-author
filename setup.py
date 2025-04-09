from setuptools import setup, find_packages

with open("README_new.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements_updated.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="advanced-ai-book-generator",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A sophisticated AI-powered book generation system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/advanced-ai-book-generator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[req for req in requirements if not req.startswith("#")],
    entry_points={
        "console_scripts": [
            "ai-book-generator=main_updated:main",
        ],
    },
)
