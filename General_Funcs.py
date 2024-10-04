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


    #TODO: Check to see which table is which with the table team titles
    team_names = driver.find_elements(By.CLASS_NAME, '_TeamName__name_dgyvp_11')
    team_names_text = [team.text for team in team_names]
    team1_name = team_names_text[-1]
    team2_name = team_names_text[-2]
    
    #TODO: Use the arrays from players.py to extract the player stats for the right team


    team1_table = box_score_tables[1]
    team2_table = box_score_tables[0]

    # Extract data for LVA
    print(f'{team1_name} Team Stats:')
    extract_team_stats(team1_table, Team_dict[team1_name])

    # Extract data for ATL
    print(f'{team2_name} Team Stats:')
    extract_team_stats(team2_table, Team_dict[team2_name])

    driver.quit()

#Extracts the team stats from the box score table
def extract_team_stats(table, player_names):
    # Extract rows from the box score table
    rows = table.find_elements(By.TAG_NAME, 'tr')

    # Define the headers for the box score table
    headers = [header.text.strip() for header in rows[0].find_elements(By.TAG_NAME, 'th')]

    # Get player stats
    for player_name in player_names:
        player_stats = get_player_stats(player_name, rows, headers)
        print(player_stats, '\n')

#Returns the stats of a player in a dictionary format
def get_player_stats(player_name, rows, headers):
    player_rows = [row for row in rows if player_name in row.text]
    if not player_rows:
        return f"Player {player_name} did not play."
    
    player_row = player_rows[0]
    player_stats = player_row.find_elements(By.TAG_NAME, 'td')
    player_dict = {headers[i]: player_stats[i].text.strip() for i in range(len(headers))}

    return player_dict

populate_box_score_table(url)