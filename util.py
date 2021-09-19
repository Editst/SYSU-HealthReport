from email_jksb import send_email
import requests,json
def get_img(ocr,driver):
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
    with open("config.json",'r') as load_f:
      load_dict = json.load(load_f)
    return load_dict
