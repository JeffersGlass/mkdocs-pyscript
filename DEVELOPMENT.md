## Installation
To install the development environment:
  1. run `make setup`
     - This installs the npm build requirements and creates the conda development environment
  2. run `conda activate ./env` to enter the development environment

## Building JS Artifacts
Any JavaScript changes (in `makeblocks.js`) must be rebuilt into the distributed files using `make build` prior to release.