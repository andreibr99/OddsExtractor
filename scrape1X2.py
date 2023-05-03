from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_odds_by_bookmaker(url):
    # specify the path to the browser driver
    path = "C:/Users/andre/Downloads/chromedriver_win32/chromedriver.exe"

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
    
    for i in range(1, 7):
        matchpath = driver.find_element(By.XPATH, '/html/head/meta[5]')
        matchName = matchpath.get_attribute('content')

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