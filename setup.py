from setuptools import setup, find_packages

setup(
    name="gh_app_sandbox",
    author="Alex Ford",
    author_email='fordas@uw.edu',
    license="MIT license",
    description="Sandbox for github app integratioSandbox for github app integrationn",
    url='https://github.com/asford/gh_app_sandbox',

    version='0.1.0',

    packages=find_packages(),
    entry_points={
        'console_scripts' : [
        'git-credential-github-app-auth='
            'gh_app_sand.cli:credential',
        'ghapp='
            'gh_app_sand.cli:main',
        ]
    },
    python_requires='>=3.6',
    install_requires=[
        open("requirements.txt").read()
    ],

    test_requires=["pytest"],
)
