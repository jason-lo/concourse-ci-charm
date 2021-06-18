# concourse-ci

## Description

Concourse-CI to be deployed on non-container cloud like LxD.

## Usage

charmcraft pack

juju deploy ./concourse-ci.charm


## Developing

Create and activate a virtualenv with the development requirements:

    virtualenv -p python3 venv
    source venv/bin/activate
    pip install -r requirements-dev.txt

## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
