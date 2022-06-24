import os, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from util import recognize
from retrying import retry

driver = webdriver.Firefox(service=Service(f"{os.environ['GITHUB_ACTION_PATH']}/geckodriver.exe"))
print("初始化selenium driver完成")

bot_token = os.environ['TG_BOT_TOKEN']
chatid = os.environ['TG_CHATID']


# 失败后随机 1-3s 后重试，最多 10 次
@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=10)
def login():
    print("访问登录页面")
    driver.get("https://cas.sysu.edu.cn/cas/login")
    time.sleep(10)

    print("读取用户名密码")
    netid = os.environ['NETID']
    password = os.environ['PASSWORD']

    print("输入用户名密码")
    driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(netid)
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password)

    print("识别验证码")
    code = recognize(driver)
    print("输入验证码")
    driver.find_element(By.XPATH,'//*[@id="captcha"]').send_keys(code)

    # 点击登录按钮
    print("登录信息门户")
    driver.find_element(By.XPATH,'//*[@id="fm1"]/section[2]/input[4]').click()
    try:
        print(driver.find_element(By.XPATH,'//*[@id="cas"]/div/div[1]/div/div/h2').text)
    except:
        print(driver.find_element(By.XPATH,'//*[@id="fm1"]/div[1]/span').text)
        raise Exception('登陆失败')

# 失败后随机 3-5s 后重试，最多 6 次
@retry(wait_random_min=3000, wait_random_max=5000, stop_max_attempt_number=2)
def jksb():
    print('访问健康申报页面')
    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
    time.sleep(15)
    try:
        number = driver.find_element(By.XPATH, '//*[@id="title_description"]').text
        print('打开健康申报成功')
    except:
        print('打开健康申报失败')
        raise Exception('打开健康申报失败')

    print("点击下一步")
    driver.find_element(By.XPATH, '//*[@id="form_command_bar"]/li[1]').click()
    time.sleep(15)

    print("提交健康申报")
    driver.find_element(By.XPATH, '//*[@id="form_command_bar"]/li[1]').click()
    time.sleep(15)
    result = driver.find_element(By.XPATH, '//div[8]/div/div[1]/div[2]').text
    print("完成健康申报")
    return f'{number}: {result}'

if __name__ == "__main__":
    login()
    time.sleep(4)
    try:
        result = jksb()
    except:
        result = '健康申报失败'
        print(result)
    driver.quit()

    # 判断是否发送通知
    if bot_token in ['False', '']:
        pass
    elif bot_token.startswith('SCT'):
        from util import wx_send
        wx_send(bot_token, result)
    else:
        from util import tgbot_send
        tgbot_send(bot_token, chatid, result)
