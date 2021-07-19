# redo scrap using expanded standings check table data to be consistent on years 2010-2020

from selenium import webdriver
import pandas as pd
import csv
import os

path = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

path = r'C:\Users\61437\Documents\Data\NBA Data\NBA Standings Data'
os.chdir(path)

leadingYear = 2010
while leadingYear <= 2020:
    rows_list = []

    driver.get('https://www.basketball-reference.com/leagues/NBA_' + str(leadingYear) + '_standings.html')

    id = "//table[@id='expanded_standings']"

    table = driver.find_element_by_xpath(id)


    # Getting table data
    for row in table.find_elements_by_xpath(".//tr"):
        dict = {'rank':'', 'team':'', 'win':'', 'lose':'', 'W/L%':''}

        if str(row.get_attribute('data-row')) in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']:

            for column in row.find_elements_by_xpath(".//th"):
                rank = column.text

            for column in row.find_elements_by_xpath(".//td"):
                if column.get_attribute('data-stat') == "team_name":
                    team = column.text

                if column.get_attribute('data-stat') == "Overall":
                    win = column.text.split('-')[0]
                    lose = column.text.split('-')[1]

            WL = float(int(win)/(int(win) + int(lose)))

            dict['rank'] = rank
            dict['team'] = team
            dict['win'] = win
            dict['lose'] = lose
            dict['W/L%'] = WL
            rows_list.insert(len(rows_list), dict)

    # Deleting multiples
    rows_list2 = []
    for item in rows_list:
        if rows_list.index(item) not in [15, 16]:
            rows_list2.append(item)

    df = pd.DataFrame(rows_list2)

    df.to_csv('NBA ' + str(leadingYear) + ' Standings.csv', index=False)

    leadingYear += 1

driver.quit()
