#!/usr/bin/env bash

PROJECT_DIRECTORY=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/..
SITES_DIRECTORY="sites"

# Set default active site
RICHIE_SITE="${RICHIE_SITE:-funmooc}"

export PROJECT_DIRECTORY
export SITES_DIRECTORY
export RICHIE_SITE
