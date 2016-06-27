from distutils.core import setup

setup(
    name='PyperV2012',
    version='0.1dev',
    packages=['pyperv2012', ],
    long_description=open('README.md').read(),
    install_requires=[
        "pywinrm >= 0.2.0",
        "json"
    ],
)
