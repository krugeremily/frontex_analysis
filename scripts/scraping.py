# Scraping Risk Analysis Reports from FRONTEX' website
## Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
from webutils.scraping_utils import get_files
## Scraping

#specify folder where downloads should be stored
download_directory = '/Users/emilykruger/Documents/GitHub/frontex_analysis/data/raw_data'
prefs = {
    'download.default_directory': download_directory,
    'download.directory_upgrade': True,
    'download.prompt_for_download': False,
}
#set driver options
chrome_options = Options()
#chrome_options.add_argument('--headless') #enable for headless mode
chrome_options.add_experimental_option("prefs", prefs)
#setting up driver
driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
# Create an instance of ActionChains
action = ActionChains(driver)


### Navigating Page
#access frontex' public register of documents
driver.get('https://prd.frontex.europa.eu')
#open advanced seach options
driver.find_element(By.CSS_SELECTOR, 'div.description.content').click()
#select category = risk analysis reports & document language = english
search_elements = driver.find_elements(By.CSS_SELECTOR, 'span.select2.select2-container.select2-container--default')
#expand languages drop down and select 'EN'
search_elements[0].click()
driver.find_element(By.XPATH, '//label[text()="EN"]').click()
#expand document category drop down and select risk analysis reports
search_elements[1].click()
driver.find_element(By.XPATH, '//label[text()="Risk analysis"]').click()
#hit search
driver.find_element(By.CSS_SELECTOR, 'i.icon-search').click()


## Downloading documents
failed_downloads = []
counter = 0

#download all files form all pages
while True:
    counter = get_files(driver=driver, counter=counter, failed_downloads=failed_downloads)
    #check for next-page button
    print('Page done.')
    try: #try to click next-page button and give page time to load
        driver.find_element(By.CSS_SELECTOR, 'i.icon-arrow-right').click()   
        time.sleep(3)
    except NoSuchElementException:
        break

driver.close()

#print number of successful and unsuccessful downloads
print(f'{len(failed_downloads)} failed downloads\n{counter} successful downloads.\nFailed Downloads: {failed_downloads}')

#Failed Downloads will be downloaded manually by accessing the link to the webpage stored in the list