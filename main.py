import cv2 as cv
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


def findPic(img_bg_path, img_slider_path):
    """
    找出图像中最佳匹配位置
    :param img_bg_path: 滑块背景图本地路径
    :param img_slider_path: 滑块图片本地路径
    :return: 返回最差匹配、最佳匹配对应的x坐标
    """

    # 读取滑块背景图片，参数是图片路径，OpenCV默认使用BGR模式
    # cv.imread()是 image read的简写
    # img_bg 是一个numpy库ndarray数组对象
    img_bg = cv.imread(img_bg_path)

    # 对滑块背景图片进行处理，由BGR模式转为gray模式（即灰度模式，也就是黑白图片）
    # 为什么要处理？ BGR模式（彩色图片）的数据比黑白图片的数据大，处理后可以加快算法的计算
    # BGR模式：常见的是RGB模式
    # R代表红，red; G代表绿，green;  B代表蓝，blue。
    # RGB模式就是，色彩数据模式，R在高位，G在中间，B在低位。BGR正好相反。
    # 如红色：RGB模式是(255,0,0)，BGR模式是(0,0,255)
    img_bg_gray = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)

    # 读取滑块，参数1是图片路径，参数2是使用灰度模式
    img_slider_gray = cv.imread(img_slider_path, 0)

    # 在滑块背景图中匹配滑块。参数cv.TM_CCOEFF_NORMED是opencv中的一种算法
    res = cv.matchTemplate(img_bg_gray, img_slider_gray, cv.TM_CCOEFF_NORMED)

    print('#' * 50)
    print(type(res))  # 打印：<class 'numpy.ndarray'>
    print(res)
    # 打印：一个二维的ndarray数组
    # [[0.05604218  0.05557462  0.06844381... - 0.1784117 - 0.1811338 - 0.18415523]
    #  [0.06151756  0.04408009  0.07010461... - 0.18493137 - 0.18440475 - 0.1843424]
    # [0.0643926    0.06221284  0.0719175... - 0.18742703 - 0.18535161 - 0.1823346]
    # ...
    # [-0.07755355 - 0.08177952 - 0.08642308... - 0.16476074 - 0.16210903 - 0.15467581]
    # [-0.06975575 - 0.07566144 - 0.07783117... - 0.1412715 - 0.15145643 - 0.14800543]
    # [-0.08476129 - 0.08415948 - 0.0949327... - 0.1371379 - 0.14271489 - 0.14166716]]

    print('#' * 50)

    # cv2.minMaxLoc() 从ndarray数组中找到最小值、最大值及他们的坐标
    value = cv.minMaxLoc(res)
    # 得到的value，如：(-0.1653602570295334, 0.6102921366691589, (144, 1), (141, 56))

    print(value, "#" * 30)

    # 获取x坐标，如上面的144、141
    return value[2:][0][0], value[2:][1][0]


def generate_tracks(distance):
    # 给距离加上20，这20像素用在滑块滑过缺口后，减速折返回到缺口
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5  # 减速阀值
    while current < distance:
        if current < mid:
            a = 2  # 加速度为+2
        else:
            a = -3  # 加速度-3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1]
    return forward_tracks, back_tracks


def main():
    # 创建一个参数对象，用来控制谷歌浏览器以无界面模式打开
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_options=chrome_options)

    # 设置浏览器宽高
    driver.set_window_size(width=2000, height=3000)

    wait = WebDriverWait(driver, 10)

    driver.get("https://sso.toutiao.com/")

    try:
        # 获取手机号码输入框
        text_box = wait.until(expected_conditions.presence_of_element_located((By.ID, "user-mobile")))
        print(text_box)

        # 获取发送验证按钮
        send_btn = wait.until(expected_conditions.presence_of_element_located((By.ID, "mobile-code-get")))
        print(send_btn)

    except Exception as e:
        print(e)
        raise RuntimeError("获取 手机号码输入框 或者 发送验证按钮 失败，程序结束")

    text_box.send_keys("18812345678")

    # time.sleep(random.uniform(2, 3))

    try:
        action = ActionChains(driver)
        action.click(send_btn).perform()
    except Exception as e:
        print(e)
    else:
        time.sleep(1.5)

        # 获取 滑块背景图
        bg_image = wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-main"]/img[1]')))
        print("\n背景：")

        print(bg_image)
        bg_image_url = bg_image.get_attribute('src')

        print(bg_image_url)

        # 使用urllib下载背景图
        # 原因是：使用bg_image.screenshot()程序卡在这里，也不报错
        urllib.request.urlretrieve(bg_image_url, "./img_bg.png")

        # 获取 滑块
        slider = wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-main"]/img[2]')))

        print("\n滑块：")
        print(slider)

        # 注意：千万不能通过截图获取滑块，因为滑块不是规则的图形
        # 而截图截出的是矩形，会把滑块周围的滑块背景图一起截取，势必影响匹配
        # slider.screenshot('./img_slider.png')
        slider_url = slider.get_attribute('src')

        urllib.request.urlretrieve(slider_url, "./img_slider.png")

        value_1, value_2 = findPic('./img_bg.png', './img_slider.png')

        print("#" * 30)
        print("最差匹配和最佳匹配对应的x坐标分别是：")
        print(value_1)
        print(value_2)
        print("#" * 30)

        # 获取滑动按钮
        button = wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-drag-button"]/img')))

        action = ActionChains(driver)
        try:
            action.click_and_hold(button).perform()
        except StaleElementReferenceException as e:
            print(e)

        action.reset_actions()

        forward_tracks, back_tracks = generate_tracks(value_2)

        for x in forward_tracks:
            action.move_by_offset(x, 0)  # 前进移动滑块
            print(x)

        print('#' * 50)

        for x in back_tracks:
            action.move_by_offset(x, 0)  # 后退移动滑块
            print(x)

        action.release().perform()


    finally:
        # time.sleep(10000)
        driver.close()


if __name__ == '__main__':
    main()

