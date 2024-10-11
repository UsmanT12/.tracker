# Simple tutorial follow through on website scraping using BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from players import *
import time

path = '/Users/usmantahir/Github_Clones/chromedriver'
#url = 'https://www.wnba.com/game/1022400187/ATL-vs-LVA/boxscore'
url = 'https://www.wnba.com/game/1042400202/LVA-vs-NYL/boxscore'
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)


#Populates the box score table for the given url
def populate_box_score_table(url):
    driver.get(url)

    # Wait for the box score tables to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BoxScore_BoxScore__table__62P7f'))
    )

    # Find all box score tables
    box_score_tables = driver.find_elements(By.CLASS_NAME, 'BoxScore_BoxScore__table__62P7f')


    # Check to see which table is which with the table team titles
    team_names = driver.find_elements(By.CLASS_NAME, '_TeamName__name_dgyvp_11')
    team_names_text = [team.text for team in team_names]
    
    team1_name = team_names_text[-1]
    team2_name = team_names_text[-2]
    
    team1_table = box_score_tables[1]
    team2_table = box_score_tables[0]

    # Extract data for team 1
    print(f'{team1_name} Team Stats:')
    print_player_stats(team1_table, Team_dict[team1_name])

    # Extract data for team 2
    print(f'{team2_name} Team Stats:')
    print_player_stats(team2_table, Team_dict[team2_name])

    driver.quit()

#Extracts the team stats from the box score table
def print_player_stats(table, player_names):
    # Extract rows from the box score table
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Define the headers for the box score table
    headers = [header.text.strip() for header in rows[0].find_elements(By.TAG_NAME, 'th')]

    # Get player stats
    for player_name in player_names:
        player_stats = get_player_stats(player_name, rows, headers)
        if player_stats['MIN'] == '0':
            print(f"Player {player_name} did not play.", '\n')
        else:
            print(player_stats['PLAYER'])
            print(player_stats, '\n')

#Returns the stats of a player in a dictionary format
def get_player_stats(player_name, rows, headers):
    player_rows = [row for row in rows if player_name in row.text]
    if not player_rows:
        player_dict = {'PLAYER': player_name, 'MIN': '0', 'FGM': '0', 'FGA': '0', 'FG%': '0', '3PM': '0', '3PA': '0', '3P%': '0', 'FTM': '0', 'FTA': '0', 'FT%': '0', 'OREB': '0', 'DREB': '0', 'REB': '0', 'AST': '0', 'STL': '0', 'BLK': '0', 'TO': '0', 'PF': '0', 'PTS': '0'}
        return player_dict
    
    player_row = player_rows[0]
    player_stats = player_row.find_elements(By.TAG_NAME, 'td')
    player_dict = {headers[i]: player_stats[i].text.strip() for i in range(len(headers))}

    return player_dict

#Main function
def main():
    populate_box_score_table(url)
    
if __name__ == '__main__':
    main()