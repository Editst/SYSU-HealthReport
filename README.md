# jksb_sysu

中山大学健康申报自动化脚本，支持定时运行和失败重试，打卡结果email通知

## 技术方案

选择了python+selenium+firefox，暂不支持chrome以及新版edge，因为中大对chrome内核的浏览器做了反爬，没有办法打开健康申报页面。url方式的爬虫太复杂，看了很久也没弄清楚该怎么请求，只能选择这条比较笨的办法。

### 验证码

登录页面的验证码使用了第三方ocr库，成功率不算高，所以加入了重试机制。获取验证码的策略为拿到最新的验证码进行识别，带上cookie与当前账户关联。

### 重试机制

默认会重试三次，每次间隔200s，可以在重试注解中调整

可以选择配置微信推送模块，结果以微信推送的形式通知打卡人
具体获取wxsend_key的方式可参考https://sct.ftqq.com/sendkey

## 启动项目

### 安装依赖
python 3 环境下
pip install -r requirements.txt

[firefox下载](https://www.mozilla.org/en-US/firefox/new/)
window,linux平台的driver已内置

[其他平台driver下载](https://github.com/mozilla/geckodriver/releases)
### 初始化配置

1. 在config.json中配置登录名 密码 wxsend_key
2. 运行jksb_sysu.py

### 定时运行

1. [window定时运行，通过计划任务，定时执行一次python脚本](https://blog.csdn.net/David_jiahuan/article/details/99960427)
2. 通过APScheduler模块，在云服务器上一直运行python文件



### 平台化

可以选择开发个简单的网站，用户提交账号密码，即可托管健康打卡，无需本地部署。但netid密码属于敏感信息，传输存储难免有安全性问题，暂时没有特别好的解决方案，建议个人私有化部署。有空可以写个shell脚本一键部署

## 免责声明

此脚本仅供学习交流，禁止商业使用，使用软件过程中，发生意外造成的损失由使用者承担。如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。
