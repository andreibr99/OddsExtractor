from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_ids(num_ids: int) -> List[str]:
   # specify the path to the browser driver
    path = "C:/Users/andre/Downloads/chromedriver_win32/chromedriver.exe"

    # create a service for the Chrome driver
    service = Service(path)
    service.start()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--blink-settings=imagesEnabled=false')

    # create an instance of the Chrome browser
    driver = webdriver.Chrome(service=service)
    driver.delete_all_cookies()
    
    # access the web page
    url = "https://www.flashscore.ro/"
    driver.get(url)

    # se asteapta ca elementul de fila "Program" sa devina vizibil si sa poata fi accesat
    program_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[1]/div/div/main/div[4]/div[2]/div/div[1]/div[1]/div[5]")))

    # se face clic pe elementul de fila "Program"
    program_tab.click()

    # wait for the element with the odd to load
    wait = WebDriverWait(driver, 15)

    ids = []
    
    i = 1
    while len(ids) < num_ids:
        path = f'/html/body/div[3]/div[1]/div/div/main/div[4]/div[2]/div/section/div/div/div[{i}]'
        element = wait.until(EC.presence_of_element_located((By.XPATH, path)))
        link = element.get_attribute('id')
        if link:
            link = link.replace('g_1_', '')
            ids.append(link)
        i += 1

    # close the browser
    driver.quit()

    return ids

def generate_links(ids):
    base_url = "https://www.flashscore.ro/meci/{}/#/comparare-cote/cote-1x2/final"
    links = []
    for id in ids:
        link = base_url.format(id)
        links.append(link)
        #print(link)
    return links
