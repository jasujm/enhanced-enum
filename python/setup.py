import os
import re
import setuptools
import sys

dunder_re = re.compile(r'^__(?P<name>[a-z]+)__ += +"(?P<value>[^"]+)"')
package_dir = os.path.abspath(os.path.dirname(__file__))


def get_description():
    with open(os.path.join(package_dir, "README")) as f:
        return f.read()


def get_package_dunder(name):
    with open(os.path.join(package_dir, "enumecg", "__init__.py")) as f:
        for row in f:
            m = dunder_re.match(row)
            if m and m.group("name") == name:
                return m.group("value")
    print(f"__{name}__ unexpectedly not found in module", file=sys.stderr)
    sys.exit(1)


setup_kwargs = dict(
    name="EnumECG",
    version=get_package_dunder("version"),
    author=get_package_dunder("author"),
    author_email="jaakko@moisio.fi",
    description="Generate Enhanced Enum definitions for C++",
    long_description=get_description(),
    license="MIT",
    url="https://github.com/jasujm/enhanced-enum",
    packages=["enumecg"],
    package_data={"enumecg": ["templates/*.in", "templates/doxygen/*.in"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["Jinja2>=2.10", "regex", "inflect>=3.0"],
)

# This is to bootstrap the build in case it is made with Enhanced Enum
# CMake toolchain
if os.environ.get("IS_CMAKE_BUILD"):
    setup_kwargs["package_dir"] = {"": package_dir}

setuptools.setup(**setup_kwargs)
