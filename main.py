"""
    BYPASS reCaptcha By YouTube Channel: NIKO TECH
    Captcha + Others By github@Mybdye 2022.03.24
"""
import random
import urllib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os
import sys
import time
import requests

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
urlLogin = 'https://hax.co.id/login'
urlRenew = 'https://hax.co.id/vps-renew/'
SpeechToTextURL = 'https://speech-to-text-demo.ng.bluemix.net/'
# secret
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
BARKKEY = os.environ['BARKKEY']


def delay():
    time.sleep(random.randint(2, 3))

def audioToText(audioFile):
    driver.execute_script('''window.open("","_blank")''')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(SpeechToTextURL)

    delay()
    audioInput = driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return result

def reCAPTCHA():
    g_recaptcha = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
    outerIframe.click()

    iframes = driver.find_elements(By.TAG_NAME, 'iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        driver.switch_to.default_content()
        iframe = driver.find_elements(By.TAG_NAME, 'iframe')[index]
        driver.switch_to.frame(iframe)
        driver.implicitly_wait(delayTime)
        try:
            audioBtn = driver.find_element(By.ID, "recaptcha-audio-button")
            audioBtn.click()
            audioBtnFound = True
            audioBtnIndex = index
            break
        except Exception as e:
            pass

    if audioBtnFound:
        try:
            while True:
                # get the mp3 audio file
                src = driver.find_element(By.ID, "audio-source").get_attribute("src")
                print("[INFO] Audio src: %s" % src)

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, os.getcwd() + audioFile)

                # Speech To Text Conversion
                key = audioToText(os.getcwd() + audioFile)
                print("[INFO] Recaptcha Key: %s" % key)

                driver.switch_to.default_content()
                iframe = driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = driver.find_element(By.ID, "audio-response")
                inputField.send_keys(key)
                delay()
                inputField.send_keys(Keys.ENTER)
                delay()
                delay()

                err = driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    print("[INFO] Success!")
                    break

        except Exception as e:
            print(e)
            barkPush('[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests')
            sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    else:
        # sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
        print('reCAPTCHA not found!')
    print('reCAPTCHA done')

def CAPTCHA():
    # 获取 captcha 图片链接
    number1 = int(driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][0])
    caculateMethod = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]').text[0]
    number2 = int(driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][0])
    print('Method', caculateMethod)
    if caculateMethod == '+':
        captcha_result = number1 + number2
    elif caculateMethod == '-':
        captcha_result = number1 - number2
    elif caculateMethod == 'X':
        captcha_result = number1 * number2
    elif caculateMethod == '/':
        captcha_result = number1 / number2
    return captcha_result

def barkPush(body):
    # bark push
    barkUrl = 'https://api.day.app/' + BARKKEY
    title = 'HaxExtend'
    requests.get(url=f'{barkUrl}/{title}/{body}?isArchive=1')
    print('bark push Done!')

# try:
    # create chrome driver
#     Options = webdriver.ChromeOptions()
#     Options.add_argument('--headless')
#     Options.add_argument('--no-sandbox')
#     Options.add_argument('--disable-gpu')
#     Options.add_argument('--disable-dev-shm-usage')
#     chromedriver = '/usr/local/share/chrome_driver'
#     os.environ["webdriver.chrome.driver"] = chromedriver
#     driver = webdriver.Chrome()
# #   driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     delay()
#     # go to website which have recaptcha protection
#     driver.get(urlLogin)
# except Exception as e:
#     sys.exit(
#         "[-] Please update the chromedriver in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

# options = Options()
# options.add_argument("--no-sandbox") #bypass OS security model

#driver = webdriver.Chrome(options=options, executable_path='/usr/local/share/chrome_driver')
# driver = webdriver.Chrome(options=options, executable_path='/usr/bin/chromedriver')
driver = webdriver.Firefox()

delay()
driver.get(urlLogin)

driver.find_element(By.XPATH, '//*[@id="text"]').send_keys(USERNAME)
driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
delay()
# reCAPTCHA
reCAPTCHA()
time.sleep(6)
# login
driver.switch_to.default_content()
driver.find_element(By.NAME, 'login').click()
# Extend VPS link
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Extend VPS Expiration'))).click()
time.sleep(6)
# input web address
driver.find_element(By.XPATH, '//*[@id="web_address"]').send_keys('hax.co.id')
# captcha
driver.find_element(By.XPATH,'//*[@id="captcha"]').send_keys(CAPTCHA())
# agreement check
driver.find_element(By.NAME, 'agreement').click()
# reCAPTCHA again
reCAPTCHA()
time.sleep(6)
driver.switch_to.default_content()
# submit_button (Renew VPS)
driver.find_element(By.NAME, 'submit_button').click()
time.sleep(12)
body = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="response"]/div'))).text
print('textBody:', body)
barkPush(body)
delay()
driver.quit()
