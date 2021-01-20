import requests

API_KEY = 'XXXXXXXXXXXXXXXXX'
GetFriendsURL = 'https://api.steampowered.com/ISteamUser/GetFriendList/v1/'
GotOwnedURL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
GetPlayerSummariesURL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'


class SteamUser:  # user class
    # will probably create a "Game" class to make future changes easier (maybe a function to account for time played, etc)
    def __init__(self, userID):  # constructor accesses user data such as list of games played and friends
        self.userID = userID
        self.user_summary = requests.get(GetPlayerSummariesURL, params={'key': API_KEY, 'steamids': userID}).json()
        self.friendList = requests.get(GetFriendsURL, params={'key': API_KEY, 'steamid': int(userID)}).json()

    def get_user_library(self):  # returns the names of the user's games in a list
        game_list = set()
        user_list = requests.get(GotOwnedURL, params={'key': API_KEY, 'steamid': int(userID), 'include_appinfo': True, 'include_played_free_games': True}).json()
        for i in user_list["response"]["games"]:
            new_game = Game(i['appid'], i['name'], i['playtime_forever'])
            game_list.add(new_game)
        return game_list

    def get_profile_name(self):
        profile_name = self.user_summary['response']['players'][0]['personaname']
        return profile_name

    def get_friends_list(self):
        friend_names = set()
        for i in self.friendList["friendslist"]["friends"]:
            new_friend = SteamUser(i['steamid'])
            friend_names.add(new_friend)
        return friend_names

    def print_friend_list(self):
        friends_print = self.get_friends_list()
        for i in friends_print:
            print(i.get_profile_name())


class Game:  # Game class, will have all the necessary info for a game so it can be readily accessed
    def __init__(self, app_id, name, play_time):
        self.app_id = app_id
        self.name = name
        self.play_time = play_time

    def __eq__(self, other): #compares the appids of 2 Game objects
        #appid is the only completely unique variable in the object so it'll be the one compared
        self_id = self.app_id
        other_id = other.app_id
        return self_id == other_id