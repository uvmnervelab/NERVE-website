#!/bin/bash

bundle exec jekyll build
rsync -avz ./_site/ w3_nervelab:www-root