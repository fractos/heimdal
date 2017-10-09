#!/bin/bash

aws s3 cp $(RULES_S3_URI) /opt/heimdal/rules.json

python -u /opt/heimdal/heimdal.py
