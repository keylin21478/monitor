# html解析头文件
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import operator
# 邮件头文件
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
# 休眠函数头文件
import datetime
import time


# 判断是否有货
def judge(target1):
    # html = urlopen("file:///C:/Users/linkey/Desktop/产品选购 - drServer.net.html")
    html = urlopen("https://portal.drserver.net/?/cart/dedicated-servers/")
    bsObj = BeautifulSoup(html, "html.parser")
    productlist = bsObj.findAll("td", {"class", "product-name"})

    for product in productlist:
        name = product.strong.get_text()
        # print(name)
        ok = operator.eq(target1, name)
        if ok == 1:
            return 1

    return 0


# 邮件发送函数
def mail(msgSend):
    my_sender = '421056455@qq.com'  # 发件人邮箱账号
    my_pass = 'jaubalfbzdlubibi'  # 发件人邮箱密码(当时申请smtp给的口令)
    my_user = '421056455@qq.com'  # 收件人邮箱账号，我这边发送给自己
    ret = True
    try:
        msg = MIMEText(msgSend, 'plain', 'utf-8')
        msg['From'] = formataddr(["发件人昵称", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["收件人昵称", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "邮件主题-监控Drserver"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
        print("邮件发送失败")
    return ret


target1 = "Intel® Atom™ C2750 (8-Core, 2.4GHz) - 16GB RAM - 2TB HDD"  # 监控目标

# 默认历史无，且监控无货
PreviousStatus = 0
NowStatus = 0
sum = 1
while 1:
    print("---------------开启第", sum, "轮监控---------------", '\n')
    now = datetime.datetime.now()  # 获取监控的时间
    NowStatus = judge(target1)  # 调用监控函数
    now2 = datetime.datetime.now()
    dtime = now2 - now
    property = PreviousStatus + NowStatus
    if property < 1:
        msg = '历史无货，且现在无货'
        print(now, msg)
    elif property > 1:
        msg = '历史有货，且现在有货'
        print(now, msg)
    elif property == 1:
        msg1 = '库存改变'
        p1 = NowStatus - PreviousStatus
        if p1 == 1:
            msg2 = '，现在有货'
        elif p1 == -1:
            msg2 = "，现在缺货"
        msg = msg1 + msg2
        print(now, msg)
        mail(msg)
    sum = sum + 1
    # print(sum)
    print("监控耗时", dtime)
    PreviousStatus = NowStatus
    time.sleep(11.11)
