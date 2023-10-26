## Installation
To install the development environment:
  1. Install [pipenv](https://pypi.org/project/pipenv/) on your system.
  2. run `make setup`
     - This installs the npm build requirements and creates the pipenv 
  3. run `pipenv shell` to enter the development environment

## Testing

With your `pipenv` environment active, run `make test` to run the static and Playwright integration tests.

## Building JS Artifacts
Any JavaScript changes (in `makeblocks.js`) must be rebuilt into the distributed files using `make build-js`.

To prepare a full build for release, run `make build-dist`

## Release

To build a public a release to PyPI, run `make deploy-real`