# Scraping Risk Analysis Reports from FRONTEX' website
## Imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import time
import clipboard


## Scraping

#specify folder where downloads should be stored
download_directory = '/Users/emilykruger/Documents/GitHub/frontex_analysis/data/risk analysis reports'
prefs = {
    'download.default_directory': download_directory,
    'download.directory_upgrade': True,
    'download.prompt_for_download': False,
}
#set driver options
chrome_options = Options()
chrome_options.add_argument('--headless') #enable for headless mode
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
#define function that downloads all files
def get_files():
    boxes = driver.find_elements(By.CSS_SELECTOR, 'a.card-wrap.js-lightbox')
    global counter
    for box in boxes:
        #open overlay box and switch navigation to it
        box.click()
        iframe = WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="lightbox"]/div/iframe'))
            )
        #wait three seconds to make sure that download button is ready to be interacted with
        time.sleep(3)
        try: #try downloading file
            driver.find_element(By.CSS_SELECTOR, 'i.icon-download').click()
            print('Download successful')
            counter+=1
            time.sleep(2)
            #close overlay box
            driver.switch_to.default_content()
            driver.find_element(By.CSS_SELECTOR, 'i.close.close-lightbox.icon-close').click()
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException): #if download fails, try to store link to web address of doc to list
            print('Download failed')
            try: 
                driver.find_element(By.CSS_SELECTOR, 'a.copy-button.button').click()
                copied_link = clipboard.paste()
                failed_downloads.append(copied_link)
                #close overlay box
                driver.switch_to.default_content()
                driver.find_element(By.CSS_SELECTOR, 'i.close.close-lightbox.icon-close').click()
            except NoSuchElementException: # if that fails, get name of doc
                #close overlay box
                driver.switch_to.default_content()
                driver.find_element(By.CSS_SELECTOR, 'i.close.close-lightbox.icon-close').click()
                #get title of doc
                title = box.find_element(By.CLASS_NAME, 'card-title').text
                failed_downloads.append(title)



#download all files form all pages
while True:
    get_files()
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