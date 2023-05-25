# ZachsModules
Common functions, classes, and other items that I use frequently for research and classwork.

## Documentation
Under construction. See docstrings.

## Installation

### Prerequisites

ZachsModules is dependent upon the python modules: 

### Getting Python

If you do not have Python installed on your machine, it can be downloaded from [https://www.anaconda.com/distribution/](https://www.anaconda.com/distribution/). Please be sure you have Python 3.6 or later.

### Getting the Source Code

You can either download the source as a ZIP file and extract the contents, or clone the PolyFits repository using Git. If your system does not already have a version of Git installed, you will not be able to use this second option unless you first download and install Git. If you are unsure, you can check by typing `git --version` into a command prompt.

#### Downloading source as a ZIP file (Not recommended)

1. Open a web browser and navigate to [https://github.com/ZachMontgomery/ZachsModules](https://github.com/ZachMontgomery/ZachsModules)
2. Make sure the Branch is set to `master`
3. Click the `Clone or download` button
4. Select `Download ZIP`
5. Extract the downloaded ZIP file to a local directory on your machine

#### Cloning the Github repository (Recommended)

1. From the command prompt navigate to the directory where ZachsModules will be installed. Note: git will automatically create a folder within this directory called ZachsModules. Keep this in mind if you do not want multiple nested folders called polyFits.
2. Execute

    $ git clone https://github.com/ZachMontgomery/ZachsModules.git

I recommend cloning from the repository, as this will allow you to most easily download and install periodic updates. This can be done by navigating to the root (ZachsModules/) directory and using the following command

    $ git pull

Please reinstall after pulling from the repository.

### Installing

Once you have the source code downloaded, navigate to the root (ZachsModules/) directory and execute

    $ pip install .

Please note that any time you update the source code (e.g. after executing a git pull), ZachsModules will need to be reinstalled by executing the above command.

### Testing the Installation

Once the installation is complete, run

    $ py.test

to verify ZachsModules is working properly on your machine. Full testing of all features is currently under construction.


## Support
For bugs, create a new issue on the Github repo.

## License
This project is licensed under the MIT license. See LICENSE file for more information.
