#!/bin/bash

# install pip, git and requests
sudo apt install python3-pip git -y
sudo -H pip3 install requests

# clone the repo
cd
git clone https://github.com/Vishwaak/attendance-tracker.git
cd attendance-tracker/

# Store configuration files
sudo rm /opt/attendance/ -rf
sudo mkdir /opt/attendance
sudo cp ./attendance/* -r /opt/attendance/
touch /opt/attendance/list.txt
sudo chmod +x /opt/attendance/config /opt/attendance/attendance.py /opt/attendance/get_bssid_names.sh
# Add a new cron-job
# write out current crontab
sudo crontab -l > mycron || touch mycron
# echo new cron into cron file, run every 15 mins
echo "*/15 * * * * /opt/attendance/config" >> mycron
# install new cron file
sudo crontab mycron
rm mycron

cd ..
rm -rf attendance-tracker/

cd /opt/attendance/
sudo python3 get_and_save_credentials.py
cd ~
