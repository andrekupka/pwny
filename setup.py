from distutils.core import setup


setup(
    name="pwny",
    version="0.1.3",
    author="André Kupka",
    author_email="kupka@in.tum.de",
    description="A small binary exploitation framework.",
    license="MIT",
    keywords="binary exploitation pwning pwny",
    url="https://github.com/fr3akout/pwny",
    packages=["pwny"],
    long_description="A small binary exploitation framework, that provides "
            "functionality to communicate with remote servers and write rop "
            "chains.",
    classifiers=[]
)
