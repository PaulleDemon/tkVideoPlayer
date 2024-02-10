from setuptools import setup

with open("Readme.md", 'r') as f:
    long_description = f.read()

setup(
    name='tkvideoplayer',
    version='2.8',
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
    ],
    keywords=['tkinter', 'video', 'player', 'video player', 'tkvideoplayer', 'play video in tkinter'],
    packages=["tkVideoPlayer"],
    install_requires=["av==11.0.0", "pillow>=10.2.0"],
    include_package_data=True,
    python_requires='>=3.6',
)