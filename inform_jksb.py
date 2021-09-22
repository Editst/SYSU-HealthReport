import requests

from util import read_json

config = read_json()
wxsend_key = config[0]["wxsend_key"]


def send_result(result):
    api = "https://sc.ftqq.com/"+str(wxsend_key)+".send"
    data = {
        "text": "健康申报结果"+result,
        "desp": "如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。"
    }
    req = requests.post(api, data=data)
    if req.status_code == 200:
        print("success")
    else:
        print("error")
