#!/bin/sh

# crontab
# */5 * * * * /usr/bin/bash /home/contact_acmucr/email-verification/build_main.sh

cd /home/contact_acmucr/email-verification

# Builds the `main` branch 
res=$(git pull origin main | grep Already)

if [[ ${res} =~ 'Already' ]]
then
    echo 'No updates to Discord Bot!'
else
    pkill -9 -f bot.py
    pip3 install -r requirements.txt
    nohup python3 -u bot.py &>> activity.log &
fi