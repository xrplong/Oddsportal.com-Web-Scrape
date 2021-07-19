NBAteams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
            'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
            'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic',
            'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']


NBAteams_acro = ['ATL', 'BOS', 'BRK', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC',
                 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

from selenium import webdriver
import pandas as pd
import csv
import os

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

path = 'C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA All-Star Data'
os.chdir(path)

leadingYear = 2007
while leadingYear <= 2007:
    rows_list = []

    driver.get('https://www.basketball-reference.com/allstar/NBA_' + str(leadingYear) + '.html')

    id1 = "//table[@id='West']"
    id2 = "//table[@id='East']"

    if leadingYear == 2018:
        id1 = "//table[@id='LeBron']"
        id2 = "//table[@id='Stephen']"

    if leadingYear == 2019:
        id1 = "//table[@id='LeBron']"
        id2 = "//table[@id='Giannis']"

    if leadingYear == 2020:
        id1 = "//table[@id='LeBron']"
        id2 = "//table[@id='Giannis']"

    tableWest = driver.find_element_by_xpath(id1)
    tableEast = driver.find_element_by_xpath(id2)

    # Getting West table data
    for row in tableWest.find_elements_by_xpath(".//tr"):
        dict = {'player':'', 'team':''}

        if str(row.get_attribute('data-row')) in ['0', '1', '2', '3', '4', '7', '8', '9', '10', '11', '12', '13']:

            player = str(row.text.split()[0]) + ' ' + str(row.text.split()[1])
            team = str(row.text.split()[2])

            if str(row.text.split()[2]) == 'NOH':
                team = 'NOP'

            if str(row.text.split()[2]) in ['NJN', 'BRK', 'BKN']:
                team = 'BRK'

            if str(row.text.split()[2]) == 'CHO':
                team = 'CHA'

            dict['player'] = player
            dict['team'] = team
            rows_list.insert(0, dict)

    # Getting East table data
    for row in tableEast.find_elements_by_xpath(".//tr"):
        dict = {'player':'', 'team':''}

        if str(row.get_attribute('data-row')) in ['0', '1', '2', '3', '4', '7', '8', '9', '10', '11', '12', '13']:

            player = str(row.text.split()[0]) + ' ' + str(row.text.split()[1])
            team = str(row.text.split()[2])

            if str(row.text.split()[2]) == 'NOH':
                team = 'NOP'

            if str(row.text.split()[2]) in ['NJN', 'BRK', 'BKN']:
                team = 'BRK'

            if str(row.text.split()[2]) == 'CHO':
                team = 'CHA'

            dict['player'] = player
            dict['team'] = team
            rows_list.insert(0, dict)

    df = pd.DataFrame(rows_list)

    df.to_csv('NBA ' + str(leadingYear) + ' All-Star Players.csv', index=False)

    leadingYear += 1

driver.quit()
