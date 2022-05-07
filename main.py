"""
    BYPASS reCaptcha By YouTube Channel: NIKO TECH
    Captcha + Others By github@Mybdye 2022.03.24
"""
import os
import sys
import time
import random
import urllib
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha

audioToTextDelay = 10
delayTime = 2
audioFile = "\\payload.mp3"
origin_host = 'hax.co.id'
SpeechToTextURL = 'https://speech-to-text-demo.ng.bluemix.net/'

# secret
USERNAME = os.environ['USERNAME']

PASSWORD = os.environ['PASSWORD']
TWOCAPTCHA_TOKEN = os.environ['TWOCAPTCHA_TOKEN']
solver = TwoCaptcha(TWOCAPTCHA_TOKEN)

try:
    BARKKEY = os.environ['BARKKEY']
    barkKey = 1
except:
    print('No BarkKey')
    barkKey = 0

global driver


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
    # google大概率不会让你用音频，只能用图片
    g_recaptcha = driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    sitekey = g_recaptcha.get_attribute("data-sitekey")
    result = solver.recaptcha(sitekey=sitekey, url='https://' + origin_host + '/login')
    print("recaptcha_res", result)
    driver.execute_script(
        """document.querySelector('[name="g-recaptcha-response"]').innerText='{}'""".format(result['code']))
    print('reCAPTCHA done')


def CAPTCHA():
    # 获取 captcha 图片链接
    number1 = int(
        driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][
            0])
    caculateMethod = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]').text[0]
    number2 = int(
        driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][
            0])
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
    if barkKey == 1:
        # bark push
        # barkUrl = 'https://api.day.app/' + BARKKEY
        # title = 'HaxExtend'
        # requests.get(url=f'{barkUrl}/{title}/{body}?isArchive=1')
        print(requests.get(
            url=f'https://service-lqj0ehgj-1256627948.bj.apigw.tencentcs.com/release/wecomchan?sendkey=wabehawbyuhiul323&msg_type=text&msg=hax_extend：{body}'))
        print('bark push Done! Body:', body)
    elif barkKey == 0:
        print('No barkKey, Body is:', body)


try:
    # create chrome driver
    Options = webdriver.ChromeOptions()
    Options.add_argument('--headless')
    # Options.add_extension('./adguard.crx')
    Options.add_argument('--no-sandbox')
    Options.add_argument('--disable-gpu')
    Options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=Options)
    delay()
    # go to website which have recaptcha protection
    print(origin_host)
except Exception as e:
    print(e)
    sys.exit(
        "[-] Please update the chromedriver in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")


def run():
    driver.get('https://' + origin_host + '/login')
    # main
    time.sleep(10)
    print('fill username')
    driver.find_element(By.XPATH, '//*[@id="text"]').send_keys(997077701)
    print('fill password')
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(PASSWORD)
    delay()
    # reCAPTCHA
    print('do reCAPTCHA')
    reCAPTCHA()
    time.sleep(10)
    # login
    driver.switch_to.default_content()
    print('click login')
    driver.find_element(By.NAME, 'login').click()
    time.sleep(10)
    # Extend VPS link
    print('click Extend VPS')
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.LINK_TEXT, 'Extend VPS Expiration'))).click()
    time.sleep(10)
    # input web address
    print('fill web address')
    driver.find_element(By.XPATH, '//*[@id="web_address"]').send_keys(origin_host)
    # captcha
    print('do CAPTCHA')
    driver.find_element(By.XPATH, '//*[@id="captcha"]').send_keys(CAPTCHA())
    # agreement check
    print('click agreement')
    driver.find_element(By.NAME, 'agreement').click()
    # reCAPTCHA again
    # print('do reCAPTCHA')
    # reCAPTCHA()
    # time.sleep(10)
    # driver.switch_to.default_content()
    # submit_button (Renew VPS)
    print('click Renew VPS')
    driver.find_element(By.NAME, 'submit_button').click()
    time.sleep(15)
    print('copy text')
    body = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="response"]/div'))).text
    # print('textBody:', body)
    delay()
    print('bark push')
    barkPush(body)
    delay()
    driver.quit()


if __name__ == '__main__':
    run()
    origin_host = 'woiden.id'
    run()
