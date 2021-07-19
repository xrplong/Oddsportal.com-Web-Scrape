NBAteams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
            'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
            'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks', 'Oklahoma City Thunder', 'Orlando Magic',
            'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards']

from selenium import webdriver
import time
import pandas as pd
import csv
import os

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

path = 'C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA Regular Season Data'
os.chdir(path)


page = 1
max_page = 9999
rows_list = []

preYear = 2008       # Change year season here
leadingYear = 2009

while page <= max_page:
    driver.get('https://www.oddsportal.com/basketball/usa/nba-2008-2009/results/#/page/' + str(page) + '/') # Change url here!!!
    time.sleep(3)

    # Finding max page
    if max_page == 9999:
        pagination = driver.find_element_by_xpath("//div[@id='pagination']")
        pagi_list = []
        for num in pagination.find_elements_by_xpath(".//a"):
            pagi_list.append((num.get_attribute('href'))[-3:-1])
        max_page = int(pagi_list[-1])

    table = driver.find_element_by_xpath("//table[@id='tournamentTable']")

    # Looping through each table row in tournament table for current page
    for row in table.find_elements_by_xpath(".//tr"):
        dict = {'date':'', 'team 1':'', 'team 2':'', 'team 1 score':'', 'team 2 score':'', 'team 1 win':'', 'team 2 win':''}

        # Finding date of current game
        if row.get_attribute('class') == 'center nob-border':
            date = row.text
            print(date)

        # Finding current game teams
        if row.get_attribute('class') in [' deactivate', 'odd deactivate']:
            teams = [td.text for td in row.find_elements_by_xpath(".//td[@class='name table-participant']")]
            if teams != []:
                teams_ = (str(teams))[2:-2]

            dict['team 1'] = teams_.split(' - ')[0]

            if len(teams_.split(' - ')) != 2:
                continue

            if  teams_.split(' - ')[1][-2:] == 'n ':
                dict['team 2'] = teams_.split(' - ')[1][:-3]
            else:
                dict['team 2'] = teams_.split(' - ')[1]

            # Finding current game score
            score = [td.text for td in row.find_elements_by_xpath(".//td[@class='center bold table-odds table-score']")]
            if score != []:
                if len(str(score)[2:-2].split(':')) != 2:
                     continue
                if str(score)[-4:-2] == 'OT':
                    score1 = str(score).split(' ')[0] + "']"
                    score = score1
                dict['team 1 score'] = (str(score)[2:-2].split(':'))[0]
                dict['team 2 score'] = (str(score)[2:-2].split(':'))[1]

            # Finding current game $odds
            payoff_loser = [td.text for td in row.find_elements_by_xpath(".//td[@class='odds-nowrp']")]
            payoff_winner = [td.text for td in row.find_elements_by_xpath(".//td[@class='result-ok odds-nowrp']")]
            if (payoff_loser != []) and (payoff_winner != []):
                payoff_left = str(payoff_winner)[2:6]
                payoff_right = str(payoff_loser)[2:6]

                if int((str(score)[2:-2].split(':'))[0]) > int((str(score)[2:-2].split(':'))[-1]):
                    dict['team 1 win'] = payoff_left
                    dict['team 2 win'] = payoff_right
                else:
                    dict['team 1 win'] = payoff_right
                    dict['team 2 win'] = payoff_left
            dict['date'] = (str(date))[0:11]

            # Skipping games not in regular season
            if len(str(date)) != 19:
                continue

            # Appending current game stats to row_list
            rows_list.insert(0, dict)

    page += 1

path = 'C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA Regular Season Data\\NBA Regular Season ' + str(preYear) + '-' + str(leadingYear)
os.mkdir(path)
os.chdir(path)

# Data into dataframe
df = pd.DataFrame(rows_list)

# Creating csv of data
df.to_csv('NBA ' + str(preYear) + '-' + str(leadingYear) + ' Regular Season results&odds.csv', index=False)

# Creating team/year data for current year
df = pd.read_csv('NBA ' + str(preYear) + '-' + str(leadingYear) + ' Regular Season results&odds.csv')
for team in NBAteams:

    with open('NBA ' + str(preYear) + "-" + str(leadingYear) + ' regular season - ' + team + '.csv', 'w') as new_file:

        csv_writer = csv.writer(new_file, delimiter = ',')
        csv_writer.writerow(['date', 'team 1', 'team 2', 'team 1 score', 'team 2 score', 'team 1 win', 'team 2 win'])
        # Note: row[1] = date, row[2] = team 1, row[3] = team 2, row[4] = team 1 score, row[5] = team 2 score,
        #       row[6] = team 1 win, row[7] = team 2 win
        for row in df.itertuples():
            if row[2] == team:
                csv_writer.writerow(row[1:])
            if row[3] == team:
                # Adjusting row to ensure file team game data always on LHS
                date = row[1]
                team1 = row[3]
                team2 = row[2]
                team1score = row[5]
                team2score = row[4]
                team1win = row[7]
                team2win = row[6]
                csv_writer.writerow([date, team1, team2, team1score, team2score, team1win, team2win])

os.remove('NBA ' + str(preYear) + '-' + str(leadingYear) + ' Regular Season results&odds.csv')

driver.quit()

# Deleting data with missing values

path = 'C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA Regular Season Data\\NBA Regular Season ' + str(preYear) + '-' + str(leadingYear)
os.chdir(path)

for team in NBAteams:
    df = pd.read_csv('C:\\Users\\61437\\Documents\\Data\\NBA Data\\NBA Regular Season Data\\NBA Regular Season ' + str(preYear) + '-' + str(leadingYear) + '\\NBA ' + str(preYear) + "-" + str(leadingYear) + ' regular season - ' + team + '.csv')
    for row in df.itertuples():
        if str(row[6]) == 'nan' or str(row[7]) == 'nan': # Checking is data is missing
            os.remove('NBA ' + str(preYear) + "-" + str(leadingYear) + ' regular season - ' + team + '.csv') # Removing team-year data
            break
