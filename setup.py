import setuptools

with open("requirements.txt", "r+", encoding="utf-8") as file:
    dependences = file.read().strip().split("\n")

with open("README.md", "r+", encoding="utf-8") as file:
    long_description = file.read()

with open("version", "r+", encoding="utf-8") as file:
    version = file.read().strip()


setuptools.setup(
    name="bedrock-world-operator",
    version=version,
    author="Minecraft Muti-Media Organization",
    author_email="TriM-Organization@hotmail.com",
    description="An operator based on Go that aims to provide interface for Python that could operating NetEase/Standard Minecraft bedrock game saves.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TriM-Organization/bedrock-world-operator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        "bedrockworldoperator": [
            "dynamic_libs/*.so",
            "dynamic_libs/*.dll",
            "dynamic_libs/*.dylib",
        ],
    },
    package_dir={"bedrockworldoperator": "python/package"},
    packages=[
        i.replace("package", "bedrockworldoperator", 1)
        for i in setuptools.find_packages(where="python")
    ],
    install_requires=dependences,
    python_requires=">=3.11",
)
