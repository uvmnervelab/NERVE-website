#!/bin/bash

cd ..
npm run build && rsync -avz --delete dist/ w3_nervelab:www-root/