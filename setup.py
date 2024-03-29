import setuptools

setuptools.setup(
    name = 'ZachsModules',
    version = '0.0.2',
    author = 'Zach Montgomery',
    author_email = 'zachary.s.montgomery@gmail.com',
    description = 'Collection of common functions and classes',
    # long_description = long_description,
    # long_description_content_type = 'test/markdown',
    url = 'https://github.com/ZachMontgomery/ZachsModules',
    packages = setuptools.find_packages(),
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    python_requires = '>=3.6',
    install_requires = ['numpy', 'datetime', 'jsonschema']
    )
