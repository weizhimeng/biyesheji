import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fromaddr = 'xuchen@duoshoubang.cn'
toaddr =['1093759654@qq.com']

def send_email(url, category, Subject):
    for i in (url, category):
        if not isinstance(i, str): i = str(i)
    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = fromaddr
    msg['To'] = str(toaddr)
    body = MIMEText("url:{}页面新元素 ,{}栏目".format(url, category), 'plain')
    msg.attach(body)
    server = smtplib.SMTP_SSL('smtp.duoshoubang.cn', 465)
    # server.SMTP('smtp.duoshoubang.cn', 80)
    server.set_debuglevel(0)
    server.login(fromaddr, "Xc199704")
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

if __name__ == '__main__':
    send_email('qidian','1111','test')