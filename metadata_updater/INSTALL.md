# Installation instructions

## Requirements
* **Linux** - Operating System. In theory works with others OSs but not tested
* **Git**   - Source code storage and versioning
* **Python 3** - Programming language. Version > 3.2 required
* **setuptools** - download, build, install, upgrade, and uninstall Python packages


### Get source code

make a git dir if you do not have one

*  `mkdir ~/git`

change to git dir

*  `cd ~/git`

Clone lds-metadata-updater project
*  `git clone https://github.com/linz/lds-metadata-updater.git`


### Setup.py

ensure you are in the lds-metadata-updater project directiry 
*  `cd ~/git/lds-metadata-updater` 

create a virtual environment
* `python -m venv .venv`
* `.\.venv\Scripts\activate`

install metadata_update and its dependencies see [requirements.txt](requirements.txt)
* `python -m pip install --upgrade pip`
* `pip install -r requirements.txt`

#### DEPRICATED METHOD
There is no need to create a virtual environment 
Install metadata_updater and its dependencies see [requirements.txt](requirements.txt)
* `python3 setup.py install`
