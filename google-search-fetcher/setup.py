import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google-search-fetcher-MXMASLIN",
    version="0.0.1",
    author="Maxim Maslin",
    author_email="mxmaslin@gmail.com",
    description="Fetches google search query result urls",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mxmaslin/otus_web/tree/master/google-search-fetcher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)