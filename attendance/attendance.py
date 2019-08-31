#!/usr/bin/python3
# Copyright (c) 2017-2019, The amFOSS contributors. All rights reserved

from datetime import datetime
import sys
import json

import requests
from urllib.request import urlopen
from subprocess import Popen, PIPE
from os.path import expanduser
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    file_path = "/opt/attendance/"
elif _platform == "darwin":
    home = expanduser("~")
    file_path = home+"/.amfoss/"

def check_internet_connection():
    try:
        status_code = urlopen('https://www.google.com').getcode()
        if status_code == 200:
            return True
    except:
        print("Internet error")
        return False
    return False


def get_bssid_list():
    list_bssid = []
    with open("list.txt") as f:
        for line in f:
            list_bssid.append(line.split("Address:"))
        lister = dict(list_bssid)
        ssid_list = list(lister.values())
        ssid_list = list(map(lambda s: s.strip(), ssid_list))
    return ssid_list


def get_credentials():
    credentials = ''
    try:
        with open(file_path + '.credentials', 'r') as file:
            credentials = file.readline()
    except EnvironmentError:
        print("Credentials error, run 'python3 get_and_save_credentials.py'")
    return credentials


def mark_attendance(lister , credentials):

    timestamp = datetime.now().isoformat()
    data = {'username': credentials['username'],'password': credentials['password'],'time': timestamp,'list': str(lister)  , 'secret':"sadsa"}
    variables = json.dumps(data)
    url = 'https://api.amfoss.in/?'
    mutation = '''
       mutation($username: String!, $password: String!, $time: DateTime!, $secret: String!, $list: String!)
            {
  LogAttendance(username: $username, password: $password,time: $time, secret: $secret, list: $list)
    {
    id
    }
}
    '''
    r = requests.post(url, json={'query': mutation, 'variables': variables})
    print(r.content)
    return False


if __name__ == '__main__':

    # check internet connection
    if not check_internet_connection():
        sys.exit()

    # get list of wifi ssid's
    wifi_bssid_list = get_bssid_list()

    if not wifi_bssid_list:
        sys.exit()

    credentials = json.loads(get_credentials())

   
    # Mark attendance
    mark_attendance(wifi_bssid_list ,credentials)
