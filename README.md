# Bug Tracker 1.0

Bug Tracker 1.0 is a web application to track errors during the development and testing phase of a software product. It allows managers and project leaders to easily record and track problems in a central location. This bugs tracking tool is designed intuitively and easy to use while implements user-level security features to ensure that only authorized users can access their projects and bugs.

The application was created using Flask, a micro web framework written in Python, SQLite3 as RDBMS, Jinja2 for template management and the Bootstrap 4.x Framework.

### Installation

Get the project's code

```BASH
$ git clone https://github.com/Adminrivero/Bug-Tracker.git
$ cd Bug-Tracker
```

Install and activate virtual environment

```BASH
$ python3 -m venv venv
$ . venv/bin/activate
```

Install modules

```BASH
$ pip install -r requirements.text
```

## Usage

Set the FLASK_APP environment variable and the DEBUG environment

```BASH
$ export FLASK_APP=bugtracker
$ export FLASK_ENV=development
$
$ # Start the application (development mode)
$ flask run
$
$ # To create database file execute:
$ flask init-db
$
$ # To import sample data for Bug Tracker execute: (Optional)
$ flask import-db
```

## Author

* **Hector Rivero** - [GitHub Account](https://github.com/Adminrivero)
