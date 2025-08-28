from setuptools import setup, find_packages

with open("README.adoc", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="adoc-link-checker",
    version="0.1.0",
    author="dhrions",
    description="Un outil en ligne de commande pour vérifier les liens brisés dans les fichiers AsciiDoc.",
    long_description=long_description,
    long_description_content_type="text/asciidoc",
    url="https://github.com/dhrions/adoc-link-checker",
    packages=find_packages(),
    install_requires=[
        "certifi==2025.8.3",
        "charset-normalizer==3.4.3",
        "click==8.2.1",
        "coverage==7.10.5",
        "idna==3.10",
        "iniconfig==2.1.0",
        "packaging==25.0",
        "pluggy==1.6.0",
        "Pygments==2.19.2",
        "pytest==8.4.1",
        "pytest-cov==6.2.1",
        "pytest-mock==3.14.1",
        "pytest-responses==0.5.1",
        "PyYAML==6.0.2",
        "requests==2.32.5",
        "responses==0.25.8",
        "urllib3==2.5.0"
    ],
    entry_points={
        "console_scripts": [
            "adoc-link-checker=adoc_link_checker.cli:cli",
        ],
    },
    python_requires=">=3.8",
    license="MIT",  # À adapter selon ta licence
    classifiers=[
        # "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.8",
        # "Programming Language :: Python :: 3.9",
        # "Programming Language :: Python :: 3.10",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
        # "Intended Audience :: Developers",
        # "Topic :: Software Development :: Quality Assurance",
        # "Topic :: Text Processing :: Markup :: AsciiDoc",
    ],
    keywords="asciidoc link checker broken links",
    project_urls={
        "Bug Tracker": "https://github.com/dhrons/adoc-link-checker/issues",
        "Source Code": "https://github.com/dhrons/adoc-link-checker",
    },
)
