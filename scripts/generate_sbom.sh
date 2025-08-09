#!/bin/sh
# Generate CycloneDX SBOM for the current Poetry environment
poetry export --without-hashes -f requirements.txt | cyclonedx-py requirements -o sbom.xml
