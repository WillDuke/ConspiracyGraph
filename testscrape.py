import json
import re
from time import sleep
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the URL's we will open and a few other variables 
main_url = 'https://www.linkedin.com' # URL A
tab_url = 'https://www.google.com' # URL B
chromedriver = '/Users/Will/chromedriver'
# Open main window with URL A
browser= webdriver.Chrome(chromedriver)
browser.get(main_url)
print("Current Page Title is : %s" %browser.title)
# Open a new window

def get_next_video(next_video, driver):

    driver.execute_script("window.open('');")

    # Switch to the new window and open URL B
    driver.switch_to.window(browser.window_handles[1])
    driver.get(next_video)

    # Switch back to URL A and close
    browser.switch_to.window(browser.window_handles[0])
    browser.close()
    # Make sure we switched back to URL B
    browser.switch_to.window(browser.window_handles[0])

    print(f'Loaded {next_video} in new tab.')