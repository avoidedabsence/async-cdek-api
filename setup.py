from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("__init__.py", "r", encoding="utf-8") as fh:
    for line in fh:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "0.1.0"

setup(
    name="async-cdek-api",
    version=version,
    author="Alexey P.",
    author_email="i@apechenin.ru",
    description="An asynchronous Python client library for the CDEK API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/avoidedabsence/async-cdek-api",
    project_urls={
        "Bug Tracker": "https://github.com/avoidedabsence/async-cdek-api/issues",
        "Documentation": "https://github.com/avoidedabsence/async-cdek-api/blob/main/docs/API_REFERENCE.md",
        "Source Code": "https://github.com/avoidedabsence/async-cdek-api",
    },
    packages=find_packages(),
    py_modules=["client", "common"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Office/Business",
        "Typing :: Typed",
    ],
    python_requires=">=3.9",
    install_requires=[
        "aiohttp>=3.8.0",
        "pydantic>=2.0.0",
        "loguru>=0.6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    keywords=[
        "cdek",
        "delivery",
        "shipping",
        "logistics",
        "api",
        "async",
        "russia",
        "courier",
    ],
    include_package_data=True,
    zip_safe=False,
)
