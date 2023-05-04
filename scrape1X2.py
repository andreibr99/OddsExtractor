from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List

import time

path = "C:\DRIVERS\ChromeDriver\chromedriver.exe"

def get_odds_by_bookmaker(url, odds_betfair):
    # specify the path to the browser driver
    

    # create a service for the Chrome driver
    service = Service(path)
    service.start()

    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # options.add_argument('--blink-settings=imagesEnabled=false')

    # create an instance of the Chrome browser
    driver = webdriver.Chrome(service=service)

    driver.delete_all_cookies()

    # access the web page
    max_attempts = 3  # numărul maxim de încercări
    wait_time = 4  # timpul maxim de așteptare în secunde

    for i in range(max_attempts):
        try:
            driver.get(url)
            WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, '/html/head/meta[5]')))
            time.sleep(1)
            break  # iese din bucla dacă pagina s-a încărcat cu succes
        except:
            if i == max_attempts - 1:
                raise Exception("Pagina nu s-a încărcat nici după {} încercări".format(max_attempts))
            driver.refresh()

    
    

    bookmakers = {}  # empty dictionary to store odds by bookmaker
    max_odds = {'1': {'bookmaker': '', 'odd': 0}, 'X': {'bookmaker': '', 'odd': 0}, '2': {'bookmaker': '', 'odd': 0}}

    matchpath = driver.find_element(By.XPATH, '/html/head/meta[5]')
    matchName = matchpath.get_attribute('content')
    
    for j in range(len(odds_betfair)):
        if(matchName.split(" - ")[0][0:3] == odds_betfair[j].team1[0:3] and matchName.split(" - ")[0][-3:] == odds_betfair[j].team1[-3:] ):
            bookmakers["Betfair"] = []
            bookmakers["Betfair"].append(odds_betfair[j].one + "\n" + odds_betfair[j].draw + "\n" + odds_betfair[j].two)
            betfair_odds = odds_betfair[j].one + "\n" + odds_betfair[j].draw + "\n" + odds_betfair[j].two
            break

    try:
        odds = betfair_odds.split('\n')
        if float(odds[0]) > max_odds['1']['odd']:
            max_odds['1']['odd'] = float(odds[0])
            max_odds['1']['bookmaker'] = "Betfair"
        if float(odds[1]) > max_odds['X']['odd']:
            max_odds['X']['odd'] = float(odds[1])
            max_odds['X']['bookmaker'] = "Betfair"
        if float(odds[2]) > max_odds['2']['odd']:
            max_odds['2']['odd'] = float(odds[2])
            max_odds['2']['bookmaker'] = "Betfair"
    except:
        x = 1

    for i in range(1, 7):
        
       
        # find the bookmaker name
        title_path = f'/html/body/div[1]/div/div[8]/div[3]/div/div[2]/div[{i}]/div/div/a/img'
        title_elements = driver.find_elements(By.XPATH, title_path)
        if title_elements:
            title = title_elements[0].get_attribute('title')
        else:
            title_path = f'/html/body/div[1]/div/div[7]/div[3]/div/div[2]/div[{i}]/div/div/a/img'
            title_elements = driver.find_elements(By.XPATH, title_path)
            if title_elements:
                title = title_elements[0].get_attribute('title')
            else:
                title = None

        # find the odd
        odd_path = f'/html/body/div[1]/div/div[8]/div[3]/div/div[2]/div[{i}]'
        odd_elements = driver.find_elements(By.XPATH, odd_path)
        if odd_elements:
            odd_value = odd_elements[0].text
        else:
            odd_path = f'/html/body/div[1]/div/div[7]/div[3]/div/div[2]/div[{i}]'
            odd_elements = driver.find_elements(By.XPATH, odd_path)
            if odd_elements:
                odd_value = odd_elements[0].text
            else:
                odd_value = None

        # add the odd to the dictionary
        if title and odd_value:
            if title not in bookmakers:
                bookmakers[title] = []
            bookmakers[title].append(odd_value)

            # update max odds dictionary
            odds = odd_value.split('\n')
            if float(odds[0]) > max_odds['1']['odd']:
                max_odds['1']['odd'] = float(odds[0])
                max_odds['1']['bookmaker'] = title
            if float(odds[1]) > max_odds['X']['odd']:
                max_odds['X']['odd'] = float(odds[1])
                max_odds['X']['bookmaker'] = title
            if float(odds[2]) > max_odds['2']['odd']:
                max_odds['2']['odd'] = float(odds[2])
                max_odds['2']['bookmaker'] = title

    # close the browser
    driver.quit()

    # return the odds organized by bookmaker as a list of dictionaries including the match name
    if bookmakers:
        return [{'match_name': matchName, 'bookmaker': k, 'odds': v} for k, v in bookmakers.items()], max_odds
    else:
        return [], max_odds
    



def get_odds_from_betfair_page():

    service = Service(path)
    service.start()
    driver = webdriver.Chrome(service=service)

    driver.delete_all_cookies()

    url = "https://www.betfair.ro/exchange/plus/ro/fotbal-pariuri-1"
    driver.get(url)
    program_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ui-view/div/div/div[2]/div/ui-view/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[1]/header/nav/ours-button[3]/a")))

    # se face clic pe elementul de fila "Program"
    program_tab.click()
    time.sleep(2)
    
    pages =len(driver.find_elements(By.CLASS_NAME, "coupon-page-navigation__bullet"))
    leagues = len(driver.find_elements(By.CLASS_NAME,"coupon-card"))
    
    ##How to get the nuber of tr in that tbody??????

    xpath = f'/html/body/ui-view/div/div/div[2]/div/ui-view/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[1]/div[2]/bf-coupon-table/div/table/tbody/tr[1]'
    betfair_matches: List[BetfairMatch] = []
    for i in range(1, leagues+1):
        xpath = f'/html/body/ui-view/div/div/div[2]/div/ui-view/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{i}]/div[2]/bf-coupon-table/div/table/tbody/tr[1]'
        for j in range (1, 5+1):
            try:
                rows = driver.find_elements(By.XPATH, xpath)
                split = rows[0].text.split("\n")
                if(split[0][-1] != "'" and split[0]!= "SFÂRŞIT" and split[0] != "PAUZĂ" and split[0].split(" ")[0] != "Începe"):
                    new_match = BetfairMatch(split[0], split[1], split[2], split[3], split[7], split[11])
                    betfair_matches.append(new_match)
                
                    xpath = f'/html/body/ui-view/div/div/div[2]/div/ui-view/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{i}]/div[2]/bf-coupon-table/div/table/tbody/tr[{j+1}]'
                elif(split[0][-1] == "'" and split[0].split(" ")[0] != "Începe"):
                    leagues = leagues + 1
                    j = 1
                    xpath = f'/html/body/ui-view/div/div/div[2]/div/ui-view/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{i}]/div[2]/bf-coupon-table[2]/div/table/tbody/tr[{j}]'
                else:
                    xpath = f'/html/body/ui-view/div/div/div[2]/div/ui-view/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{i}]/div[2]/bf-coupon-table/div/table/tbody/tr[{j+1}]'
            except:
                continue
                  

    driver.quit()
    return betfair_matches


class BetfairMatch:
    def __init__(self, date: str, team1: str, team2: str, one: float, draw: float, two: float):
        self.date = date
        self.team1 = team1
        self.team2 = team2
        self.one = one
        self.draw = draw
        self.two = two

