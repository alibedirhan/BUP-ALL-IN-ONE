# setup.py
from setuptools import setup, find_packages
import os

# Read version from VERSION file
version = "1.0.0"
if os.path.exists("VERSION"):
    with open("VERSION", "r") as f:
        version = f.read().strip()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

requirements = read_requirements('requirements.txt')

# Read README for long description
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="bupilic-management-system",
    version=version,
    author="Ali Bedirhan",
    author_email="alibedirhan@example.com",
    description="BupiliÇ İşletme Yönetim Sistemi - Comprehensive Business Management Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alibedirhan/BUP-ALL-IN-ONE",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'bupilic=bupilic_ana_program:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': [
            'icon/*.png',
            'ISKONTO_HESABI/*.py',
            'KARLILIK_ANALIZI/*.py',
            'MUSTERI_SAYISI_KONTROLU/*.py',
            'YASLANDIRMA/*.py',
            'YASLANDIRMA/GUI/*.py',
            'YASLANDIRMA/MODULES/*.py',
        ],
    },
    zip_safe=False,
)

# MANIFEST.in
include *.txt
include *.md
include *.py
include VERSION
recursive-include icon *.png *.ico
recursive-include ISKONTO_HESABI *.py
recursive-include KARLILIK_ANALIZI *.py  
recursive-include MUSTERI_SAYISI_KONTROLU *.py
recursive-include YASLANDIRMA *.py
recursive-include build *.py *.spec
recursive-include scripts *.bat *.sh
global-exclude *.pyc
global-exclude __pycache__
global-exclude *.log
global-exclude .git*
global-exclude dist/*
global-exclude build/*
prune tests
prune .pytest_cache

# VERSION file content
1.0.0
