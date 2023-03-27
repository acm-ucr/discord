#!/bin/sh

# crontab
# */5 * * * * source /home/contact_acmucr/.bashrc; /home/contact_acmucr/email_verification/build_main.sh

cd /home/contact_acmucr/email_verification

exec > >(tee -a -i /home/contact_acmucr/email_verification/buildlog.txt)
exec 2>&1

# Builds the `main` branch 
res=$(git pull origin main | grep Already)

if [[ ${res} =~ 'Already' ]]
then
    echo 'No updates to Discord Bot!'
else
    pkill -9 -f discordbot.py
    pip3 install -r requirements.txt
    python3 discordbot.py
fi