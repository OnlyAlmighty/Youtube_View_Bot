from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--mute-audio")
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-extensions")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-web-security")
options.add_argument("--disable-features=site-per-process")
options.add_argument("--no-sandbox")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

PROXY_FILE_PATH = 'D:\Application\proxy.txt'

# Read the proxies from the text file
with open(PROXY_FILE_PATH, 'r') as f:
    proxies = [line.strip() for line in f]

link = input("Enter the Video link : ")
counter = 0
while True:
    for proxy in proxies:
        proxy_parts = proxy.split(',')
        proxy_address = f"{proxy_parts[8]}://{proxy_parts[0]}:{proxy_parts[7]}"
        proxy_dict = {
            'http': proxy_address,
            'https': proxy_address,
        }
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['proxy'] = {
            'proxyType': 'manual',
            'httpProxy': proxy_address,
            'sslProxy': proxy_address,
        }

        try:
            counter += 1
            browser = webdriver.Chrome(options=options, desired_capabilities=capabilities)
            browser.get(link)
            time.sleep(3)
            click = browser.find_element(By.XPATH,'//*[@id="movie_player"]/div[5]/button')
            click.click()
            while True:
                start_time = time.time()
                # Switch to the next tab
                browser.switch_to.window(browser.window_handles[-1])
                time.sleep(35)
                # Reload the video
                end_time = time.time()
                total_time = end_time - start_time
                browser.refresh()
                print(f"Successfully Sent View to {link} .  Iteration: {counter}. Total Time: {total_time:.2f} seconds")

        except:
            browser.quit()
            continue

