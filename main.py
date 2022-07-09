import random
import math
import re

import hangman_draws
import os


USERS_FILE_ROUTE = "./sources/users.txt"


def print_game_message(message):
    os.system("cls")
    print(hangman_draws.GAME_TITLE)
    print(message)


def validate_player_ingress():

    user_input_ok = False
    username = input("Please enter your player name: ")

    while not user_input_ok:
        if username == "":
            print_game_message("Oh, something went worng...")
            username = input("Player name is mandatory, please enter one: ")
            continue

        user_input_ok = True
            
    return re.sub("\\s+", " ", username)


def find_user_info(username):
    user_info = {}

    with open(USERS_FILE_ROUTE, "r", encoding="utf-8") as user_file:
        for user in user_file:
            user_split = user.split("|")
            
            if user_split[0] == username:
                user_info = {
                    "username": user_split[0],
                    "password": user_split[1],
                    "points": int(user_split[2]),
                }

    return user_info


def user_sing_up(username): 
    print_game_message("Nice to meet you " + username)
    print("You are new here, you need to register now.")

    password_ok = False
    password = input("Please enter your password (minimum 4 characters): ")

    while not password_ok:
        if len(password) < 4:
            print_game_message("Invalid password.")
            password = input("Please enter your password (minimum 4 characters): ")
            continue
        
        password_ok = True

    with open(USERS_FILE_ROUTE, "a", encoding="utf-8") as users_file:
        users_file.write(username + "|" + password + "|0")
    
    print_game_message("Register sucessful.")


def user_login(user_info):
    print_game_message("Is good to see you again " + user_info["username"])  

    password_ok = False
    login_retries =  5
    password = input("Please enter your password: ")

    while not password_ok:
        
        assert login_retries > 0, "Login attempts exceeded"
            
        if password != user_info["password"]:
            print_game_message("Incorrect password. Remaining attempts " + str(login_retries))
            password = input("Please enter your password: ")
            login_retries -= 1
            continue
        
        password_ok = True

    print_game_message("Login sucessful.")


def read_words_file():
    pass


def run():

    login_ok = False

    while not login_ok:
        print_game_message("Welcome player, lets play :D")
        username = validate_player_ingress()
        user_info = find_user_info(username)

        try:
            if(len(user_info) == 0):
                user_sing_up(username)
            else:
                user_login(user_info)
        except AssertionError as e:
            print("Login error. Cause:", str(e))
            input("Enter anything to continue: ")
            continue
        
        login_ok = True


if __name__ == '__main__':
    run()

