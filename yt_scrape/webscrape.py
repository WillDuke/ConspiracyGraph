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

RAW_RELATED_IDS = './data/related_ids.json'
SOURCE_IDS_PATH = './data/valid_ids.txt'
CACHE = './data/cache.txt'

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
    
    while True:
        try:
            driver.get(url)
            break
        except:
            sleep(0.5)

    # bypass offer for youtube premium
    try:
        element = WebDriverWait(driver, 7).until(
            presence((By.XPATH, button_xpath))
        )
        element.click()
    except:
        pass

    # wait until the related lists show up
    wait.until(visible((By.ID, "related")))
    
    # scroll down to the bottom so that all of the related videos load
    for i in range(10):
        sleep(0.2)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    
    # note: above breaks headless mode, and below didn't work as well

    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     scroll_height = 500
    #     document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
    #     driver.execute_script(f"window.scrollTo(0, {document_height_before + scroll_height});")
    #     sleep(1)
    #     document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
    #     if document_height_after == document_height_before:
    #         break

    # titles = recommended.find_elements_by_id("video-title")
    
    # get all of the links on the page (hacky I know)
    elems = driver.find_elements_by_xpath("//a[@href]")

    all_links = [elem.get_attribute("href") for elem in elems]

    # select only pure links to other videos
    pattern = re.compile("https://www.youtube.com/watch\?v=\w+$")
    related_links = list(set([link for link in all_links 
                        if bool(re.search(pattern, link))]))

    related_ids = [link.split("=")[1] for link in related_links]

    with open(CACHE, 'a+') as f:
        f.write(f"{video_id}: {related_ids}\n")

    print(f'Found {len(related_ids)} related videos for {video_id}.')

    return related_ids

def get_new_tab(driver):
    """Open new tab and close old one."""
    # open second tab
    driver.execute_script("window.open('');")

    # switch to second tab and open url
    driver.switch_to.window(driver.window_handles[1])

    # switch back to first tab and close
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    # Make sure we switched back to URL B
    driver.switch_to.window(driver.window_handles[0])
    sleep(1)

def get_all_related(video_ids, driver):
    """Get all of the related ids, dumping to a json cache if there is an API error."""

    for id in tqdm(video_ids):
        # get related video ids
        get_new_tab(driver)

        try:
            get_related_ids(id, driver)
        except:
            print(f'Failed to get related videos for {id}')
            continue

    driver.quit()

if __name__ == "__main__":

   # load video_ids
    with open(SOURCE_IDS_PATH, 'r') as file:
        ids = file.readlines()[0].split(', ')
    
    with open(RAW_RELATED_IDS) as f:
        already_complete = json.load(f)

    # exclude the ones already complete from first tests
    ids = [id for id in ids if id not in already_complete.keys()]
    
    driver = init_webdriver()

    all_related = get_all_related(ids, driver)