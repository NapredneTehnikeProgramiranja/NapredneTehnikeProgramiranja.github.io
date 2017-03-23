#!/usr/bin/env sh

git checkout develop

stack build
git submodule update
stack exec site build
cp README.md _site/README.md
git add -A && git commit -m "deploy"

# git checkout master
# git merge develop -X theirs

# shopt -s extglob
# rm -r !(.git|_site)
# cp _site/* .
# rm -r _site

# git add -A && git commit -m "publish" && git push

git checkout develop
