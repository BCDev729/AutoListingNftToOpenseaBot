# library installation:
# pip3 install -U selenium
# pip3 install webdriver-manager
#
# usage:
# first start Chrome in debug mode:
#   google-chrome --remote-debugging-port=1234
# then:
#   - sign in to MetaMask and select right network and account
#   - connect to OpenSea
# finally start the sell script:
#   python3 sell.py
#
# see here for an example run:
# https://www.youtube.com/watch?v=0B5BIEXcMmI
# needs about 45 seconds per NFT

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# connect to Chrome
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:1234")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# maximum number of NFTs to sell
count_max = 4

# start token number
token = 18

# price in ETH
price = "0.01"

def switch_to_metamask():
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        time.sleep(0.1)
        if 'MetaMask' in driver.title:
            break

# load each NFT, and sell it, if it is available for selling
wait = WebDriverWait(driver, 60)
count = 0
# while True:
try:
    print(f"testing token {token} for sale")

    # load page. This waits until the page is loaded
    driver.get(f"https://testnets.opensea.io/assets/rinkeby/0x88b48f654c30e99bc2e4a1559b4dcf1ad93fa656/108651444898117541705274915681209130002788180308517530609307416954337637695489")

    # wait a bit until all asynchronous calls are done
    time.sleep(3)

    # get and click the sell button. Generates an exception, if there is no sell button
    sell_button = driver.find_element(by=By.XPATH, value='//a[normalize-space()="Sell"]')
    sell_button.click()
    time.sleep(3)

    # set price and click "Complete listing" button
    driver.find_element(by=By.NAME, value='price').send_keys(price)
    driver.find_element(by=By.XPATH, value='//button[normalize-space()="Complete listing"]').click()
    time.sleep(3)

    # click sign button
    driver.find_element(by=By.XPATH, value='//button[normalize-space()="Sign"]').click()

    # wait until MetaMask window is opened
    timeout = 10
    while True:
        if len(driver.window_handles) == 2:
            break
        time.sleep(1)
        timeout -= 1
        if timeout == 0:
            print("timeout")
            break
    time.sleep(2)

    # switch to MetaMask window
    switch_to_metamask()

    # wait until sign message is visible
    sign_message_path = '//span[@class="signature-request-message--node-label"]'
    wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, sign_message_path)))
    time.sleep(0.1)

    # select MetaMask sign message, and scroll down to enable sign button
    switch_to_metamask()
    time.sleep(0.1)
    msg = driver.find_element(by=By.XPATH, value=sign_message_path)
    msg.click()
    page = driver.find_element(by=By.XPATH, value='/*')
    for i in range(10):
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    time.sleep(0.1)

    # click MetaMask sign button
    driver.find_element(by=By.XPATH, value='//button[normalize-space()="Sign"]').click()

    # wait until MetaMask window is closed
    timeout = 10
    while True:
        if len(driver.window_handles) == 1:
            break
        time.sleep(1)
        timeout -= 1
        if timeout == 0:
            print("timeout")
            break
    time.sleep(1)

    # switch to main window
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(1)

    # check for end
    count += 1
    # if count == count_max:
    #     break
    print("token offered for sale")

except NoSuchElementException:
    print("not for sale")

token += 1


print(f"{count} new tokens offered for sale")