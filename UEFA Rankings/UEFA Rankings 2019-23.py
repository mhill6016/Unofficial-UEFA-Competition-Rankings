from tkinter import ROUND
import pandas as pd
import math
import sys

from dataclasses import dataclass

#Struct used to define key statistics for teams and countries in (a) given UEFA competition(s)
@dataclass
class Competition:
    record : list
    games : int
    points : float

    def record(self) -> list:
        return self.record

    def games(self) -> list:
        return self.games

    def points(self) -> float:
        return self.points

#Struct used to define UEFA Teams
@dataclass
class Team:
    name : str
    country: str
    total_points : Competition
    #badge : str

    def name(self) -> str:
        return self.name

    def country(self) -> list:
        return self.country

    def total_points(self) -> Competition:
        return self.total_points

# Used as a function which initializes the starting stats of a team for a competition.
def init_competition():
    return (Competition([0, 0, 0], 0, 0))

##############################################################################################################
# Marks where begining of club ranking is in excel spreadsheets from previous years
YEAR_TO_COL = {19:64, 20:63, 21:85}


#Dictionary of UEFA Countries and teams for easy access
COUNTRIES = {}
TEAMS = {}


CLUB_RANKING_DF = [0 for j in range(4)]
COUNTRY_RANKING_DF = [0 for l in range(4)]

def init_club_dataframes(start_year, end_year):
    link_help = ['Club', 'Country']
    for i in range(start_year, end_year):
        if i in YEAR_TO_COL:
            link = '20'+str(i)+'-'+str(i+1)+'/UEFA Rankings 20'+str(i)+'-'+str(i+1)+'.xlsx'
            CLUB_RANKING_DF[i-19] = pd.read_excel(link, sheet_name="Overall Rankings").iloc[:,YEAR_TO_COL[i]:]
            COUNTRY_RANKING_DF[i-19] = pd.read_excel(link, sheet_name="Country Rankings").iloc[:55,0:5]
            # print(len(COUNTRY_RANKING_DF[i-19].values[0]))
        else:
            links = ['', '']
            for j in range(2):
                links[j] = '20'+str(i)+'-'+str(i+1)+'/UEFA ' + link_help[j] + ' Ranking 20'+str(i)+'-'+str(i+1)+'.csv'
            CLUB_RANKING_DF[i-19] = pd.read_csv(links[0])
            COUNTRY_RANKING_DF[i-19] = pd.read_csv(links[1])
            # print(len(COUNTRY_RANKING_DF[i-19].values[0]))

def set_teams():
    for index in range(len(CLUB_RANKING_DF)):
        rank = CLUB_RANKING_DF[index].values
        for i in range(len(rank)):
            country = rank[i][7]
            if country != "Country":
                team = rank[i][1]

                # Finds all of the teams to play for the UEFA country from its league
                if country not in COUNTRIES:
                    COUNTRIES[country] = []
                if team not in COUNTRIES[country]:
                    COUNTRIES[country].append(team)

                # Accumulate the stats for each team every year in TEAMS dictionary
                comp_stats = init_competition()
                # Compute points, games played, and record (if available)
                comp_stats.points = rank[i][2]
                comp_stats.games = rank[i][3]
                if not (math.isnan(float(rank[i][4])) or math.isnan(float(rank[i][5])) or math.isnan(float(rank[i][6]))):
                    for k in range(3):
                        comp_stats.record[k] = rank[i][k+4]

                if team not in TEAMS:
                    TEAMS[team] = [Team(team, country, init_competition()), [0 for j in range(4)]]
                    
                TEAMS[team][1][index] = comp_stats

def calculate_points():
    for team_name in TEAMS:
        team = TEAMS[team_name]
        team_stats = team[0].total_points
        for index in range(len(team[1])):
            if team[1][index] != 0:
                season_stats = team[1][index]
                for ind in range(len(team_stats.record)):
                    team_stats.record[ind] += season_stats.record[ind]
                team_stats.games += season_stats.games
                team_stats.points += (season_stats.points*(.3-.05*(3-index)))
        team_stats.points = team_stats.points*(10/9)


def init_club_ranking():
    team_stats = [[] for i in range(len(TEAMS))]
    ind = 0
    for team_name in TEAMS:
        # initialize array holding important information for each team
        row = [0 for j in range(8)]
        team = TEAMS[team_name]
        row[1] = team_name
        row[7] = team[0].country

        total_stats = team[0].total_points

        # Updates total record
        for index in range(len(total_stats.record)):
            row[4+index] += total_stats.record[index]

        row[2] = total_stats.points
        row[3] = total_stats.games
        team_stats[ind] = row
        ind += 1

    final_rank = sorted(team_stats, key=lambda stats: stats[2], reverse=True)
    ind = 1
    for new_team in final_rank:
        new_team[0] = ind
        ind += 1
    return final_rank
    
def init_country_rank():
    country_rank_dict = {}

    # First adds information based on Country ranking information
    for index in range(len(COUNTRY_RANKING_DF)):
        year_df = COUNTRY_RANKING_DF[index]
        for row in year_df.values:
            # Sets array and country in array, initializes number of teams to 0
            if row[1] not in country_rank_dict:
                country_rank_dict[row[1]] = [0 for i in range(8)]
                country_rank_dict[row[1]][1] = row[1]
                country_rank_dict[row[1]][2] = 0
            country_stats = country_rank_dict[row[1]]
            # Calculates average coefficient points
            country_stats[3] += row[4]*(.3-.05*(3-index))
            #Calculates games played, for new seasons
            if len(row) != 5:
                for ind in range(4, 8):
                    country_stats[ind] += row[ind+1]
    
    # Then uses club ranking information to add more crucial details.
    club_rank = init_club_ranking()
    for club_row in club_rank:
        country = club_row[7]
        country_stats = country_rank_dict[country]
        country_stats[2] += 1
        country_stats[4] += club_row[3]
    
    country_rank = [[] for j in range(len(country_rank_dict))]
    index = 0
    for country in country_rank_dict:
        new_row = country_rank_dict[country]
        country_rank[index] = new_row
        index += 1
    
    final_rank = sorted(country_rank, key=lambda stats: stats[3], reverse=True)

    index = 1
    for new_country in final_rank:
        new_country[0] = index
        new_country[3] *= (10/9)
        index += 1
    return final_rank

def club_rank_to_csv(final_rank):
    col = ["Rank", "Team", "Points", "Games Played", "Wins", "Losses", "Draws", "Country"]
    dataframe = pd.DataFrame(final_rank, columns=col)
    dataframe.to_excel("UEFA Club Ranking 2019-23.xlsx", index=False)

def country_rank_to_csv(final_rank):
    col = ["Rank", "Country", "# of Teams", "Overall Points", "Games Played", "Wins", "Losses", "Draws"]
    # print(final_rank)
    dataframe = pd.DataFrame(final_rank, columns=col)
    dataframe.to_excel("UEFA Country Ranking 2019-23.xlsx", index=False)

##############################################################################################################

def main():
    if len(sys.argv) != 2:
        print("Error: Must have two command line arguments.")
        return
    elif sys.argv[1] == "Club":
        init_club_dataframes(19, 23)
        set_teams()
        calculate_points()
        final_rank = init_club_ranking()
        club_rank_to_csv(final_rank)
    elif sys.argv[1] == "Country":
        init_club_dataframes(19, 23)
        set_teams()
        calculate_points()
        final_rank = init_country_rank()
        country_rank_to_csv(final_rank)
    else:
        print("Error: Invalid command line argument.")
    return

main()

# print(COUNTRIES)
# for team in TEAMS:
#     print(TEAMS[team][0])
# print(len(TEAMS))
