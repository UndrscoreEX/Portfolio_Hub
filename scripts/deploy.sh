#!/bin/bash
#pull from github

cd /home/ubuntu/portfolio_proj
git stash
git pull origin main

cd /home/ubuntu/portfolio_proj/hub
sudo chown ubuntu:ubuntu db.sqlite3

