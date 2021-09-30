# SYSU Health Report

基于 [@tomatoF](https://github.com/tomatoF) 的 [jksb_sysu](https://github.com/tomatoF/jksb_sysu) 项目，发布到 GitHub Marketplace，方便调用。

可以实现每天定时运行，并使用 Telegram Bot 发送运行结果。

**已可以正常运行，仍存在较大不确定性，谨慎使用**

# 使用

Star 后前往 [SYSU-HealthReport-Template](https://github.com/Editi0/SYSU-HealthReport-Template) 查看。

# 配置

```yaml
jobs:
  report:
    runs-on: windows-latest
    steps:
    - name: Use SYSU Health Report
      uses: Editi0/SYSU-HealthReport@master
      with:
        netid: ${{secrets.NETID}}
        password: ${{secrets.PASSWORD}}
        ocr_token: ${{secrets.OCR_TOKEN}}
        tg_bot_token: ${{secrets.TG_BOT_TOKEN}}
        tg_chatid: ${{secrets.TG_CHATID}}
```

# TODO

**欢迎提交 pull requests 来增加其他通知推送方式，不过要考虑好 Token 的传递问题。**

# 免责声明

此脚本仅供学习交流，禁止商业使用，使用软件过程中，发生意外造成的损失由使用者承担。如遇身体不适、或居住地址发生变化，请及时更新健康申报信息。