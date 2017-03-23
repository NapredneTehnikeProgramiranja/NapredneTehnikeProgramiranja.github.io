#!/usr/bin/env sh

stack build
stack exec site clean
git submodule update
cd _site && git checkout master && cd ..
stack exec site build
cp README.md _site/README.md
cd _site && git add -A && git commit -m "publish" && git push origin master --force
