# jksb_sysu

基于 [@tomatoF](https://github.com/tomatoF) 的 [jksb_sysu](https://github.com/tomatoF/jksb_sysu) 项目，适配了 GitHub Actions，可以实现每天定时运行，并使用 Telegram Bot 或微信发送运行结果。

**目前仍处于测试状态，功能未完善，不保证可以成功运行**

## 技术方案

python+selenium+firefox。

## 项目配置

首先 Fork 此项目**顺便 Star 一下**，之后前往 Settings-Secrets 填写下列信息，注意需要大写。

### 验证码

采用[第三方在线识别平台](http://fast.95man.com)，每日免费额度100，请自行前往注册账号，获取 Token。

将上述的 Token 填入 `OCR_TOKEN` 中。

### 账号密码

将 netid 填入 `NETID` 中，将密码填入 `PASSWORD` 中。

### Telegram Bot 推送

如果希望使用 Telegram Bot 推送运行结果，将你的 Bot 的 Token 填入 `TG_BOT_TOKEN`，将你与该 Bot 的 chatid 填入 `TG_CHATID` 中。

使用该通知方式假定你已知道如何设置，具体请 Google，否则请放弃，**并随意填写上述两项**。

## 免责声明

此脚本仅供学习交流，禁止商业使用，使用软件过程中，发生意外造成的损失由使用者承担。如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。
