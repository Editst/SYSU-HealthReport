from email_jksb import send_email
import requests,json
def get_img(ocr,driver):
    """
    获取最新的一张验证码图片，并返回识别结果
    :param ocr: 识别验证码库实例
    :param driver: 驱动实例，获取cookie
    :return res:识别结果 
    """
    cookies=driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    url = "https://cas-443.webvpn.sysu.edu.cn/cas/captcha.jsp"
    res =  s.get(url)
    with open('1.jpg',"wb") as f:
        f.write(res.content)

    with open('1.jpg', 'rb') as f:  
        img_bytes = f.read()
    res = ocr.classification(img_bytes)
    return res 
def read_json():
    """
    从config.json读取配置文件
    """
    with open("config.json",'r') as load_f:
      load_dict = json.load(load_f)
    return load_dict
