"""app.py - main app file"""

# import player data from constants.py
import constants

# special constant tuple to assist the menu functions
ALPHABET = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')

MENU_ERROR_MESSAGE = '\nInvalid choice. Please select a valid menu option.'

def get_height(player):
    """get_height(player)

    Returns a given player's height for the sake of the List.sort() function
    """
    return player['height']

def get_experience(player):
    """get_experience(player)

    Returns a given player's experience level for the sake of the List.sort() function
    """
    return player['experience']

def yes_or_no_to_bool(yes_or_no):
    """yes_or_no_to_bool(yes_or_no)

    Takes a string that contains the word "yes" or "no" and converts it to an
    equivalent boolean value. Will raise a ValueError if any other value is passed.
    That won't likely happen in this short program but it's good to be defensive.
    """
    if yes_or_no.upper() == 'YES':
        return True
    elif yes_or_no.upper() == 'NO':
        return False
    else:
        raise ValueError('Expected "yes" or "no" string value')

def clean_guardians(guardians):
    """clean_guardians(guardians)

    Turn the guardian names into a list and remove the 'and'
    """

    guardian_list = guardians.split(' and ')

    return guardian_list

def clean_data():
    """clean_data()

    Read the existing player data from the PLAYERS constants
    Clean the player data and build a new collection from it
    """
    players = []

    for player in constants.PLAYERS:
        new_player = {}
        new_player['height'] = int(player['height'].split()[0])
        new_player['experience'] = yes_or_no_to_bool(player['experience'])
        new_player['name'] = player['name']
        new_player['guardians'] = clean_guardians(player['guardians'])

        players.append(new_player)

    return players

def balance_teams(players):
    """balance_teams()

    Now that the player data has been cleaned, balance the players across
    the three teams: Panthers, Bandits and Warriors. Make sure the teams have
    the same number of total players on them when your team balancing function
    has finished.

    HINT: To find out how many players should be on each team, divide the length
    of players by the number of teams.
    Ex: num_players_team = len(PLAYERS) / len(TEAMS)
    """

    players.sort(key=get_experience)

    team_counter = 0
    for i, player in enumerate(players):
        if team_counter >= len(constants.TEAMS):
            team_counter = 0
        player['team'] = constants.TEAMS[team_counter]
        team_counter += 1

    return players

def print_stats(players, team):
    """print_stats(players, team)

    Displaying the stats
    When displaying the selected teams' stats to the screen you will want to include:

    * Team's name as a string"""
    print(f'\nTeam Name: {team}')

    """* Total players on that team as an integer"""
    players_on_team = [player['name'] for player in players if player['team'] == team]
    print(f'\nTeam Roster ({len(players_on_team)} players total)')

    """* The player names as strings separated by commas

    NOTE: When displaying the player names it should not just display the List
    representation object. It should display them as if they are one large comma
    separated string so the user cannot see any hints at what data type players
    are held inside.
    """
    print(', '.join(players_on_team))

    player_guardians = [player['guardians'] for player in players if player['team'] == team]

    print('\nGuardians:')
    guardian_str = ''
    second_guardian_str = ''

    for guardian_list in player_guardians:
        guardian_str += f'{guardian_list[0]}, '
        try:
            second_guardian_str += f'{guardian_list[1]}, '
        except IndexError:
            second_guardian_str += '              '

    print(guardian_str.rstrip(', '))
    print(second_guardian_str.rstrip(', '))

    print()

    experienced_players = len([player for player in players if player['team'] == team and
        player['experience']])
    inexperienced_players = len([player for player in players if player['team'] == team and
        not player['experience']])

    print(f'Inexperienced Players: {inexperienced_players}')
    print(f'Experienced Players: {experienced_players}')

    print()

    average_height = (sum([player['height'] for player in players
        if player['team'] == team]) / len(players_on_team))

    print(f'Avg. Height: {round(average_height, 2)}\n')

def sanitize_menu_option(choice, options=2):
    """sanitize_menu_option(choice, options=2)

    Ensures the user submitted a valid alphabetical menu option and raises a ValueError if not
    Takes a helpful options argument to provide flexibility in the number of possible menu options
    """
    uppercase_choice = choice.upper()

    for i in range(options):
        expected_choice = ALPHABET[i]
        if expected_choice == uppercase_choice:
            return expected_choice

    raise ValueError('Expected valid menu option')



def main_menu():
    """main_menu()

    Display the main menu to the user and return their response.
    """
    print("""----MENU----

    Here are your choices:
     A) Display Team Stats
     B) Quit\n""")

    valid_choice = ''

    while True:
        choice = input('\nEnter an option:  ')

        try:
            valid_choice = sanitize_menu_option(choice)
        except:
            print(MENU_ERROR_MESSAGE)
            continue

        return valid_choice


def team_menu():
    """team_menu()

    Display the list of teams as a menu and return the user's choice.
    """

    valid_choice = ''

    print()

    for i, team in enumerate(constants.TEAMS):
        print(f'{ALPHABET[i]}) {team}')

    choice_invalid = True
    while choice_invalid:
        choice = input('\nEnter an option:  ')

        try:
            valid_choice = sanitize_menu_option(choice, options=len(constants.TEAMS))
        except:
            print(MENU_ERROR_MESSAGE)
            continue

        choice_invalid = False

    for i, team in enumerate(constants.TEAMS):
        if valid_choice == ALPHABET[i]:
            return team

# dunder main
if __name__ == '__main__':
    players = clean_data()
    balanced_players = balance_teams(players)

    print('BASKETBALL TEAM STATS TOOL')
    print('By Renee Louise Brinkman\n')

    while True:
        menu_choice = main_menu()
        if menu_choice == 'A':
            selected_team = team_menu()
            print_stats(balanced_players, selected_team)
            input('Press enter to continue...')
            print()
        elif menu_choice == 'B':
            print()
            break
        else:
            # this shouldn't happen
            raise ValueError()
