# Robot Framework IDE server

A simple server for querying and editing Robot Framework test data.

Very much Work In Progress, nothing in guaranteed to work.

Reads the given suite, parses it using RF modules and tries to import libraries & resource files.

## Usage
Start server with:
`git clone https://github.com/yanne/rideserver/`
`cd rideserver`
`python rideserver/main.py <path/to/your/testsuite>`

### Supported queries

* List files in the project: `curl http://127.0.0.1:5000/project`
* List all libraries used in the project: `curl http://127.0.0.1:5000/libraries`
* Search keywords by pattern from all libraries and resource files: `curl http://127.0.0.1:5000/search/keywords/<pattern>`
* Search test cases by tags: `curl http://127.0.0.1:5000/search/tests/<tagname>`


## Hacking

Strongly recommend using Virtualenv.

`git clone https://github.com/yanne/rideserver/`
`cd rideserver`
`mkvirtualenv rideserver`
`pip install -r requiremenst.txt`
