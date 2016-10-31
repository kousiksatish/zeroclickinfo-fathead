#!/bin/bash

mkdir -p download && cd download
rm -f *.html
rm -f *.json
wget --quiet https://angular.io/docs/ts/latest/api/api-list.json
cd ../
python fetch.py
