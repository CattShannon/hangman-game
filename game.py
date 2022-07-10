import os
import random
import re

from hangman_prints import display_hangman_scene, print_custom_message
from hangman_prints import display_player_word


USERS_FILE_ROUTE = "./sources/users.txt"
USERS_TEMP_FILE_ROUTE = "./sources/users_temp.txt"
DATA_WORDS_FILE_ROUTE = "./sources/data.txt"
GAME_INITIAL_POINTS = 10
GAME_BASE_RETRIES = 10


def get_game_word():
    words_list = []

    with open(DATA_WORDS_FILE_ROUTE, "r", encoding="utf-8") as words_file:
        words_list = [word for word in words_file]

    assert len(words_list) > 0, "Game file is empty" 

    return words_list[random.randint(0, len(words_list) - 1)].upper()


def is_a_valid_letter_input(letter):
    return len(letter) == 1 and letter != " "  


def get_player_input(player_word, round_status, round_retries):
    
    print_custom_message("Remaining attempts: " + str(round_retries))
    display_hangman_scene(round_status)
    display_player_word(player_word)
    player_interaction = input("Guess a letter: ")
    
    while not is_a_valid_letter_input(player_interaction): 
        print_custom_message("Invalid input, please enter just one letter.")
        display_hangman_scene(round_status)
        display_player_word(player_word)
        player_interaction = input("Guess a letter: ")

    return player_interaction


def calculate_percentage(part, whole_part):
    return int(100 * (part / whole_part))


def is_above_50_percent_limit(actual_retries, initial_retries):
    return calculate_percentage(actual_retries, initial_retries) <= 50


def check_letter_in_word_game(letter, word_game, player_word):
    new_player_word = []

    for position, char in enumerate(word_game):
        if char == letter:
            new_player_word.append(letter)
        elif player_word[position] == "_":
            new_player_word.append("_")
        else:
            new_player_word.append(player_word[position])

    return "".join(new_player_word)

    
def calculate_round_earned_points(round_retries, initial_round_retries, round_status):
    result = int(GAME_INITIAL_POINTS * (calculate_percentage(round_retries, initial_round_retries) / 100))

    if round_status != "loss" and result == 0:
        return 1
    
    return result


def update_users_file():
    os.remove(USERS_FILE_ROUTE)
    os.rename(USERS_TEMP_FILE_ROUTE, USERS_FILE_ROUTE)


def update_user_score(earned_points, user_info):

    with open(USERS_FILE_ROUTE, "r", encoding="utf-8") as users_r, open(USERS_TEMP_FILE_ROUTE, "w", encoding="utf-8") as users_w:
        users = [user for user in users_r if user != ""]

        for user in users:
            user_split = re.sub("\\n", "", user).split("|")
            
            if user_split[0] == user_info["username"]:
                users_w.write(user_info["username"] 
                              + "|" + user_info["password"] 
                              + "|" + str(int(user_split[2]) + earned_points))
                users_w.write("\n")
                continue
            
            users_w.write(user_split[0] + "|" + user_split[1] + "|" + user_split[2])
            users_w.write("\n")
    
    update_users_file()


def handle_winner(earned_points, user_info, word_game):
    print_custom_message("Congratulations " + user_info["username"] + ", you are a savior." +
                         "\nYou earned " + str(earned_points) + " points.")
    print("The hidden word was:", word_game)
    display_hangman_scene("victory")

    update_user_score(earned_points, user_info)


def play_game(user_info):
    word_game = get_game_word()
    word_game = re.sub("\\n", "", word_game)
    initial_round_retries = len(word_game) + GAME_BASE_RETRIES
    round_retries = initial_round_retries
    player_word = "".join(["_"] * len(word_game))
    round_status = "initial"

    while player_word.__contains__("_"):
        if round_retries < 1:
            round_status = "loss"
            break
        elif round_status != "scared" and is_above_50_percent_limit(round_retries, initial_round_retries):
            round_status = "scared"

        player_interaction = get_player_input(player_word, round_status, round_retries).upper()

        if word_game.__contains__(player_interaction):
            player_word = check_letter_in_word_game(player_interaction, word_game, player_word)
            continue

        round_retries -= 1

    earned_points = calculate_round_earned_points(round_retries, initial_round_retries, round_status)

    if round_status != "loss":
        handle_winner(earned_points, user_info, word_game)
    else:
        print_custom_message("You have lost. You earned 0 points.")
        print("The hidden word was:", word_game)
        display_hangman_scene(round_status)
    

def start_game(user_info): 
    keep_playing = True

    while keep_playing:
        play_game(user_info)

        keep_playing = int(input("""
Enter '1' to play again.
If you want to go back at menu enter anything.

        """))


def sort_scoreboard(users):

    for i in range(1, len(users)):
        item_to_insert = users[i]

        j = i - 1

        while j >= 0 and users[j]["points"] > item_to_insert["points"]:
            users[j + 1] = users[j]
            j -= 1

        users[j + 1] = item_to_insert

    return users[::-1]


def refresh_score_board():

    print_custom_message("Loading scoreboard...")

    users = []

    with open(USERS_FILE_ROUTE, "r", encoding="utf-8") as users_r, open(USERS_TEMP_FILE_ROUTE, "w", encoding="utf-8") as users_w:
        for user in users_r:
            user_split = re.sub("\\n", "", user).split("|")
            users.append({
                "username": user_split[0],
                "password": user_split[1],
                "points": int(user_split[2])
            })

        users = sort_scoreboard(users)

        for user in users:
            users_w.write(user["username"] + "|" + user["password"] + "|" + str(user["points"]))
            users_w.write("\n")

    update_users_file()
    return users


def look_the_the_scoreboard():
    users_scoreboard = refresh_score_board()
    print_custom_message("Players ranking: ")
    print("Position\tPlayerName\t\tPoints")
    
    for position, user in enumerate(users_scoreboard):
        print("{:<8}".format(str(position + 1)) + "\t" 
        + "{:<10}".format(user["username"]) + "\t\t" 
        + str(user["points"]))

    print("\n")
    input("Enter anyting to go back at menu.")


def game_menu(user_info):
    MENU = """

What do yo want to do?

1. Play
2. Look the scoreboard
3. Look your actual position in scoreboard 
4. exit

Enter the numeric code of your choice:
    """

    active_session = True

    operations = [
        lambda x: start_game(x), 
        lambda x: look_the_the_scoreboard(),
        lambda x: print("Feature unavailable.")
    ]

    while active_session:
        try:
            print_custom_message("Welcome to the Hangman game:")
            choice = int(input(MENU))

            if choice == 4:
                active_session = False
                print_custom_message("Bye.")
                break

            operations[choice - 1](user_info)
        except IndexError:
            print_custom_message("Invalid option.")
        except ValueError:
            print_custom_message("Invalid option.")