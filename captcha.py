import urllib
import time
import os

from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import globalVal
import main

delayTime = 2
audioToTextDelay = 10
TWOCAPTCHA_TOKEN = os.environ['TWOCAPTCHA_TOKEN']
solver = TwoCaptcha(TWOCAPTCHA_TOKEN)
audioFileName = "\\payload.mp3"

SpeechToTextURL = 'https://speech-to-text-demo.ng.bluemix.net/'


def audioToText(audioFile):
    globalVal.driver.execute_script('''window.open("","_blank")''')
    globalVal.driver.switch_to.window(globalVal.driver.window_handles[1])
    globalVal.driver.get(SpeechToTextURL)

    main.delay()
    audioInput = globalVal.driver.find_element(By.XPATH, '//*[@id="root"]/div/input')
    print(audioFile)
    audioInput.send_keys(audioFile)

    time.sleep(audioToTextDelay)

    text = globalVal.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')
    while text is None:
        text = globalVal.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[7]/div/div/div/span')

    result = text.text

    globalVal.driver.close()
    globalVal.driver.switch_to.window(globalVal.driver.window_handles[0])

    return result


def twoCaptcha(g_recaptcha):
    # google大概率不会让你用音频，只能用图片
    sitekey = g_recaptcha.get_attribute("data-sitekey")
    result = solver.recaptcha(sitekey=sitekey, url='https://' + main.origin_host + '/login')
    print("recaptcha_res", result)
    globalVal.driver.execute_script(
        """document.querySelector('[name="g-recaptcha-response"]').innerText='{}'""".format(result['code']))


def reCAPTCHA():
    g_recaptcha = globalVal.driver.find_elements(By.CLASS_NAME, 'g-recaptcha')[0]
    outerIframe = g_recaptcha.find_element(By.TAG_NAME, 'iframe')
    outerIframe.click()

    iframes = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')
    audioBtnFound = False
    audioBtnIndex = -1

    for index in range(len(iframes)):
        globalVal.driver.switch_to.default_content()
        iframe = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')[index]
        globalVal.driver.switch_to.frame(iframe)
        globalVal.driver.implicitly_wait(delayTime)
        try:
            audioBtn = globalVal.driver.find_element(By.ID, "recaptcha-audio-button")
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
                src = globalVal.driver.find_element(By.ID, "audio-source").get_attribute("src")
                print("[INFO] Audio src: %s" % src)

                # download the mp3 audio file from the source
                urllib.request.urlretrieve(src, os.getcwd() + audioFileName)

                # Speech To Text Conversion
                key = audioToText(os.getcwd() + audioFileName)
                print("[INFO] Recaptcha Key: %s" % key)

                globalVal.driver.switch_to.default_content()
                iframe = globalVal.driver.find_elements(By.TAG_NAME, 'iframe')[audioBtnIndex]
                globalVal.driver.switch_to.frame(iframe)

                # key in results and submit
                inputField = globalVal.driver.find_element(By.ID, "audio-response")
                inputField.send_keys(key)
                main.delay()
                inputField.send_keys(Keys.ENTER)
                main.delay()
                main.delay()

                err = globalVal.driver.find_elements(By.CLASS_NAME, 'rc-audiochallenge-error-message')[0]
                if err.text == "" or err.value_of_css_property('display') == 'none':
                    print("[INFO] Success!")
                    break

        except Exception as e:
            print(e)
            print("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
            print("获取语言验证码失败，尝试使用图片fuck reCAPTCHA")
            twoCaptcha(g_recaptcha)
            # sys.exit("[INFO] Possibly blocked by google. Change IP,Use Proxy method for requests")
    else:
        # sys.exit("[INFO] Audio Play Button not found! In Very rare cases!")
        print('reCAPTCHA not found!')
    print('reCAPTCHA done')


def numCAPTCHA():
    # 获取 captcha 图片链接
    number1 = int(
        globalVal.driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[1]').get_attribute('src').split('-')[1][
            0])
    caculateMethod = globalVal.driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]').text[0]
    number2 = int(
        globalVal.driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/div[1]/img[2]').get_attribute('src').split('-')[1][
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
