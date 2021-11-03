#!/usr/bin/env bash

# navigate to /path/to/taxonomy_welder/JOSS_paper

docker run --rm \
    --volume $PWD:/data \
    --user $(id -u):$(id -g) \
    --env JOURNAL=joss \
    openjournals/paperdraft
