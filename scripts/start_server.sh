#!/bin/bash

#start server up again
sudo systemctl start portfolio_app.service

sleep 10
cd cd /home/ubuntu/portfolio_proj/hub
python manage.py migrate
sleep 10



