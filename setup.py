from setuptools import setup, find_packages


requirements = []


with open("requirements.txt") as f:
    requires = f.readlines()
    for require in requires:
        requirements.append(require.strip("\n"))


setup(
    name="amis_py",
    version="0.0.1",
    description="amis python wrapper",
    url="https://github.com/bstr9/amis-py",
    author="bstr",
    packages=find_packages(include=["*"]),
    license="Apache-2.0",
    include_package_data=True,
    install_requires=requirements
)
