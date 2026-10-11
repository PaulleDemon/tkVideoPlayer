from setuptools import setup
from pathlib import Path

long_description = Path("Readme.md").read_text(encoding="utf-8")

setup(
    name='tkvideoplayer',
    version='3.0',
    description="This library helps you play video files in tkinter",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Paul',
    url="https://github.com/PaulleDemon/tkVideoPlayer",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
        "Programming Language :: Python :: 3.11"
        "Programming Language :: Python :: 3.12"
        "Programming Language :: Python :: 3.13"
    ],
    keywords=['tkinter', 'video', 'player', 'video player', 'tkvideoplayer', 'play video in tkinter'],
    packages=["tkVideoPlayer"],
    install_requires=["av==9.2.0", "pillow>=9.0.1"],
    include_package_data=True,
    python_requires='>=3.6',
)