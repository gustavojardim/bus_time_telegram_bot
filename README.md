# Bus departure time via Telegram
Telegram bot programmed in Python to search for the next depertature time of a particular bus line on a bus company site.

## Setup guide
Clone this repo inside the folder you desire

Install **pipenv** with the following in the command line
```
pip install pipenv
```
Once you have installed pipenv, enter the repo folder and run
```
pipenv shell # This command creates a python virtual environment
pipenv install # This command shall install all the dependencies from Pipfile
```
If ```pipenv install``` fails to install the dependencies, do the following
```
pipenv lock
pipenv install
```
The upper commands will updated the Pipfile.lock with the dependencies from Pipfile, and then install the dependencies described in the **.lock** file.
