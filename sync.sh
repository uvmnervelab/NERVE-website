#!/bin/bash

bundle exec jekyll build
rsync -avz ./_site/ w3:www-root