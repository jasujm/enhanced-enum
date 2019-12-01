import os
import setuptools

package_dir = os.path.abspath(os.path.dirname(__file__))


def get_description():
    with open(os.path.join(package_dir, "README")) as f:
        return f.read()


setup_kwargs = dict(
    name="EnumECG",
    version="0.1.dev1",
    author="Jaakko Moisio",
    author_email="jaakko@moisio.fi",
    description="Generate Enhanced Enum definitions for C++",
    long_description=get_description(),
    license="MIT",
    url="https://github.com/jasujm/enhanced-enum",
    packages=["enumecg"],
    package_data={"enumecg": ["templates/*.in"]},
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
