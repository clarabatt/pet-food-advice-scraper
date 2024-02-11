# Pet Food Advice Scraper

This project is a web scraper that collects pet food information to create a database of pet food products.

## Environment Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management. 

**[Install Poetry following their documentation.](https://python-poetry.org/docs/#installation)**

Once Poetry is installed, make sure to configure it to create virtual environments within the project's directory:

> This is a recommended setting so it will be easier to delete the virtual environment if needed.

```bash
poetry config virtualenvs.in-project true
```

Install the dependencies using:

```bash
poetry install
```

This will install the dependencies and create a virtual environment for the project.

## Usage

To activate the virtual environment, use:

```bash
poetry shell
```

To run the project, use:

```bash
poetry run python main.py
```

This will run the main.py script within the project's virtual environment.
