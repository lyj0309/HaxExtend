"""
    BYPASS reCaptcha By YouTube Channel: NIKO TECH
    Captcha + Others By github@Mybdye 2022.03.24
"""

import os
import sys
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import captcha
import globalVal

# secret
USERNAME = os.environ['USERNAME']
PASSWORD = os.environ['PASSWORD']
origin_host = os.environ['HOST']


# origin_host = 'hax.co.id'

def delay():
    time.sleep(random.randint(2, 3))


def barkPush(body):
    # bark push
    # barkUrl = 'https://api.day.app/' + BARKKEY
    # title = 'HaxExtend'
    # requests.get(url=f'{barkUrl}/{title}/{body}?isArchive=1')
    try:
        WXURL = os.environ['WXURL']
        data = {
            "msgtype": "text",
            "text": {
                "content": f"{origin_host}：{body}"
            }
        }
        requests.post(WXURL,json=data)
    except:
        return


def run():
    print(origin_host)
    globalVal.driver.get('https://' + origin_host + '/login')
    # main
    time.sleep(10)
    print('fill username')
    globalVal.driver.find_element(By.XPATH, '//*[@id="text"]').send_keys(USERNAME)
    print('fill password')
    globalVal.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
    delay()
    # reCAPTCHA
    print('do reCAPTCHA')
    captcha.reCAPTCHA()
    time.sleep(10)
    # login
    globalVal.driver.switch_to.default_content()
    print('click login')
    globalVal.driver.find_element(By.NAME, 'login').click()
    time.sleep(10)
    # Extend VPS link
    print('click Extend VPS')
    WebDriverWait(globalVal.driver, 30).until(
        EC.visibility_of_element_located((By.LINK_TEXT, 'Extend VPS Expiration'))).click()
    time.sleep(10)
    # input web address
    print('fill web address')
    globalVal.driver.find_element(By.XPATH, '//*[@id="web_address"]').send_keys(origin_host)
    # captcha
    print('do CAPTCHA')
    globalVal.driver.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(captcha.numCAPTCHA())
    # agreement check
    print('click agreement')
    globalVal.driver.find_element(By.NAME, 'agreement').click()
    # reCAPTCHA again
    # print('do reCAPTCHA')
    # reCAPTCHA()
    # time.sleep(10)
    # globalVal.driver.switch_to.default_content()
    # submit_button (Renew VPS)
    print('click Renew VPS')
    globalVal.driver.find_element(By.NAME, 'submit_button').click()
    time.sleep(15)
    print('copy text')
    body = WebDriverWait(globalVal.driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="response"]/div'))).text
    # print('textBody:', body)
    delay()
    print('bark push',body)
    barkPush(body)
    delay()


if __name__ == '__main__':
    try:
        # create chrome driver
        Options = webdriver.ChromeOptions()
        Options.add_argument('--headless')
        # Options.add_extension('./adguard.crx')
        Options.add_argument('--no-sandbox')
        Options.add_argument('--disable-gpu')
        Options.add_argument('--disable-dev-shm-usage')
        globalVal.driver = webdriver.Chrome(options=Options)
        delay()
        # go to website which have recaptcha protection
    except Exception as e:
        print(e)
        sys.exit(
            "[-] Please update the chromedriver in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")
    run()
    globalVal.driver.quit()
