# jksb_sysu

中山大学健康申报自动化脚本

## 技术方案

选择了python+selenium+firefox，暂不支持chrome以及新版edge，因为中大对chrome内核的浏览器做了反爬，没有办法打开健康申报页面。url方式的爬虫太复杂，看了很久也没弄清楚该怎么请求。

### 验证码

登录页面的验证码使用了比较简单的ocr库，成功率一般。获取验证码的策略比较简单，带上当前的cookie重新请求一次，拿到最新的验证码进行识别。

### 重试机制

默认会重试三次，每次间隔200s，可以在重试注解中调整

可以选择配置email模块，结果以邮件的形式进行通知打卡人

## 启动项目

### 安装依赖

pip install -r requirements.txt

[firefox下载](https://www.mozilla.org/en-US/firefox/new/)

### 初始化配置

1. 在config.json中配置登录名 密码
2. 运行jksb_sysu.py

### 定时运行

1. [window定时运行，通过计划任务，定时执行一次python脚本](https://blog.csdn.net/David_jiahuan/article/details/99960427)
2. 通过APScheduler模块，在云服务器上一直运行python文件

### 打卡结果邮件通知

以及邮箱的用户名 授权码和接受者的邮件地址，需要开启smtp功能

[网易163邮箱启用授权码流程](https://note.youdao.com/ynoteshare/index.html?id=f9fef46114fb922b45460f4f55d96853&type=note&_time=1632103586112)


## 免责声明

账号密码属于敏感信息，建议个人私有化部署，此脚本仅供学习交流使用