import os, time
from selenium import webdriver
from util import get_img
from retrying import retry

driver_path = os.getcwd()+"//geckodriver"
options = webdriver.FirefoxOptions()
options.add_argument("--headless") #设置火狐为headless无界面模式
options.add_argument("--disable-gpu")
driver = webdriver.Firefox(executable_path=driver_path, options=options)
print("初始化selenium driver完成")

@retry(wait_fixed=200000,stop_max_attempt_number=3) #延迟200s 每次重试
def jksb():

    print("访问登陆页面")
    driver.get("https://cas.sysu.edu.cn/cas/login?service=https://portal.sysu.edu.cn/shiro-cas")
    time.sleep(5)

    print("读取用户名密码")
    netid = os.environ['NETID']
    password = os.environ['PASSWORD']

    print("输入用户名密码")
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(netid)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)

    print("识别验证码")
    code = get_img(driver, os.environ["RECURL"])

    print("输入验证码")
    driver.find_element_by_xpath('//*[@id="captcha"]').send_keys(code)

    # 点击登录按钮
    print("登录信息门户")
    driver.find_element_by_xpath('//*[@id="fm1"]/section[2]/input[4]').click()

    time.sleep(4)
    
    # 进入健康申报
    print("进入健康申报页面")
    driver.get("http://jksb.sysu.edu.cn/infoplus/form/XNYQSB/start")
    time.sleep(4)

    # 点击下一步
    print("健康申报页面，点击下一步")
    driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    time.sleep(4)

    # 点击提交
    # print("提交健康申报")
    # driver.find_element_by_xpath('//*[@id="form_command_bar"]/li[1]').click()
    # time.sleep(2)
    # result = driver.find_element_by_xpath('/html/body/div[8]/div/div[1]/div[2]').text
    # print(result)
    # print("完成健康申报")

    driver.quit()
    return True

if __name__ == '__main__':
    jksb()

