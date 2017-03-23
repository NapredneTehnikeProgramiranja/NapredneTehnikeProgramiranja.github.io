#!/usr/bin/env sh

stack build
git submodule update
stack exec site build
cp README.md _site/README.md
cd _site && git add -A && git commit -m "publish" && git push origin master --force
