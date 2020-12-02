import setuptools  # type: ignore

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(  # type: ignore
    name="asus-charge-control-cforrester",
    version="1.0.0",
    author="Christopher Forrester",
    author_email="christopher@cforrester.ca",
    description="Set your recent ASUS notebook's maximum charge level on Linux.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cforrester1988/asus-charge-control",
    license="GPLv3+"
    packages=setuptools.find_packages(),  # type: ignore
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": ["asuscharge=asuscharge.asuscharge:main"],
    },
)
