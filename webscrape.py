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

RAW_RELATED_IDS = 'data/related_ids.json'
SOURCE_IDS_PATH = 'data/valid_ids.txt'
CACHE = {}

def init_webdriver(PATH = '/Users/Will/chromedriver'):
    options = Options()
    # options.headless=True
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome(PATH, options = options)
    
    return driver
    
def get_related_ids(video_id, driver):

    wait = WebDriverWait(driver, 10)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located

    button_xpath = "//ytd-mealbar-promo-renderer/div/div[2]/ytd-button-renderer/a/paper-button/yt-formatted-string"

    url = "https://www.youtube.com/watch?v=" + video_id
    
    driver.get(url)

    # bypass offer for youtube premium
    try:
        element = wait.until(
            presence((By.XPATH, button_xpath))
        )
        element.click()
        # driver.find_element_by_xpath(button_xpath).click()
    except:
        pass

    # wait until the related lists show up
    wait.until(visible((By.ID, "related")))
    
    # scroll down to the bottom so that all of the related videos load
    for i in range(10):
        sleep(0.2)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)

    # titles = recommended.find_elements_by_id("video-title")
    
    # get all of the links on the page (hacky I know)
    elems = driver.find_elements_by_xpath("//a[@href]")

    all_links = [elem.get_attribute("href") for elem in elems]

    # select only pure links to other videos
    pattern = re.compile("https://www.youtube.com/watch\?v=\w+$")
    related_links = list(set([link for link in all_links 
                        if bool(re.search(pattern, link))]))

    related_ids = [link.split("=")[1] for link in related_links]

    return related_ids

def get_all_related(video_ids):
    """Get all of the related ids, dumping to a json cache if there is an API error."""
    global CACHE

    for id in tqdm(video_ids):
        # get related video ids
        sleep(2)
        try:
            driver = init_webdriver()
            related_ids = get_related_ids(id, driver)
            driver.quit()
            CACHE[id] = related_ids
        except:
            print(f'Failed to get related videos for {id}')
            continue
        finally:
            driver.quit()
    return CACHE

if __name__ == "__main__":

   # load video_ids
    with open(SOURCE_IDS_PATH, 'r') as file:
        ids = file.readlines()[0].split(', ')
    
    try:
        all_related = get_all_related(ids)
    except:
        with open(RAW_RELATED_IDS, 'w') as file:
            json.dump(CACHE, file) 
