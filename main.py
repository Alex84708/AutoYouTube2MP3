from bs4 import BeautifulSoup as soup
import sys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from urllib.request import urlopen as uReq
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Hardcoded link
youtubePlaylistURL = 'https://www.youtube.com/playlist?list=PLVTio_ldhYuhEhaQLoG5FHONllZd-Acws'

# Update if playlist provided
if len(sys.argv) >= 2:
    youtubePlaylistURL = sys.argv[1]

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(youtubePlaylistURL)

bs = soup(browser.page_source, "html.parser")

allVideoTags = bs.find_all(id="video-title")
allVideoLinks = []

for tag in allVideoTags:
    print("https://www.youtube.com" + tag.get("href"))
    allVideoLinks.append("https://www.youtube.com" + tag.get("href"))

youtubeToMp3URL = "https://mp3-convert.org/"

for videoLink in allVideoLinks:
    browser.get(youtubeToMp3URL)

    # find link field and enter url
    linkField = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/form/input')))
    linkField.send_keys(videoLink + "\n")

    # click download
    time.sleep(3)
    browser.find_element_by_id("download_url").click()
    
    # Close all but first tab
    firstTime = True
    for handle in browser.window_handles:
        browser.switch_to.window(handle)
        if not firstTime:
            browser.close()
        firstTime = False

    # Switch back to first tab
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(2)

# Give some time for downloads to finish
time.sleep(15)