# DMPS

DMPS is a Python library for dealing with DMPS observations


## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. 


### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python 3](https://www.python.org)



## Installation

Clone the repository

```console
$ git clone https://github.com/gfogwill/dmps
$ cd dmps
```

Now let's install the requirements. But before we do that, we **strongly**
recommend creating a virtual environment with a tool such as
[virtualenv](https://virtualenv.pypa.io/en/stable/):

```console
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Every time you start a new session you need to activate the virtual environment.

```console
$ source venv/bin/activate
```


## Testing the code

```console
$ dmps info
```

If everything is OK you should see the program logo.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
