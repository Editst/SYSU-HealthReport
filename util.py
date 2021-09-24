import requests

def get_img(driver, rec_url):
    ''' 调用某位不知名好心人的在线识别验证码后端
    '''
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

    url = "https://cas.sysu.edu.cn/cas/captcha.jsp"
    res =  s.get(url)
    files = {'img': ('captcha.jpg', res.content, 'image/jpeg')}
    r =  requests.post(rec_url, files = files)
    if len(r.text) == 4:
        capt = r.text
        print(f'验证码识别成功：{capt}')
        return capt
    else:
        print(f'识别失败：{r.text}，重试')
        return False
