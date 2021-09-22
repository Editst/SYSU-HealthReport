from logging import log
from logutil import LogUtil
from inform_jksb import send_result
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import ddddocr
import time
from util import get_img,read_json
from apscheduler.schedulers.blocking import BlockingScheduler
from retrying import retry
import platform
 
if platform.system().lower() == 'windows':
    driver_path = os.getcwd()+"//geckodriver.exe"
    print("windows")
elif platform.system().lower() == 'linux':
    driver_path = os.getcwd()+"//geckodriver"
    print("linux")

ocr = ddddocr.DdddOcr()
log = LogUtil("jksb")

options = webdriver.FirefoxOptions()
options.add_argument("--headless") #设置火狐为headless无界面模式
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(executable_path=driver_path,options=options)
log.get_logger().info("初始化selenium driver完成")

@retry(wait_fixed=200000,stop_max_attempt_number=3) #延迟200s 每次重试
def jksb():
    
    # 记录步骤执行状态
    step = 0

    log.get_logger().info("访问登陆页面")
    login_page = driver.get("https://cas.sysu.edu.cn/cas/login?service=https://portal.sysu.edu.cn/shiro-cas")
    time.sleep(5)


    log.get_logger().info("读取用户名密码")
    data = read_json()
    username = data[0]["username"]
    password = data[0]["password"]


    step = 1 #读取用户名密码成功
    log.get_logger().info("输入用户名密码")
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    step = 2 #输入用户名密码成功
    
    log.get_logger().info("识别验证码")
    code = get_img(ocr,driver)
    step = 3 #识别验证码成功

    log.get_logger().info("输入验证码")
    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(code)
    step = 4 #输入验证码成功

    # 点击登录按钮
    log.get_logger().info("登录信息门户")
    driver.find_element_by_xpath('//*[@id="fm1"]/section[2]/input[4]').click()

    time.sleep(4)

    
    # 进入健康申报
    log.get_logger().info("进入健康申报页面")
    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
    # driver.find_element_by_xpath('//*[@id="topSideLink"]/div[1]/div[3]/div[1]/div[2]/div[1]/div/div/div/div/div/div/div/div/div/ul/li[1]/div[1]').click()
    time.sleep(4)

    # 点击下一步
    log.get_logger().info("健康申报页面，点击下一步")
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    step=5 #进入健康申报页面


    time.sleep(4)
    # 点击提交
    log.get_logger().info("提交健康申报")
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    step=6 #点击提交按钮成功

    time.sleep(2)
    result = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/div[2]').text
    step=7 #健康申报完成
    log.get_logger().info("完成健康申报")

    # driver.quit()
    return "成功"

def inform_result():
    try:
        send_result(jksb())
        driver.quit()
    except Exception as e:
        driver.get_screenshot_as_file(os.getcwd()+"//error.png")
        driver.quit()
        send_result("失败")
    
# 定时任务 每天6：40自动打卡，以邮件形式通知
# scheduler = BlockingScheduler()
# scheduler.add_job(inform_result,'cron',day_of_week ='0-6',hour = 6,minute = 40 )
# scheduler.start()
try:
    inform_result()
    driver.quit()
except Exception as e:
    driver.get_screenshot_as_file(os.getcwd()+"//error.png")
    driver.quit()







