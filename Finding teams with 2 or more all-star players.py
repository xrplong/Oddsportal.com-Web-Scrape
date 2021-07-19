# Finding teams with 2 or more all-star players for each year and returning their regular season score and ranking

NBAteams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
            'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
            'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic',
            'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']


NBAteams_acro = ['ATL', 'BOS', 'BRK', 'CHO', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC',
                 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

NBAteams_acro2 = ['ATL', 'BOS', 'BRK', 'CHO']

from selenium import webdriver
import pandas as pd
import csv
import os

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

leadingYear = 2009
while leadingYear <= 2020:

    rows_list = []

    # Getting list of all-star players from previous two years
    all_star_year = []
    path = 'C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA All-Star Data\\NBA All-Star Players by Year'
    os.chdir(path)

    df = pd.read_csv('C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA All-Star Data\\NBA All-Star Players by Year\\NBA ' + str(leadingYear - 1) + ' All-Star Players.csv')

    for rows in df.itertuples():
        all_star_year.append(rows[1])

    df = pd.read_csv('C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA All-Star Data\\NBA All-Star Players by Year\\NBA ' + str(leadingYear - 2) + ' All-Star Players.csv')

    for rows in df.itertuples():
        all_star_year.append(rows[1])


    for team in NBAteams_acro:
        # Adjusting team acronym for past changes
        if team == 'NOP' and leadingYear <= 2013:
            team = 'NOH'

        if team == 'BRK' and leadingYear <= 2012:
            team = 'NJN'

        if team == 'CHO' and leadingYear <= 2014:
            team = 'CHA'

        # Getting website
        driver.get('https://www.basketball-reference.com/teams/' + str(team) + '/' + str(leadingYear) + '.html')

        # Getting table
        table = driver.find_element_by_xpath("//table[@id='roster']")

        team_year = []

        # Getting table data
        for row in table.find_elements_by_xpath(".//tr"):

            if str(row.get_attribute('data-row')) in ['0', '1', '2', '3', '4', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:
                name = ""
                name += str(row.text.split()[1]) + ' ' + str(row.text.split()[2])
                team_year.append(name)

        # Counting all-star players in current team-year
        all_star_count = 0

        for player in all_star_year:
            if player in team_year:
                all_star_count += 1

        # Checking if current team-year has 2 or more all-star players
        if all_star_count >= 2:

            # Getting current team-year regular season record
            driver.get('https://www.basketball-reference.com/teams/' + team + '/' + str(leadingYear) + '_games.html')
            div1 = driver.find_element_by_xpath("//div[@id='meta']")
            div2 = div1.find_element_by_xpath("//div[@data-template='Partials/Teams/Summary']")
            p1 = div2.find_element_by_xpath("//p[strong='Record:']").text
            record = str(p1).split()[1][:-1]

            print(leadingYear, team, record)

            dict = {'team':'', 'record':''}
            dict['team'] = str(team)
            dict['record'] = str(record)

            rows_list.insert(0, dict)

    path = r'C:\Users\61437\Documents\Data\NBA Data\NBA All-Star Data\NBA teams with 2 or more All-Star Players by Year'
    os.chdir(path)

    df = pd.DataFrame(rows_list)
    df.to_csv('NBA ' + str(leadingYear) + ' Teams with 2 or more All-Star Players.csv', index = False)

    leadingYear += 1

driver.quit()
