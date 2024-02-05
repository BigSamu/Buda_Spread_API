#!/bin/bash

# Run coverage commands
coverage run -m pytest && coverage report -m && coverage-badge -of assets/coverage.svg
