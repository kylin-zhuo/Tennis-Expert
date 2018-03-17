#!/bin/bash

dt=$(date '+%m/%d/%Y %H:%M')

git add *
git commit -m "$dt"
git push