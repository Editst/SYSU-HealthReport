from email_jksb import send_email
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import ddddocr
import time
from util import get_img,read_json
from apscheduler.schedulers.blocking import BlockingScheduler
from retrying import retry


ocr = ddddocr.DdddOcr()
# options = 
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-blink-features")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.use_chromium = True
# options.add_argument("headless")
# options.add_argument("disable-gpu")
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#     "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
# })
@retry(wait_fixed=200000,stop_max_attempt_number=3) #延迟200s 每次重试
def jksb():
    
    # 记录步骤执行状态
    step = 0
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless") #设置火狐为headless无界面模式
    options.add_argument("--disable-gpu")
    driver = webdriver.Firefox(executable_path=os.getcwd()+"//geckodriver.exe",options=options)



    # 访问登录页面
    login_page = driver.get("https://cas.sysu.edu.cn/cas/login?service=https://portal.sysu.edu.cn/shiro-cas")

    time.sleep(5)
    data = read_json()
    username = data[0]["username"]
    password = data[0]["password"]

    step = 1 #读取用户名密码成功

    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    step = 2 #输入用户名密码成功

    code = get_img(ocr,driver)
    step = 3 #识别验证码成功

    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(code)
    step = 4 #输入验证码成功

    # 点击登录按钮
    driver.find_element_by_xpath('//*[@id="fm1"]/section[2]/input[4]').click()

    time.sleep(4)

    print("登陆成功")

    
    # 进入健康申报
    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
    # driver.find_element_by_xpath('//*[@id="topSideLink"]/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/ul/li[1]/div[1]').click()
    time.sleep(4)

    # 点击下一步
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    step=5 #进入健康申报页面


    time.sleep(4)
    print("点击提交")
    # 点击提交
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    step=6 #点击提交按钮成功

    time.sleep(2)
    result = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/div[2]').text
    step=7 #健康申报完成
    print(result)
    driver.quit()
    return "成功"

def inform_result():
    try:
        send_email(jksb())
    except Exception as e:
        send_email("失败")
    
# 定时任务 每天6：40自动打卡，以邮件形式通知
# scheduler = BlockingScheduler()
# scheduler.add_job(inform_result,'cron',day_of_week ='0-6',hour = 6,minute = 40 )
# scheduler.start()
jksb()







