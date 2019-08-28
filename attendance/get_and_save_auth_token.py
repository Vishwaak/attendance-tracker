import getpass
import json
import sys
import requests
file_path = "./"

def get_and_save_auth_token():
    print("Enter your amFOSS website username and password.")
    username = input("username: ")
    password = getpass.getpass("Password: ")
    data = {"username": username, "password": password}
    #Saves username and password
    with open('.credentials', 'w') as file:
        json.dump(data, file)
        print("Token successfully saved, please run this script whenever you change your credentials.")

if __name__ == '__main__':
    get_and_save_auth_token()
