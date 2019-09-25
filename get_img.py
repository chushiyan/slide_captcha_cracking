import cv2
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import urllib.request
import random

# 创建一个参数对象，用来控制谷歌浏览器以无界面模式打开
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 设置代理
# chrome_options.add_argument('--proxy-server=http://127.0.0.1:8080')

# 设置启动时设置默认语言为英文
# chrome_options.add_argument('lang=en_US')

# 忽略https证书
# chrome_options.add_argument('--ignore-certificate-errors')

driver = webdriver.Chrome(chrome_options=chrome_options)

driver.set_window_size(width=2000, height=3000)

wait = WebDriverWait(driver, 20)


def get_img(index):
    driver.get("https://sso.toutiao.com/")
    try:

        # 获取输入框
        text_box = wait.until(expected_conditions.presence_of_element_located((By.ID, "user-mobile")))
        print(text_box)

        # 获取发送验证按钮
        send_btn = wait.until(expected_conditions.presence_of_element_located((By.ID, "mobile-code-get")))
        print(send_btn)

    except Exception as e:
        print(e)

    else:
        time.sleep(random.uniform(3, 6))
        text_box.send_keys("18887654321")
        try:
            action = ActionChains(driver)
            action.click(send_btn).perform()
        except Exception as e:
            print(e)
        else:
            time.sleep(1.5)
            # 滑块背景图
            bg_image = wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-main"]/img[1]')))
            print("\n背景：")
            print(bg_image)
            bg_image_url = bg_image.get_attribute('src')
            print('##### ', bg_image_url, ' ######')

            if bg_image_url is None:
                # 获取验证码过于频繁会出现 不显示验证码的情况，导致滑块背景图片地址为空
                time.sleep(random.uniform(20, 30))
                return

            # 使用urllib下载背景图。
            # 原因是：使用bg_image.screenshot()程序卡在这里，也不报错
            try:
                urllib.request.urlretrieve(bg_image_url, "./images/{}_{}.png".format(index, 1))
            except Exception as e:
                print(e)
                return

                # bg_image.screenshot('./img_bg.png')

            # 滑块
            slider = wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-main"]/img[2]')))
            print("\n滑块：")
            print(slider)

            slider_url = slider.get_attribute('src')
            urllib.request.urlretrieve(slider_url, "./images/{}_{}.png".format(index, 2))

    finally:
        a = random.uniform(10, 15)
        print(a)
        time.sleep(a)


def main():
    for i in range(20000, 20100 + 1):
        print('#' * 50)
        print(i)
        print('#' * 50)
        get_img(i)


if __name__ == '__main__':
    main()
    driver.close()
