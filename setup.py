from setuptools import setup, find_packages


install_requires = [
    "google-auth-oauthlib",  # for google
    "handofcats",
    "requests",
]
dev_requires = ["black", "flake8", "mypy"]
tests_requires = ["pytest"]

setup(
    classifiers=[
        # "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
    ],
    python_requires=">3.5",
    packages=find_packages(exclude=["cliauth.tests"]),
    install_requires=install_requires,
    extras_require={"testing": tests_requires, "dev": dev_requires},
    tests_require=tests_requires,
    test_suite="cliauth.tests",
    #     entry_points="""
    #       [console_scripts]
    #       cliauth = cliauth.cli:main
    # """,
)
