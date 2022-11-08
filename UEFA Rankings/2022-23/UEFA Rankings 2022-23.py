from tkinter import ROUND
import pandas as pd
import sys
# import matplotlib.pyplot as plt
from dataclasses import dataclass

#Struct used to define key statistics for teams and countries in (a) given UEFA competition(s)
@dataclass
class Competition:
    record : list
    games : list
    points : float

    def record(self) -> list:
        return self.record

    def games(self) -> list:
        return self.games

    def points(self) -> float:
        return self.points

#Struct used to define UEFA Countries
@dataclass
class Country:
    name: str
    rank: int
    teams: list

    def name(self) -> str:
        return self.name
    
    def rank(self) -> int:
        return self.rank

    def teams(self) -> list:
        return self.teams

#Struct used to define UEFA Teams
@dataclass
class Team:
    name: str
    coefficient: int
    country: str
    champions_league : Competition
    europa_league : Competition
    conference_league : Competition
    bonus_points : float
    #badge : str

    def name(self) -> str:
        return self.name
    
    def coefficient(self) -> int:
        return self.rank

    def country(self) -> list:
        return self.country

    def champions_league(self) -> Competition:
        return self.champions_league

    def europa_league(self) -> Competition:
        return self.europa_league

    def conference_league(self) -> Competition:
        return self.conference_league

    def bonus_points(self) -> float:
        return self.bonus_points

#Struct used to define the result for a team in a game.
@dataclass
class Result:
    team: str
    rating: str
    points: float

    def team(self) -> str:
        return self.team

    def rating(self) -> str:
        return self.rating

    def points(self) -> float:
        return self.points

#Struct used to define a singular game
@dataclass
class Game:
    id: int
    score: str
    result1: Result
    result2: Result

    def id(self) -> int:
        return self.id

    def score(self) -> str:
        return self.score
    
    def result1(self) -> Result:
        return self.result1

    def result2(self) -> Result:
        return self.result2

# Used as a function which initializes the starting stats of a team for a competition.
def init_competition():
    return (Competition([0, 0, 0], [], 0))

##############################################################################################################

# Used to assign every team to a country
TEAM_TO_COUNTRY = [ ("England", ["Manchester City", "Liverpool", "Chelsea", "Tottenham Hotspur", "Arsenal", "Manchester United", "West Ham United"]),
                    ("Spain", ["Real Madrid", "Barcelona", "Atlético Madrid", "Sevilla", "Real Betis", "Real Sociedad", "Villarreal"]),
                    ("Italy", ["Milan", "Inter Milan", "Napoli", "Juventus", "Lazio", "Roma", "Fiorentina"]),
                    ("Germany", ["Bayern Munich", "Borussia Dortmund", "Bayer Leverkusen", "RB Leipzig", "Union Berlin", "SC Freiburg", "1. FC Köln", "Eintracht Frankfurt"]),
                    ("France", ["Paris Saint-Germain", "Marseille", "Monaco", "Nantes", "Rennes", "Nice"]),
                    ("Portugal", ["Porto", "Sporting CP", "Benfica", "Braga", "Gil Vicente", "Vitória de Guimarães"]),
                    ("Netherlands", ["Ajax", "PSV Eindhoven", "Feyenoord", "Twente", "AZ"]),
                    ("Russia", []),
                    ("Belgium", ["Club Brugge", "Union Saint-Gilloise", "Gent", "Anderlecht", "Antwerp"]),
                    ("Austria", ["Red Bull Salzburg", "Sturm Graz", "Austria Wien", "Wolfsberger AC", "Rapid Wien"]),
                    ("Scotland", ["Celtic", "Rangers", "Heart of Midlothian", "Dundee United", "Motherwell"]),
                    ("Ukraine", ["Shakhtar Donetsk", "Dynamo Kyiv", "Dnipro-1", "Zorya Luhansk", "Vorskla Poltava"]),
                    ("Turkey", ["Trabzonspor", "Fenerbahçe", "Sivasspor", "Konyaspor", "İstanbul Başakşehir"]),
                    ("Denmark", ["Copenhagen", "Midtjylland", "Silkeborg", "Brøndby", "Viborg"]),
                    ("Cyprus", ["Apollon Limassol", "AEK Larnaca", "Omonia", "APOEL", "Aris Limassol"]),
                    ("Serbia", ["Red Star Belgrade", "Partizan", "Čukarički", "Radnički Niš"]),
                    ("Czech Republic", ["Viktoria Plzeň", "Slovácko", "Slavia Prague", "Sparta Prague"]),
                    ("Croatia", ["Dinamo Zagreb", "Hajduk Split", "Osijek", "Rijeka"]),
                    ("Switzerland", ["Zürich", "Lugano", "Basel", "Young Boys"]),
                    ("Greece", ["Olympiacos", "Panathinaikos", "PAOK", "Aris"]),
                    ("Israel", ["Maccabi Haifa", "Hapoel Be'er Sheva", "Maccabi Tel Aviv", "Maccabi Netanya"]),
                    ("Norway", ["Bodø/Glimt", "Molde", "Viking", "Lillestrøm"]),
                    ("Sweden", ["Malmö FF", "AIK", "Djurgårdens IF", "Elfsborg"]),
                    ("Bulgaria", ["Ludogorets Razgrad", "Levski Sofia", "CSKA Sofia", "Botev Plovdiv"]),
                    ("Romania", ["CFR Cluj", "Sepsi Sfântu Gheorghe", "FCSB", "Universitatea Craiova"]),
                    ("Azerbaijan", ["Qarabağ", "Neftçi Baku", "Zira", "Gabala"]),
                    ("Kazakhstan", ["Tobol", "Kairat", "Astana", "Kyzylzhar"]),
                    ("Hungary", ["Ferencváros", "Kisvárda", "Puskás Akadémia", "Fehérvár"]),
                    ("Belarus", ["Shakhtyor Soligorsk", "Gomel", "BATE Borisov", "Dinamo Minsk"]),
                    ("Poland", ["Lech Poznań", "Raków Częstochowa", "Pogoń Szczecin", "Lechia Gdańsk"]),
                    ("Slovenia", ["Maribor", "Koper", "Olimpija Ljubljana", "Mura"]),
                    ("Slovakia", ["Slovan Bratislava", "Spartak Trnava", "Ružomberok", "DAC Dunajská Streda"]),
                    ("Liechtenstein", ["Vaduz"]),
                    ("Lithuania", ["Žalgiris", "Sūduva", "Kauno Žalgiris", "Panevėžys"]),
                    ("Luxembourg", ["F91 Dudelange", "Racing Union", "Differdange 03", "Fola Esch"]),
                    ("Bosnia and Herzegovina", ["Zrinjski Mostar", "Velež Mostar", "Tuzla City", "Borac Banja Luka"]),
                    ("Republic of Ireland", ["Shamrock Rovers", "St Patrick's Athletic", "Sligo Rovers", "Derry City"]),
                    ("North Macedonia", ["Shkupi", "Makedonija Gjorče Petrov", "Akademija Pandev", "Shkëndija"]),
                    ("Armenia", ["Pyunik", "Ararat-Armenia", "Alashkert", "Ararat Yerevan"]),
                    ("Latvia", ["RFS", "Valmiera", "Liepāja", "Riga"]),
                    ("Albania", ["Tirana", "Vllaznia", "Laçi", "Partizani"]),
                    ("Northern Ireland", ["Linfield", "Crusaders", "Cliftonville", "Larne"]),
                    ("Georgia", ["Dinamo Batumi", "Saburtalo Tbilisi", "Dinamo Tbilisi", "Dila Gori"]),
                    ("Finland", ["HJK", "KuPS", "SJK", "Inter Turku"]),
                    ("Moldova", ["Sheriff Tiraspol", "Petrocub Hîncești", "Milsami Orhei", "Sfîntul Gheorghe"]),
                    ("Malta", ["Hibernians", "Floriana", "Ħamrun Spartans", "Gżira United"]),
                    ("Faroe Islands", ["KÍ Klaksvík", "B36 Tórshavn", "HB", "Víkingur"]),
                    ("Kosovo", ["Ballkani", "Llapi", "Drita", "Gjilani"]),
                    ("Gibraltar", ["Lincoln Red Imps", "Europa", "St Joseph's", "Bruno's Magpies"]),
                    ("Montenegro", ["Sutjeska Nikšić", "Budućnost Podgorica", "Dečić", "Iskra"]),
                    ("Wales", ["The New Saints", "Bala Town", "Newtown"]), 
                    ("Iceland", ["Víkingur Reykjavík","Breiðablik","KR"]),
                    ("Estonia", ["FCI Levadia", "Paide Linnameeskond","Flora"]),
                    ("Andorra", ["Inter Club d'Escaldes", "Atlètic Club d'Escaldes", "UE Santa Coloma"]),
                    ("San Marino", ["La Fiorita", "Tre Fiori", "Tre Penne"])]

# England = Country("England", 1, [])
# England.teams.append("Chelsea")
# print(England)

##############################################################################################################

#List of all UEFA Wiki page as panda tables
CHAMPIONS_LEAGUE_WIKI = pd.read_html('https://en.wikipedia.org/wiki/2022%E2%80%9323_UEFA_Champions_League')
EUROPA_LEAGUE_WIKI = pd.read_html('https://en.wikipedia.org/wiki/2022%E2%80%9323_UEFA_Europa_League')
CONFERENCE_LEAGUE_WIKI = pd.read_html('https://en.wikipedia.org/wiki/2022%E2%80%9323_UEFA_Europa_Conference_League')

# Initializes a dictionary conatining three dictionaries for each competition, with each containing the index of dataframe corresponding to each round.
# For the first item in the dictionary that has not been set up in the wiki, this should be marked with -1
INDEX_CHAMPIONS_LEAGUE = {"Teams":6, "Preliminary Round":8, "First Round":10, "Second Round":11, "Third Round":13, "Playoff Round":15, "Group Stage":17,
                          "Round of 16":-1, "Quarter Finals":13, "Semi Finals":14, "Final":15}
INDEX_EUROPA_LEAGUE = {"Teams":6, "Third Round":8, "Playoff Round":10, "Group Stage":11, "KO Playoff":-1, "Round of 16":11,
                       "Quarter Finals":7, "Semi Finals":8, "Final":9}
INDEX_CONFERENCE_LEAGUE = {"Teams":6, "First Round":8, "Second Round":9, "Third Round":11, "Playoff Round":13, "Group Stage":15, "KO Playoff":-1,
                           "Round of 16":11, "Quarter Finals":12, "Semi Finals":13, "Final":14}
INDEX_COMPETITION_LIST = {"Champions League":INDEX_CHAMPIONS_LEAGUE, "Europa League":INDEX_EUROPA_LEAGUE, "Conference League":INDEX_CONFERENCE_LEAGUE}

# Initializes a dictionary conatining three dictionaries for each competition, with each containing the dataframes corresponding to the matches of each round.
PANDA_CHAMPIONS_LEAGUE = {}
PANDA_EUROPA_LEAGUE = {}
PANDA_CONFERENCE_LEAGUE = {}
PANDA_COMPETITION_LIST = {"Champions League":PANDA_CHAMPIONS_LEAGUE, "Europa League":PANDA_EUROPA_LEAGUE, "Conference League":PANDA_CONFERENCE_LEAGUE}

# Initializes a dictionary matching each wiki with competition string.
WIKI_COMPETITION_LIST = {"Champions League":CHAMPIONS_LEAGUE_WIKI, "Europa League":EUROPA_LEAGUE_WIKI, "Conference League":CONFERENCE_LEAGUE_WIKI}

# Initializes a dictionary that helps to consolidate match information for each competition.
# Format contains tuples where the first three entries are the number of iterations of tuples and the 
# last entry marks whether to concatenate dataframes vertically or horizontally (0 -> v, 1 -> h)
TABLE_ITERATIONS = {"Preliminary Round": (2, 0, 0, 0), "Second Round": (2, 0, 2, 0), "Third Round": (2, 2, 2, 0), "Playoff Round": (2, 1, 2, 0), "Group Stage": (8, 8, 8, 1)}

# First entry is Champions League, second entry is Europa League, and third entry is Conference League.
# This is mapped with the dictionary below
COMPETITION_INDEX = {"Champions League":0, "Europa League":1, "Conference League":2}

# Sets up a list with the required dataframes given both the wikis and saved csvs.
# Can toggle the "test" field to print each dataframe, to ensure accuracy of function.
# The "save_point" denotes the point in the dataframes from which we want to load data from the
# our saved CSV files; everything after this point will be downloaded from the wikipedia page. 
def set_dataframes(save_point:str, new_names:bool, test:bool):
    for competition in INDEX_COMPETITION_LIST:
        upload_from_csv = True
        # Save point should be marked "N/A" if we do not want to take data from csv file.
        # If there are no CSV files currently present, this should always be the case.
        if save_point == "N/A":
            upload_from_csv = False
        index_dict = INDEX_COMPETITION_LIST[competition]
        panda_dict = PANDA_COMPETITION_LIST[competition]
        wiki = WIKI_COMPETITION_LIST[competition]
        for key in index_dict:
            # new_names indicates whether or not we want to import the teams directly from wiki
            csv_name = "save files/" + competition + " " + key + ".csv"
            if key == "Teams":
                if new_names:
                    ind = index_dict[key]
                    dataframe = wiki[ind]
                    dataframe.to_csv(csv_name)
                else:
                    dataframe = pd.read_csv(csv_name)
            else:
                # The first element with -1 as its index indicates when the wiki stops listing round matches
                if index_dict[key] == -1:
                    break
                if upload_from_csv:
                    dataframe = pd.read_csv(csv_name)
                else:
                    if key in TABLE_ITERATIONS:
                        dataframe = pd.DataFrame()
                        tup = TABLE_ITERATIONS[key]
                        iter = tup[COMPETITION_INDEX[competition]]
                        index = index_dict[key]
                        ax = tup[3]
                        for i in range(iter):
                            dataframe = pd.concat([dataframe, wiki[index+i]], axis=ax)
                        dataframe.to_csv(csv_name, index=False)
                    else:
                        ind = index_dict[key]
                        dataframe = wiki[ind]
                        dataframe.to_csv(csv_name, index=False)
                if key == save_point:
                    upload_from_csv = False
            panda_dict[key] = dataframe
            if test:
                print(competition + " " + key + " dataframe:")
                print(dataframe)
    return

#Dictionary of UEFA Countries and teams for easy access
COUNTRIES = {}
TEAMS = {}

# Sets the list of UEFA Countries based off of TEAMS_TO_COUNTRIES Table
# Set new_save to true if you want to pull countries from wikipedia page again.
def set_countries(new_save:bool):
    if new_save:
        dataframe = pd.DataFrame()
        # Check to make sure below range matches table range in the wikipedia page.
        for j in range(2, 5):
            tmp = CHAMPIONS_LEAGUE_WIKI[j]
            dataframe = pd.concat([dataframe, tmp], axis=0)
        dataframe.to_csv("save files/UEFA Countries.csv")
    else:
        dataframe = pd.read_csv("save files/UEFA Countries.csv", usecols=[1,2,3,4,5])

    temp = dataframe.values
    for i in range(len(temp)):
        country = temp[i]
        COUNTRIES[country[1]] = (Country(country[1], country[0], []))

    for country in COUNTRIES:
        for entry in range(len(TEAM_TO_COUNTRY)):
            if(COUNTRIES[country].name == TEAM_TO_COUNTRY[entry][0]):
                for team in TEAM_TO_COUNTRY[entry][1]:
                    COUNTRIES[country].teams.append(team)
    return

#Sets the list of UEFA Teams based off of the COUNTRIES TABLE
# Need to call "set_countries()" first
def set_teams():
    for country in COUNTRIES:
        for team in COUNTRIES[country].teams:
            TEAMS[team] = (Team(team, -1, COUNTRIES[country].name, init_competition(),
                            init_competition(), init_competition(), 0))

##############################################################################################################

#Sets the coefficient of every team given in the wiki table
#In order to be preformed correctly, this function should be called in order of competition prestige.
def set_coefficients(wiki_table):
    coefficient_dict = {"1st" : 1, "2nd" : 2, "3rd" : 3, "4th" : 4, "5th" : 5, 
                        "6th" : 6, "7th" : 7, "EL" : 8, "Abd-1st" : 1, "Abd-2nd" : 2,
                        "Abd-3rd" : 3, "Abd-4th" : 4, "Abd-5th" : 5}
    for row in wiki_table:
        for index in range(2, len(row)):
            team_str = row[index]
            try:
                float(team_str)
            except ValueError:
                team_list = team_str.replace('(', '|').replace(')', '|').split('|')
                if team_list[0].strip() in TEAMS:
                    team = TEAMS[team_list[0].strip()]
                    if team.coefficient == -1:
                        country = COUNTRIES[team.country]
                        country_rank = country.rank
                        num_teams = len(country.teams)
                        if "CW" == team_list[1]:
                            domestic_place = num_teams-1
                        elif "PW" == team_list[1]:
                            domestic_place = num_teams
                        elif "LC" == team_list[1]:
                            domestic_place = num_teams-1
                        else:
                            domestic_place = coefficient_dict[team_list[1]]
                        team.coefficient = (1-.01*country_rank) - (.01*domestic_place-.01)
                # else:
                #     print(team_list[1])
    return

# set_coefficients(CHAMPIONS_LEAGUE_WIKI[7].values)
# set_coefficients(EUROPA_LEAGUE_WIKI[7].values)
# set_coefficients(CONFERENCE_LEAGUE_WIKI[7].values)

def check_coefficients():
    for team in TEAMS:
        team_check = TEAMS[team]
        if team_check.coefficient == -1:
            print("Error: The following team has been assigned an invalid coefficient - ", team_check.name)
    return

# print(TEAMS)
# print(COUNTRIES)

##############################################################################################################

# Represents a global variable that is continuously update every time a game is processed.
GAME_ID_NUM = 0

# Is a dictionary mapping all calculated games to there ID number.
GAMES = {}

# Is a dictionary which maps a tuple relating a specific round in a given competition to a list of its corresponding game ids.
ROUNDS_TO_GAMES= {}

# Building block function that takes in two team structs, a score, and a penalty winner field
#    and outputs a Game struct
def game_calc(team1_name:str, team2_name:str, score:str, pw:int)->Game:
    global GAME_ID_NUM
    if score == "—":
        return None
    goals = score.replace("(", "–").split("–")
    # Different checks to ensure the game is valid:
    if team1_name not in TEAMS or team2_name not in TEAMS:
        return None
    if len(goals) != 2 or len(goals[0]) == 0:
        return None
    if not (pw == 1 or pw == 0 or pw == -1):
        return None
    
    team1 = TEAMS[team1_name]
    team2 = TEAMS[team2_name]
    goal_difference = int(goals[0])-int(goals[1])
    gd = goal_difference*.125
    os1 = team2.coefficient
    os2 = team1.coefficient
    winner = goal_difference/(abs(goal_difference) if goal_difference else 1)
    tiebreaker = {1:(2, "W"), 0:(1, "D"), -1:(0.5, "L")}
    winner_dict1 = {1:(3,"W"), 0:tiebreaker[pw], -1:(0,"L")}
    winner_dict2 = {1:(0,"L"), 0:tiebreaker[-pw], -1:(3,"W")}
    tmp1 = winner_dict1[winner]
    tmp2 = winner_dict2[winner]
    mr1 = tmp1[0]
    mr2 = tmp2[0]
    rating1 = tmp1[1]
    rating2 = tmp2[1]
    points1 = (mr1+gd)*os1+os1 if gd>=0 else mr1+os1+gd
    points2 = (mr2-gd)*os2+os2 if -gd>=0 else mr2+os2-gd

    id = GAME_ID_NUM
    GAME_ID_NUM += 1

    result1 = (Result(team1.name, rating1, points1))
    result2 = (Result(team2.name, rating2, points2))
    game = (Game(id, score, result1, result2))
    return game

##############################################################################################################

def single_game_from_row(game_row, test):
    pw = 0
    team1 = game_row[0]
    team2 = game_row[2]

    unadapt_score = game_row[1]
    tmp = unadapt_score.replace("p", "(").replace("[", "(").split("(")
    score = tmp[0].strip()
    if len(tmp) > 2 and "–" in tmp[2]:
        penalties = tmp[2].split("–")
        print(int(penalties[0]), int(penalties[1]))
        if len(penalties) != 2:
            print("Error: single game function error w/ penalties:")
            print(team1, ", ", team2, ", ", score, ", 0")
            return None
        elif int(penalties[0]) > int(penalties[1]):
            pw = 1
        else:
            pw = -1
    
    game = game_calc(team1, team2, score, pw)
    if game == None and test:
        print("Game not valid: ", team1, ", ", team2, ", ", score, ", ", pw)
    return game

def double_game_from_row(game_row, test):
    team1 = game_row[0]
    team2 = game_row[2]

    score1 = game_row[3]
    unadapt_score2 = game_row[4]
    tmp = unadapt_score2.split("(")
    score2 = tmp[0].strip()

    games = []
    game1 = game_calc(team1, team2, score1, 0)
    game2 = game_calc(team1, team2, score2, 0)
    if game1 != None:
        games.append(game1)
    elif test:
        print("Game not valid: ", team1, ", ", team2, ", ", score1, ", 0")
    if game2 != None:
        games.append(game2)
    elif test:
        print("Game not valid: ", team1, ", ", team2, ", ", score2, ", 0")
    return games
    # print("Game 1: ", team1, team2, score1)
    # print("Game 2: ", team1, team2, score2)
    # return

def group_stage_from_rows(table_rows, test):
    if len(table_rows) != 4:
        print("Group Stage Table Error.")
        return None
    unadapt_team = [[] for i in range(4)]
    team = ["" for i in range(4)]
    for j in range(4):
        unadapt_team[j] = table_rows[j][1].split(" (")
        team[j] = unadapt_team[j][0]

    games = []
    for k in range(4):
        for l in range(4):
            team1 = team[k]
            team2 = team[3-l]
            score = table_rows[k][-(l+1)]
            game = game_calc(team1, team2, score, 0)
            if game != None:
                games.append(game)
            elif test:
                print("Game not valid: ", team1, ", ", team2, ", ", score, ", 0")
            # game = (team1, team2, score, 0)
            # games.append(game)
    return games

def final_from_dtf(dataframe):
    return

##############################################################################################################

MATCH_TYPES = {"Preliminary Round": "single", "Group Stage":"group", "Final":"single"}

# Funcition that performs and stores calculations for all games in a given round
# Valid entries for match type include "single", "double", and "group"
# comp_and_round should be entered as a tuple with a string representing the competition in the first index,
#    and the round in the second index
def round_calc(dataframe, match_type:str, comp_and_round:tuple, test:bool):
    rows = dataframe.values
    game_list = []
    if match_type == "group":
        for ind in range(len(rows[0])//16):
            fi = 16*ind
            bi = 16*(ind+1)
            group_rows = rows[:, fi:bi]
            games = group_stage_from_rows(group_rows, test)
            for game in games:
                id = game.id
                GAMES[id] = game
                game_list.append(id) 
    elif match_type == "single":
        for row in rows:
            game = single_game_from_row(row, test)
            if game != None:
                id = game.id
                GAMES[id] = game
                game_list.append(id)
    elif match_type == "double":
        for row in rows:
            two_games = double_game_from_row(row, test)
            for game in two_games:
                id = game.id
                GAMES[id] = game
                game_list.append(id)
    else:
        print("Error: Not given valid match type.")
    ROUNDS_TO_GAMES[comp_and_round] = game_list
    return

##############################################################################################################
ROUND_STATS = {}

def calc_round_stats(comp_and_round):
    rating_to_index = {"W":0, "D":2, "L":1}
    ROUND_STATS[comp_and_round] = {}
    curr_round_stats = ROUND_STATS[comp_and_round]
    game_list = ROUNDS_TO_GAMES[comp_and_round]
    for id in game_list:
        game = GAMES[id]
        team_results = [0, 0]
        team_results[0] = game.result1
        team_results[1] = game.result2
        for team_result in team_results:
            team_name = team_result.team
            if team_name not in curr_round_stats:
                curr_round_stats[team_name] = init_competition()
            team_stats = curr_round_stats[team_name]
                
            # Updates record for the round
            record_index = rating_to_index[team_result.rating]
            team_stats.record[record_index] += 1

            # Updates the games for a given team for a game
            team_stats.games.append(id)

            # Updates the points for a team given a game
            team_stats.points += team_result.points
    return

def calc_rounds_comp(comp):
    comp_list = PANDA_COMPETITION_LIST[comp]
    for round in comp_list:
        if round != "Teams":
            calc_round_stats((comp, round))
    return

def calc_all_rounds():
    for comp in PANDA_COMPETITION_LIST:
        calc_rounds_comp(comp)
    return

##############################################################################################################
# Is a dictionary used to map the round a team reaches and the amount of bonus points they receive
BONUS_POINTS = {"Preliminary Round" : 0.1,
                "First Round" : 0.1,
                "Second Round" : 0.2,
                "Third Round" : 0.3,
                "Playoff Round" : 0.5,
                "Group Stage" : 1.0,
                "KO Playoff" : 1.0,
                "Round of 16" : 0.7,
                "Quarter Finals" : 0.7,
                "Semi Finals" : 0.7,
                "Final" : 0.7}

def find_bonus_points(comp_and_round):
    if "Champions League" == comp_and_round[0]:
        if comp_and_round[1] == "Round of 16":
            return 3
        return 3*BONUS_POINTS[comp_and_round[1]]
    elif "Europa League" == comp_and_round[0]:
        return 1.5*BONUS_POINTS[comp_and_round[1]]
    elif "Conference League" == comp_and_round[0]:
        return BONUS_POINTS[comp_and_round[1]]
    else:
        print("Error: find_bonus_points: Input invalid.")
        return 0


# Calculates the total points, record, and games played of every team in a given competition
# "All" may also be a valid input to the function, calculating these values for every competition.
def calc_competition(competition):
    if competition == "All":
        comps = PANDA_COMPETITION_LIST
    else:
        comps = {competition:PANDA_COMPETITION_LIST[competition]}
    for team in TEAMS:
        latest_round = "N/A"
        for comp in comps:
            comp_list = PANDA_COMPETITION_LIST[comp]
            for round in comp_list:
                if (comp, round) in ROUND_STATS and team in ROUND_STATS[(comp, round)]:
                    round_stats = ROUND_STATS[(comp, round)][team]

                    # Selects which competition field to modify
                    if comp == "Champions League":
                        total_stats = TEAMS[team].champions_league
                    elif comp == "Europa League":
                        total_stats = TEAMS[team].europa_league
                    elif comp == "Conference League":
                        total_stats = TEAMS[team].conference_league
                    else:
                        print("Error: Competition is invalid.")
                        return

                    # Updates total record
                    for ind in range(len(total_stats.record)):
                        total_stats.record[ind] += round_stats.record[ind]

                    # Updates total number of games
                    for id in round_stats.games:
                        total_stats.games.append(id)

                    # Updates point total
                    total_stats.points += round_stats.points

                    # Adds either bonus points for single round if the team has competed in previous rounds,
                    # or all of the bonus points in the competition up to the round the team is currently competing in.
                    if latest_round == "N/A":
                        # Adds up all of the previous rounds team did not participate in to get total bonus points 
                        for comp_and_round in ROUND_STATS:
                            if comp == comp_and_round[0]:
                                TEAMS[team].bonus_points += find_bonus_points(comp_and_round)
                            if (comp, round) == comp_and_round:
                                if comp == "Europa League":
                                    TEAMS[team].bonus_points += 0.6
                                elif comp == "Conference League":
                                    TEAMS[team].bonus_points += 0.1
                                break
                    else:
                        # For Preliminary Round UCL teams dropping into the UECL Second Round
                        if latest_round == "Preliminary Round" and (comp, round) == ("Conference League", "Second Round"):
                            TEAMS[team].bonus_points += find_bonus_points((comp, "First Round"))
                        # For First Round UCL teams who were selected for a bye to the UECL Third Round
                        if latest_round == "First Round" and (comp, round) == ("Conference League", "Third Round"):
                            TEAMS[team].bonus_points += find_bonus_points((comp, "Second Round"))
                        # For League Path teams dropping from UCL 3rd round into Europa League Group Stage
                        if latest_round == "Third Round" and (comp, round) == ("Europa League", "Group Stage"):
                            TEAMS[team].bonus_points += find_bonus_points((comp, "Playoff Round"))
                        # For first place teams in the group stage of the UEL and UECL advancing directly to the R16 KO's
                        if latest_round == "Group Stage" and (comp == "Europa League" or comp == "Conference League") and round == "Round of 16":
                            TEAMS[team].bonus_points += find_bonus_points((comp, "KO Playoff"))
                        TEAMS[team].bonus_points += find_bonus_points((comp, round))
                    latest_round = round
    return

##############################################################################################################

# Creates a list structure that forms a ranking for the specified competition.
# COULD POSSIBLY ADD FORM PRETTY EASILY TO THIS IN THE FUTURE
def init_ranking(competition):
    if competition == "All":
        comps = PANDA_COMPETITION_LIST
    else:
        comps = {competition:PANDA_COMPETITION_LIST[competition]}
    team_stats = [[] for i in range(len(TEAMS))]
    ind = 0
    for team_name in TEAMS:
        # initialize array holding important information for each team
        row = [0 for j in range(8)]
        team = TEAMS[team_name]
        row[1] = team_name
        row[7] = team.country

        # Selects which competition field to modify
        raw_points = 0
        games_played = 0
        bonus_points = 0
        for comp in comps:
            if comp == "Champions League":
                total_stats = team.champions_league
            elif comp == "Europa League":
                total_stats = team.europa_league
            elif comp == "Conference League":
                total_stats = team.conference_league
            else:
                print("Error: Competition is invalid.")
                return

            # Updates point total for competition
            raw_points += total_stats.points

            # Updates games played for the competition
            games_played += len(total_stats.games)

            # Updates total record
            for index in range(len(total_stats.record)):
                row[4+index] += total_stats.record[index]

        # Updates the number of bonus points received for a competition.
        bonus_points = team.bonus_points
        final_points = raw_points/(games_played if games_played != 0 else 1) + bonus_points
        row[2] = final_points
        row[3] = games_played
        team_stats[ind] = row
        ind += 1

    final_rank = sorted(team_stats, key=lambda stats: stats[2], reverse=True)
    ind = 1
    for new_team in final_rank:
        new_team[0] = ind
        ind += 1
    return final_rank

# Creates a ranking for all of the countries participating in UEFA Competitions.
def init_country_rank():
    country_rank_dict = {}
    club_rank = init_ranking("All")
    for row in club_rank:
        if row[7] not in country_rank_dict:
            country_rank_dict[row[7]] = [0 for i in range(9)]
        country_stats = country_rank_dict[row[7]]
        country_stats[2] += 1
        country_stats[3] += row[2]
        for ind in range(4, 8):
            country_stats[ind+1] += row[ind-1]
    
    country_rank = [[] for j in range(len(country_rank_dict))]
    index = 0
    for country in country_rank_dict:
        new_row = country_rank_dict[country]
        new_row[1] = country
        new_row[4] = new_row[3]/new_row[2]
        country_rank[index] = new_row
        index += 1
    
    final_rank = sorted(country_rank, key=lambda stats: stats[4], reverse=True)

    index = 1
    for new_country in final_rank:
        new_country[0] = index
        index += 1
    return final_rank

# Puts club ranking into csv form
def club_rank_to_csv(final_rank, competition):
    col = ["Rank", "Team", "Points", "Games Played", "Wins", "Losses", "Draws", "Country"]
    dataframe = pd.DataFrame(final_rank, columns=col)
    dataframe.to_excel("UEFA "+competition+" Ranking 2022-23.xlsx", index=False)

# Puts country ranking into csv form
def country_rank_to_csv(final_rank):
    col = ["Rank", "Country", "# of Teams", "Overall Points", "Avg. Coefficient Pts", "Games Played", "Wins", "Losses", "Draws"]
    dataframe = pd.DataFrame(final_rank, columns=col)
    dataframe.to_excel("UEFA Country Ranking 2022-23.xlsx", index=False)

##############################################################################################################

def main():
    # Toggle this value to receive additional data about teams, countries, and what dataframes are being loaded.
    test = True
    # Valid inputs for second command line argument are "Champions League", "Europa League", "Conference League", "Club", and "Country"
    if len(sys.argv) <= 2:
        print("Error: Must have at least three command line arguments.")
        return
    elif sys.argv[1] in INDEX_COMPETITION_LIST:
        competition = sys.argv[1]
    elif sys.argv[1] == "Club" or sys.argv[1] == "Country":
        competition = "All"
    else:
        print("Error: Command line argument in 'competition' position is not valid.")
        return
    # Valid inputs for third command line argument are "Load", "Save Matches", and "Save All"
    # Load must have at least three arguments, last argument being the save point.
    if sys.argv[2] == "Save All":
        current_round = "N/A"
        new_names = True
    elif sys.argv[2] == "Save Matches":
        current_round = "N/A"
        new_names = False
    elif sys.argv[2] == "Load": 
        if len(sys.argv) > 3 and any(sys.argv[3] in INDEX_COMPETITION_LIST[dict] for dict in INDEX_COMPETITION_LIST):
            current_round = sys.argv[3]
            new_names = False
        else:
            print("Error: Load argument requires valid additional argument entered afterwards.")
            return
    else:
        print("Error: Invalid entry for third command line argument.")
        return

    # Set the dataframes that we will draw data from in each ranking .py file.
    set_dataframes(current_round, new_names, test)
    # Set the countries and teams dictionaries that will be used to 
    # retrieve data about each country and team.
    set_countries(new_names)
    set_teams()
    for comp in PANDA_COMPETITION_LIST:
        dict = PANDA_COMPETITION_LIST[comp]
        set_coefficients(dict["Teams"].values)

    # Small if statement that prints out diffeent tests to see if program is working correctly
    if test:
        for team_name in TEAMS:
            team = TEAMS[team_name]
            print("Team: ", team.name, " | ", team.coefficient, " | ", team.country)
        print("#################################################################")
        print(COUNTRIES)
        check_coefficients()

    # This is where we run the actual program, calculating results for games, rounds, etc.
    if competition == "All":
        comps = PANDA_COMPETITION_LIST
    else:
        comps = {competition:PANDA_COMPETITION_LIST[competition]}
    for new_comp in comps:
        for key in comps[new_comp]:
            dataframe = comps[new_comp][key]
            if key == "Teams":
                match_type = None
            elif key in MATCH_TYPES:
                match_type = MATCH_TYPES[key]
            else:
                match_type = "double"
            comp_and_round = (new_comp, key)
            if match_type != None:
                round_calc(dataframe, match_type, comp_and_round, test)            
    if competition == "All":
        calc_all_rounds()
    else:
        calc_rounds_comp(competition)
    if test:
        print(GAMES)
        print(ROUNDS_TO_GAMES)
        print(ROUND_STATS)
    calc_competition(competition)
    if sys.argv[1] == "Country":
        final_rank = init_country_rank()
        country_rank_to_csv(final_rank)
    else:
        final_rank = init_ranking(competition)
        club_rank_to_csv(final_rank, sys.argv[1])
    return

main()

# wiki_page = pd.read_html("https://en.wikipedia.org/wiki/2022%E2%80%9323_UEFA_Champions_League")
# print(group_stage(wiki_page[17].values))

# print(PANDA_CHAMPIONS_LEAGUE["First Round"].values)
# vals = wiki_page[15]
# print("First: ", vals.values)
# dataframe = pd.DataFrame()
# for i in range(8):
#     dataframe = pd.concat([dataframe, wiki_page[15+i]], axis=1)
#     front = 16*i
#     back = 16*(i+1)
#     print(dataframe.values[:, front:back])

# print(len(dataframe.values[0])//16)

# group_stage_from_dtf(vals.values)
# for row in vals.values:
#     double_game_from_dtf(row)

