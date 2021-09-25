import os, time
from selenium import webdriver
from util import get_img, tgbot_send
from retrying import retry

options = webdriver.FirefoxOptions()
options.add_argument("--headless") #设置火狐为headless无界面模式
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(executable_path=f'{os.getcwd()}/geckodriver', options=options)
print("初始化selenium driver完成")

token = os.environ['TG_BOT_TOKEN']
chatid = os.environ['TG_CHATID']

# 失败后随机 3-5s 后重试，最多 6 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=6)
def login():
    print("访问登录页面")
    driver.get("https://cas.sysu.edu.cn/cas/login")
    time.sleep(4)

    print("读取用户名密码")
    netid = os.environ['NETID']
    password = os.environ['PASSWORD']

    print("输入用户名密码")
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(netid)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    print("识别验证码")
    code = get_img(driver, os.environ['RECURL'])
    print("输入验证码")
    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(code)

    # 点击登录按钮
    print("登录信息门户")
    driver.find_element_by_xpath('//*[@id="fm1"]/section[2]/input[4]').click()
    try:
        print(driver.find_element_by_xpath('//*[@id="cas"]/div/div[1]/div/div/h2').text)
    except:
        print(driver.find_element_by_xpath('//*[@id="fm1"]/div[1]/span').text)
        raise Exception('登陆失败')

# 失败后随机 3-5s 后重试，最多 6 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=6)
def jksb():
    print('访问健康申报页面')
    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
    time.sleep(4)
    try:
        number = driver.find_element_by_xpath('//*[@id="title_description"]').text
        print(number)
    except:
        raise Exception('打开健康申报失败')

    print("点击下一步")
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    time.sleep(4)

    print("提交健康申报")
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    time.sleep(2)
    result = driver.find_element_by_xpath('//div[8]/div/div[1]/div[2]').text
    print("完成健康申报")
    return result

if __name__ == "__main__":
    login()
    try:
        tgbot_send(token, chatid, jksb())
        driver.quit()
    except:
        print('健康申报失败')
        tgbot_send(token, chatid, '健康申报失败')
        driver.quit()

