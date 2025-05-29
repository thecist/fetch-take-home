#!/bin/bash
pip install datamodel-code-generator

# Explicitly specify the input format as OpenAPI
datamodel-codegen --input ./scripts/pydantic/api.yaml --input-file-type openapi --output model.py
