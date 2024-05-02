## scraping functions
## Imports

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import time
import clipboard

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