# DMPS

DMPS is a Python library for dealing with DMPS observations


## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. 


### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Example 1](https://www.example.com)
- [Example 2](https://www.example.com)


## Installation

Python 3.6+ is required to run code from this repo.

```console
$ git clone https://gitlab.smn.gov.ar/gfogwill/dmps
$ cd dmps
```

Now let's install the requirements. But before we do that, we **strongly**
recommend creating a virtual environment with a tool such as
[virtualenv](https://virtualenv.pypa.io/en/stable/):

```console
$ virtualenv -p python3 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```



## Running the tests


### Sample Tests


### Style test



Project Organization
------------
* `LICENSE`
* `Makefile`
    * top-level makefile. Type `make` for a list of valid commands
* `README.md`
    * this file
* `data`
    * Data directory. often symlinked to a filesystem with lots of space
    * `data/raw`
        * Raw (immutable) hash-verified downloads
    * `data/interim`
        * Extracted and interim data representations
    * `data/processed`
        * The final, canonical data sets for modeling.
* `docs`
    * A default Sphinx project; see sphinx-doc.org for details
* `models`
    * Trained and serialized models, model predictions, or model summaries
    * `models/trained`
        * Trained models
    * `models/output`
        * predictions and transformations from the trained models
* `notebooks`
    *  Jupyter notebooks. Naming convention is a number (for ordering),
    the creator's initials, and a short `-` delimited description,
    e.g. `1.0-jqp-initial-data-exploration`.
* `references`
    * Data dictionaries, manuals, and all other explanatory materials.
* `reports`
    * Generated analysis as HTML, PDF, LaTeX, etc.
    * `reports/figures`
        * Generated graphics and figures to be used in reporting
    * `reports/tables`
        * Generated data tables to be used in reporting
    * `reports/summary`
        * Generated summary information to be used in reporting
* `requirements.txt`
    * (if using pip+virtualenv) The requirements file for reproducing the
    analysis environment, e.g. generated with `pip freeze > requirements.txt`
* `environment.yml`
    * (if using conda) The YAML file for reproducing the analysis environment
* `setup.py`
    * Turns contents of `src` into a
    pip-installable python module  (`pip install -e .`) so it can be
    imported in python code
* `src`
    * Source code for use in this project.
    * `src/__init__.py`
        * Makes src a Python module
    * `src/data`
        * Scripts to fetch or generate data. In particular:
        * `src/data/make_dataset.py`
            * Run with `python -m src.data.make_dataset fetch`
            or  `python -m src.data.make_dataset process`
    * `src/analysis`
        * Scripts to turn datasets into output products
    * `src/models`
        * Scripts to train models and then use trained models to make predictions.
        e.g. `predict_model.py`, `train_model.py`
* `tox.ini`
    * tox file with settings for running tox; see tox.testrun.org


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
