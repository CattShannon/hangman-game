import re

from hangman_prints import print_custom_message
from game import game_menu


USERS_FILE_ROUTE = "./sources/users.txt"

def start_program():
    login_ok = False
    user_info = {}

    while not login_ok:
        print_custom_message("Welcome player, lets play :D")
        username = validate_player_ingress()
        user_info = find_user_info(username)

        try:
            if(len(user_info) == 0):
                user_sing_up(username)
            else:
                user_login(user_info)
        except AssertionError as e:
            print("Login error. Cause:", str(e))
            input("Press enter to continue ")
            continue
        
        login_ok = True
    
    return user_info


def validate_player_ingress():

    user_input_ok = False
    username = input("""    
Please enter your player name

Minimum 3 characters
Maximum 10 characters
    """)

    while not user_input_ok:
        if username == "":
            print_custom_message("Oh, something went worng...")
            username = input("Player name is mandatory, please enter one: ")
            continue
        elif len(username) < 3:
            print_custom_message("Your username is not enough long (Min. 3 characters)")
            username = input("Please enter your player name: ")
            continue
        elif len(username) > 10:
            print_custom_message("Your username is too long (Max. 10 characters)")
            username = input("Please enter your player name: ")
            continue

        user_input_ok = True
            
    return re.sub("\\s+", " ", username)


def find_user_info(username):
    user_info = {}

    with open(USERS_FILE_ROUTE, "r", encoding="utf-8") as user_file:
        for user in user_file:
            user_split = re.sub("\\n", "", user).split("|")
            
            if user_split[0] == username:
                user_info = {
                    "username": user_split[0],
                    "password": user_split[1],
                    "points": int(user_split[2]),
                }

    return user_info


def user_sing_up(username): 
    print_custom_message("Nice to meet you " + username)
    print("You are new here, you need to register now.")

    password_ok = False
    password = input("Please enter your password (minimum 4 characters): ")

    while not password_ok:
        if len(password) < 4:
            print_custom_message("Invalid password.")
            password = input("Please enter your password (minimum 4 characters): ")
            continue
        
        password_ok = True

    with open(USERS_FILE_ROUTE, "a", encoding="utf-8") as users_file:
        users_file.write(username + "|" + password + "|0\n")
    
    print_custom_message("Register sucessful.")


def user_login(user_info):
    print_custom_message("Is good to see you again " + user_info["username"])  

    password_ok = False
    login_retries =  5
    password = input("Please enter your password: ")

    while not password_ok:
        
        assert login_retries > 0, "Login attempts exceeded"
            
        if password != user_info["password"]:
            print_custom_message("Incorrect password. Remaining attempts " + str(login_retries))
            password = input("Please enter your password: ")
            login_retries -= 1
            continue
        
        password_ok = True

    print_custom_message("Login sucessful.")


def run():
    user_info = start_program()
    game_menu(user_info)

if __name__ == '__main__':
    run()

