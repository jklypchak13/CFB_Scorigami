# CFB_Scorigami

This is an attempt at creating a scori-gami related table similar to [this](https://nflscorigami.com/) but for college football.

## Dependency Installation

This project utilizes [pipenv](https://pypi.org/project/pipenv/) to manage it's dependencies. First, install pipenv

```bash
pip install pipenv
```

Then, to use pipenv to install the dependencies run

```bash
pipenv install
```

This will then install the dependencies, and create a virtual environment. To enter that environment, run

```bash
pipenv shell
```

## Generate the Site

This project utilizes Jinja in order to generate the website as a static html file. Once you have followed the previous steps, simply run

```bash
python src/generate_pages.py
```

This will take some time to execute, as all games from 1869 need to be scraped. However, these games will be stored locally on your machine after the first execution. The exception is the current year, which will be scraped each time (in order to get the up to date games).

## Acknowledgements

First, I would like to thank [ACMerriman](https://github.com/ACMerriman) for the original creation of Scorigami. This was his idea, and I am simply translating it to college football as well. Second, I would like to thank [Sports Reference](https://www.sports-reference.com) for providing the data on the games.
